#    coding: UTF-8
#    User: haku
#    Date: 13-2-24
#    Time: 上午1:01
#
import re


class Pattern:
    def __init__(self, task_entry=None, shell=None):
        assert (task_entry != None), "task_entry can't be None"
        self.task_entry = task_entry
        self.shell = shell
        self.convertedshells = []

    def convertPattern(self, area):
        if None == self.task_entry.get(area):
            return False
        text = self.task_entry.get(area)
        matched = re.findall(r'\$\{(.*?)\}', text)
        if len(matched) == 0:
            return False
        print "Got Patter", matched[0]
        if matched[0][0:1] == '#':
            keyname = matched[0][1:]
            assert self.shell != None, "shell can't be empty when using #"
            if self.shell.get(keyname) == None:
                return False
            assert len(self.shell[keyname]) == 1, " shell'src is not a single value"
            self.task_entry[area] = re.sub(r'\$\{(.*?)\}', self.shell[keyname][0], text, 1)
            self.convertedshells.append(self.task_entry)
            


    def getConvertdShells(self):
        return self.convertedshells

    def __fakeShell(self):
        return self.task_entry
