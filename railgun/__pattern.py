#    coding: UTF-8
#    User: haku
#    Date: 13-2-24
#    Time: 上午1:01
#
import re
import copy

class Pattern:
    def __init__(self, task_entry=None, shell=None):
        assert (task_entry != None), "task_entry can't be None"
        self.task_entry = task_entry
        self.shell = shell
        self.convetedstrs = []

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
            new_str = re.sub(r'\$\{(.*?)\}', self.shell[keyname][0], text, 1)
            self.convetedstrs.append(new_str)

        if re.match(r'\d*,\d*', matched[0]):
            assert self.shell == None, "shell can't be setted before this time"
            regxp = re.search(r'(\d*),(\d*)', matched[0])
            lower = int(regxp.group(1))
            max = int(regxp.group(2))
            for i in range(lower, max+1) :
                new_str = re.sub(r'\$\{(.*?)\}', str(i), text, 1)
                self.convetedstrs.append(new_str)
        return True

    def getConvertdStr(self):
        return self.convetedstrs