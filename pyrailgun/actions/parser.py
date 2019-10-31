

__author__ = 'haku-mac'

import re
import sys

from bs4 import BeautifulSoup

from pyrailgun.actions.action import RailGunAction

if sys.version > '3':
    unicode = str


class ParserAction(RailGunAction):

    def action(self, task_entry, shell_groups, global_data):
        rule = task_entry['rule'].strip()
        parent_name = task_entry.get('parentName')
        self.logger.info("parsing with rule " + rule)
        strip = task_entry.get('strip')
        datas = task_entry.get('datas')
        pos = task_entry.get('pos')
        attr = task_entry.get('attr')
        parsed_datas = []
        for data in datas:
            self.logger.debug("parse from raw " + str(data))
            if isinstance(data, str):
                soup = BeautifulSoup(data)
            else:
                soup = data
            # apply rule
            parsed_data_sps = soup.select(rule)
            data_len = len(parsed_data_sps)
            if data_len > 0:
                # set pos
                if None != pos:
                    if pos > len(parsed_data_sps) - 1:
                        parsed_data_sps = []
                    else:
                        parsed_data_sps = [parsed_data_sps[pos]]
                # find parent
                if parent_name:
                    parsed_data_sps = parsed_data_sps[0]
                    parsed_data_sps = [parsed_data_sps.find_parent(parent_name.strip())]
                for i in range(data_len):
                    tag = parsed_data_sps[i]
                    if None != attr:
                        tag = tag.get(attr)
                    if strip == 'true':
                        tag = unicode(tag)
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
        if current_shell is not None and task_entry.get('setField') is not None and len(parsed_datas) > 0:
            field_name = task_entry.get('setField')
            self.logger.debug("set" + field_name + "as" + str(parsed_datas))
            current_shell[field_name] = parsed_datas
        task_entry['datas'] = parsed_datas
        return task_entry
