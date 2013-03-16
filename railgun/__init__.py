#    coding: UTF-8
#    User: haku
#    Date: 13-2-14
#    Time: 上午1:01
#
__author__ = 'haku'
import re
import requests
import yaml
from bs4 import BeautifulSoup
from __pattern import Pattern
from __logging import Logger


class RailGun():
    def __init__(self):
        self.config_data = self.shell_groups = {}
        self.logger = Logger.getLogger()

    # set taskdata into me
    def setTaskData(self, taskdata):
        self.taskData = dict(taskdata)

    # set taskdata into me via a yaml file
    def setTask(self, tfile):
        assert isinstance(tfile, file), "taskfile should be an instance file, get" + str(type(tfile))
        taskData = yaml.load(tfile)
        self.taskData = dict(taskData)

    # set some running configure
    def setConfig(self, config_key, config_value):
        self.config_data[config_key] = config_value

    # do work
    def fire(self):
        self.__parserShells(self.taskData)
        return self.shell_groups

    # get parsed shells
    def getShells(self, groupname='default'):
        return self.shell_groups.get(groupname)

    def __parserShells(self, task_entry):
        """

        :param task_entry:
        :return:
        """
        if (isinstance(task_entry, unicode)):
            return
            # do current action
        actionname = task_entry["action"].strip()
        if None != task_entry.get('shellid'):
            self.logger.info("info current shell [" + task_entry.get('shellgroup') + ":" + \
                             str(task_entry.get('shellid')) + "]")

        actionMap = { 'main': "__main"
            , 'shell': '__createShell'
            #, 'faketask': '__faketask'
            , 'fetcher': '__fetch'
            , 'parser': '__parser'
        }

        if actionname in actionMap.keys():
            worker = getattr(self
                , '_RailGun{}'.format(actionMap[actionname])
            )
            if callable(worker):
                task_entry = worker(task_entry)

        if (None == task_entry.get('subaction')):
            return

        for subtask in task_entry['subaction']:
            # if entry is not fakedshell and entry has datas then copy to subtask
            if (subtask['action'] != 'faketask' and task_entry.get('datas') != None):
                subtask['datas'] = task_entry.get('datas')
                # ignore datas field
            if 'datas' == str(subtask):
                continue
                # passed to subtask
            if None != task_entry.get('shellgroup'):
                subtask['shellgroup'] = task_entry.get('shellgroup')
            if None != task_entry.get('shellid'):
                subtask['shellid'] = task_entry.get('shellid')
            self.__parserShells(subtask)
        return

    def __main(self, task_entry):
        self.logger.info("task_entry['name']" + "运行")
        return task_entry

    def __fetch(self, task_entry):
        p = Pattern(task_entry, self.__getCurrentShell(task_entry))
        urls = p.convertPattern('url')
        s = requests.session()
        task_entry['datas'] = []
        for url in urls:
            self.logger.info("fetching " + url)
            if "" == url:
                # do not fetch null url
                continue
            data = s.get(url).text
            task_entry['datas'].append(data)
        return task_entry

    def __parser(self, task_entry):
        rule = task_entry['rule'].strip()
        self.logger.info("parsing with rule " + rule)
        strip = task_entry.get('strip')
        datas = task_entry.get('datas')
        pos = task_entry.get('pos')
        attr = task_entry.get('attr')
        parsed_datas = []
        for data in datas:
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
                    attr_data = BeautifulSoup(tag)
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
        current_shell = self.__getCurrentShell(task_entry)
        if current_shell != None and task_entry.get('setField') != None:
            fieldname = task_entry.get('setField')
            self.logger.debug("set" + fieldname + "as" + str(parsed_datas));
            current_shell[fieldname] = parsed_datas
        task_entry['datas'] = parsed_datas
        return task_entry

    def __createShell(self, task_entry):
        datas = task_entry.get('datas')
        # every shell has only one data
        subacts = []
        self.logger.info(str(len(datas)) + " shells created")
        shellgroup = task_entry.get('group', 'default')
        shellid = 0
        self.shell_groups[shellgroup] = {}
        for data in datas:
            shellid += 1
            # init shell
            self.shell_groups[shellgroup][shellid] = {}
            # task entry splited into pieces
            # sub actions nums = now sub nums * shell num
            subact = {
                "action": "faketask",
                "shellgroup": shellgroup,
                "shellid": shellid,
                "datas": [data],
                "subaction": task_entry["subaction"]
            }
            subacts.append(subact)
        task_entry["subaction"] = subacts
        return task_entry

    def __getCurrentShell(self, task_entry):
        if (None == task_entry.get('shellgroup')):
            return None
        shellgroup = task_entry['shellgroup']
        if None == self.shell_groups.get(shellgroup):
            return None
        shellid = task_entry['shellid']
        shell = self.shell_groups[shellgroup][shellid]
        return shell