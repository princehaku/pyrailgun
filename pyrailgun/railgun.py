# coding: UTF-8
# User: haku
# Date: 14-5-22
#    Time: 4:01
#

__author__ = 'haku-mac'

import re
import json
import sys

import requests
from bs4 import BeautifulSoup

from pattern import Pattern
from logger import Logger


class RailGun:
    def __init__(self):
        self.global_data = {}
        self.shell_groups = {}
        self.logger = Logger.getLogger()

    # set taskdata into me
    def setTaskData(self, task_data):
        self.task_data = dict(task_data)

    # set taskdata into me via a yaml file
    def setTask(self, tfile, ext=None):
        assert isinstance(tfile, file), "taskfile should be an instance file, get" + str(type(tfile))
        if not ext:
            ext = tfile.name.split(".")[-1]
        task_data = json.load(tfile)
        assert task_data, "Task Data is Empty"
        self.task_data = dict(task_data)

    # set some running global
    def setGlobalData(self, key, value):
        self.global_data[key] = value

    # do work
    def fire(self):
        shell_groups = {}
        self.__parserShells(self.task_data, shell_groups)
        self.shell_groups = shell_groups
        return shell_groups

    # get parsed shells
    def getShells(self, group_name='default'):
        return self.shell_groups.get(group_name)

    def __parserShells(self, task_entry, shell_groups):
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

        actionMap = {
            'main': "__main"
            , 'shell': '__createShell'
            , 'faketask': '__faketask'
            , 'fetcher': '__fetch'
            , 'parser': 'ParserAction'
        }

        if actionname in actionMap.keys():
            if (actionMap[actionname][0] == "_"):
                worker = getattr(self
                                 , '_RailGun{}'.format(actionMap[actionname])
                )
                if callable(worker):
                    task_entry = worker(task_entry, shell_groups)
            else:
                from pyrailgun.actions.parseraction import ParserAction
                module = ParserAction
                worker = getattr(module
                                 ,"action")
                task_entry = worker(module(), task_entry, shell_groups)

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
            self.__parserShells(subtask, shell_groups)

        return shell_groups

    def __main(self, task_entry, shell_groups):
        self.logger.info(task_entry['name'] + " is now running")
        return task_entry

    # using webkit to fetch url
    def __fetch_webkit(self, task_entry, shell_groups):
        p = Pattern(task_entry, self.__getCurrentShell(task_entry, shell_groups), self.global_data)

        import cwebbrowser

        task_entry['datas'] = []

        urls = p.convertPattern('url')
        timeout = task_entry.get('timeout', 120)
        delay = task_entry.get('delay', 0)

        for url in urls:
            self.logger.info("fetching " + url)
            data = ""
            if not url:
                # do not fetch null url
                continue
            browser = cwebbrowser.CWebBrowser()
            browser.setHeaders(task_entry.get('headers', []))
            #browser.show();
            try:
                browser.load(url=url, load_timeout=timeout, delay=delay)
            except cwebbrowser.Timeout:
                self.logger.error("fetch " + url + " timeout ")
            except  Exception, exception:
                self.logger.error("fetch " + url + " error ")
                print "Exception message:", exception

            else:
                html = browser.html()
                if html:
                    html = html.encode('utf-8')
                    data = html
                else:
                    self.logger.error("fetch " + url + " failed with no response")
            task_entry['datas'].append(data)

            browser.close()
        return task_entry

    def __fetch_requests(self, task_entry, shell_groups):
        p = Pattern(task_entry, self.__getCurrentShell(task_entry, shell_groups), self.global_data)

        timeout = task_entry.get('timeout', 120)
        urls = p.convertPattern('url')
        s = requests.session()
        headers = task_entry.get('headers', [])
        task_entry['datas'] = []
        if not urls:
            return task_entry
        for url in urls:
            self.logger.info("fetching " + url)
            data = ""
            if not url:
                # do not fetch null url
                continue
            try:
                response = s.get(url, timeout=timeout, headers=headers)
                if 200 != response.status_code:
                    self.logger.error("fetch " + url + " failed with code " + (str)(response.status_code))
                data = response.text
            except:
                self.logger.error("fetch " + url + " failed in sockets")
            task_entry['datas'].append(data)
        return task_entry

    # fetch something
    def __fetch(self, task_entry, shell_groups):

        if task_entry.get("webkit", False):
            return self.__fetch_webkit(task_entry, shell_groups)
        return self.__fetch_requests(task_entry, shell_groups)

    def __faketask(self, task_entry, shell_groups):
        return task_entry

    # parse with soup
    def __parser(self, task_entry, shell_groups):
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
        current_shell = self.__getCurrentShell(task_entry, shell_groups)
        if current_shell != None and task_entry.get('setField') != None and len(parsed_datas) > 0:
            fieldname = task_entry.get('setField')
            self.logger.debug("set" + fieldname + "as" + str(parsed_datas));
            current_shell[fieldname] = parsed_datas
        task_entry['datas'] = parsed_datas
        return task_entry

    def __createShell(self, task_entry, shell_groups):
        datas = task_entry.get('datas')
        # every shell has only one data
        subacts = []
        self.logger.info(str(len(datas)) + " shells created")
        shellgroup = task_entry.get('group', 'default')
        shellid = 0
        shell_groups[shellgroup] = {}
        for data in datas:
            shellid += 1
            # init shell
            shell_groups[shellgroup][shellid] = {}
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

    def __getCurrentShell(self, task_entry, shell_groups):
        if (None == task_entry.get('shellgroup')):
            return None
        shellgroup = task_entry['shellgroup']
        if None == shell_groups.get(shellgroup):
            return None
        shellid = task_entry['shellid']
        shell = shell_groups[shellgroup][shellid]
        return shell
