

__author__ = 'haku-mac'

import re, time
import requests
import json
from pyrailgun.actions.action import RailGunAction
from pyrailgun.logger import Logger
from bs4 import BeautifulSoup


class ParserAction(RailGunAction):

    def action(self, task_entry, shell_groups):
        rule = task_entry['rule'].strip()
        self.logger.info("parsing with rule " + rule)
        strip = task_entry.get('strip')
        datas = task_entry.get('datas')
        pos = task_entry.get('pos')
        attr = task_entry.get('attr')
        parsed_datas = []
        for data in datas:
            self.logger.debug("parse from raw " + str(data))
            soup = BeautifulSoup(data)
            parsed_data_sps = soup.select(rule)
            # set pos
            if (None != pos):
                if pos > len(parsed_data_sps) - 1:
                    parsed_data_sps = []
                else:
                    parsed_data_sps = [parsed_data_sps[pos]]
            for tag in parsed_data_sps:
                tag = unicode(tag)
                if (None != attr):
                    attr_data = BeautifulSoup(tag.encode("utf8"))
                    tag = attr_data.contents[0].get(attr)
                if strip == 'true':
                    dr = re.compile(r'<!--.*-->')
                    tag = dr.sub('', tag)
                    dr = re.compile(r'<.*?>')
                    tag = dr.sub('', tag)
                    dr = re.compile(r'[\r\n]')
                    tag = dr.sub('', tag)
                parsed_datas.append(tag)
        self.logger.info("after parsing " + str(len(parsed_datas)))
        # set data to shell
        current_shell = self.get_current_shell(task_entry, shell_groups)
        if current_shell != None and task_entry.get('setField') != None and len(parsed_datas) > 0:
            fieldname = task_entry.get('setField')
            self.logger.debug("set" + fieldname + "as" + str(parsed_datas));
            current_shell[fieldname] = parsed_datas
        task_entry['datas'] = parsed_datas
        return task_entry