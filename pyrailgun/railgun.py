# coding: UTF-8
# User: princehaku
# Date: 14-5-22
# Time: 4:01
#

__author__ = 'princehaku'

import json
import copy
import sys

from pyrailgun.actions.fetcher import FetcherAction
from pyrailgun.modules.logger import Logger

PY3 = False

if sys.version > '3':
    unicode = str
    PY3 = True


class RailGun:
    def __init__(self):
        self.global_data = {}
        self.shell_groups = {}
        self.orign_task_date = {}
        self.logger = Logger.getLogger()

    # set taskdata into me
    def setTaskData(self, task_data):
        self.task_data = dict(task_data)
        self.orign_task_date = copy.deepcopy(task_data)

    # set taskdata into me via a json file
    def setTask(self, tfile, ext=None):
        if PY3:
            assert tfile.readable(), "taskfile should be an instance file, get" + str(type(tfile))
        else:
            assert isinstance(tfile, file), "taskfile should be an instance file, get" + str(type(tfile))
        if not ext:
            ext = tfile.name.split(".")[-1]
        task_data = json.load(tfile)
        assert task_data, "Task Data is Empty"
        self.task_data = dict(task_data)
        self.orign_task_date = copy.deepcopy(task_data)

    # reset task status
    def resetTask(self):
        self.task_data = copy.deepcopy(self.orign_task_date)

    # set some running global
    def setGlobalData(self, key, value):
        self.global_data[key] = value

    # do work
    def fire(self):
        shell_groups = {}
        self.__parser_shells(self.task_data, shell_groups, self.global_data)
        self.shell_groups = shell_groups
        return shell_groups

    # get parsed shells
    def getShells(self, group_name='default'):
        return self.shell_groups.get(group_name)

    def __parser_shells(self, task_entry, shell_groups, global_data):
        """

        :param task_entry:
        :return:
        """
        if isinstance(task_entry, unicode):
            return
            # do current action
        action_name = task_entry["action"].strip()
        if None != task_entry.get('shellid'):
            self.logger.info("info current shell [" + task_entry.get('shellgroup') + ":" + \
                             str(task_entry.get('shellid')) + "]")

        action_map = {
            'main': "__main"
            , 'shell': '__createShell'
            , 'faketask': '__faketask'
            , 'fetcher': 'FetcherAction'
            , 'parser': 'ParserAction'
        }

        if action_name in action_map.keys():
            # 这里调用本类的函数
            if action_map[action_name][0] == "_":
                worker = getattr(self
                                 , '_RailGun{}'.format(action_map[action_name])
                )
                if callable(worker):
                    task_entry = worker(task_entry, shell_groups)

            # 其他情况采用actions里面定义的类加载
            else:
                module = __import__("pyrailgun.actions." + action_name)
                # getClass
                module = getattr(getattr(getattr(module, "actions"), action_name), action_map[action_name])
                # call Func
                worker = getattr(module, "action")
                task_entry = worker(module(), task_entry, shell_groups, global_data)

        if None == task_entry.get('subaction'):
            return

        for subtask in task_entry['subaction']:
            # if entry is not fakedshell and entry has datas then copy to subtask
            if subtask['action'] != 'faketask' and task_entry.get('datas') is not None:
                subtask['datas'] = task_entry.get('datas')
                # ignore datas field
            if 'datas' == str(subtask):
                continue
                # passed to subtask
            if None != task_entry.get('shellgroup'):
                subtask['shellgroup'] = task_entry.get('shellgroup')
            if None != task_entry.get('shellid'):
                subtask['shellid'] = task_entry.get('shellid')
            self.__parser_shells(subtask, shell_groups, global_data)

        return shell_groups

    def __main(self, task_entry, shell_groups):
        self.logger.info(task_entry['name'] + " is now running")
        return task_entry

    def __faketask(self, task_entry, shell_groups):
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

