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


class RailGun():
    def __init__(self):
        self.config_data = dict([])
        self.shell_groups = dict([])

    # set taskdata into me
    def setTaskData(self, taskdata):
        self.taskdata = dict(taskdata)

    # set taskdata into me via a yaml file
    def setTask(self, tfile):
        assert isinstance(tfile, file), "taskfile should be an instance file, get" + str(type(tfile))
        taskdata = yaml.load(tfile)
        self.taskdata = dict(taskdata)

    # set some running configure
    def setConfig(self, config_key, config_value):
        self.config_data[config_key] = config_value

    # do work
    def fire(self):
        self.__parserShells(self.taskdata)
        return self.shell_groups

    # get parsed shells
    def getShells(self, groupname='default'):
        return self.shell_groups.get(groupname)

    def __parserShells(self, task_entry):
        if (None == task_entry):
            return
        if (isinstance(task_entry, unicode)):
            return
            # do current action
        actionname = task_entry["action"].strip()
        if actionname == 'main':
            task_entry = self.__main(task_entry)
        if actionname == 'shell':
            task_entry = self.__createShell(task_entry)
        if actionname == 'faketask':
            pass
        if actionname == 'fetcher':
            task_entry = self.__fetch(task_entry)
        if actionname == 'parser':
            task_entry = self.__parser(task_entry)
        if (None == task_entry.get('subaction')):
            return
        for subtask in task_entry['subaction']:
            # if entry is not fakedshell and entry has datas then copy to subtask
            if (subtask['action'] != 'faketask' and task_entry.get('datas') != None):
                subtask['datas'] = task_entry.get('datas')
                # ignore datas field
            if str(subtask) == 'datas':
                continue;
                # passed to subtask
            if task_entry.get('shellgroup') != None:
                subtask['shellgroup'] = task_entry.get('shellgroup')
            if task_entry.get('shellid') != None:
                subtask['shellid'] = task_entry.get('shellid')
            self.__parserShells(subtask)
        return

    def __main(self, task_entry):
        print task_entry['name'], "运行"
        return task_entry

    def __fetch(self, task_entry):
        p = Pattern(task_entry, self.__getCurrentShell(task_entry))
        urls = [task_entry['url'].strip()]
        if (p.convertPattern('url')):
            urls = p.getConvertdStr()
        s = requests.session()
        task_entry['datas'] = []
        for url in urls:
            print "fetching ", url
            data = s.get(url)
            task_entry['datas'].append(data.text)
        return task_entry

    def __parser(self, task_entry):
        rule = task_entry['rule'].strip()
        print "parsing with rule ", rule
        strip = task_entry.get('strip')
        datas = task_entry.get('datas')
        pos = task_entry.get('pos')
        attr = task_entry.get('attr')
        parsed_datas = []
        for data in datas:
            soup = BeautifulSoup(data)
            parsed_data_sps = soup.select(rule)
            # set pos
            if (None != pos) :
                if pos > len(parsed_data_sps) - 1:
                    parsed_data_sps = []
                else :
                    parsed_data_sps = [parsed_data_sps[pos]]
            for tag in parsed_data_sps:
                tag = unicode(tag)
                if (None != attr) :
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
        print "after parsing", len(parsed_datas)
        # set data to shell
        current_shell = self.__getCurrentShell(task_entry)
        if current_shell != None and task_entry.get('setField') != None:
            fieldname = task_entry.get('setField')
            print "set ", fieldname
            current_shell[fieldname] = parsed_datas
        task_entry['datas'] = parsed_datas
        return task_entry

    def __createShell(self, task_entry):
        datas = task_entry.get('datas')
        # every shell has one data
        subacts = []
        print len(datas), " shells created"
        shellgroup = task_entry.get('group', 'default')
        shellid = 0
        self.shell_groups[shellgroup] = dict({})
        for data in datas:
            shellid += 1
            # init shell
            self.shell_groups[shellgroup][shellid] = dict([])
            # task entry splited into pieces
            # sub actions = now sub * shell num
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
        print "get shell [", shellgroup, ":", shellid, "]"
        return shell