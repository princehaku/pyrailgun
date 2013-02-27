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

    # deep.. and deep
    def convertPattern(self, area, resource_str = None):
        if None == self.task_entry.get(area):
            return None
        text = self.task_entry.get(area)
        if resource_str != None:
            text = resource_str
        matched = re.findall(r'\$\{(.*?)\}', text)
        if len(matched) == 0:
            return text
        print "Got Patter", matched[0]
        convetedstrs = []
        if matched[0][0:1] == '#':
            keyname = matched[0][1:]
            assert self.shell != None, "shell can't be empty when using #"
            if self.shell.get(keyname) == None:
                return None
            assert len(self.shell[keyname]) <= 1, " shell 'src length is greater than 1"
            replacedst = ""
            if len(self.shell[keyname]) == 1:
                replacedst = self.shell[keyname][0]
            new_str = re.sub(r'\$\{(.*?)\}', replacedst, text, 1)
            convetedstrs.append(new_str)

        if re.match(r'\d*,\d*', matched[0]):
            assert self.shell == None, "rule " + matched[0] + " can't be set in shells"
            regxp = re.search(r'(\d*),(\d*)', matched[0])
            lower = int(regxp.group(1))
            max = int(regxp.group(2))
            for i in range(lower, max + 1):
                new_str = re.sub(r'\$\{(.*?)\}', str(i), text, 1)
                convetedstrs.append(new_str)
        convetedstrs_new = []
        for s_str in convetedstrs:
            converted_sub = self.convertPattern(area, resource_str=s_str)
            if isinstance(converted_sub, list) :
                for new_str in converted_sub:
                    convetedstrs_new.append(new_str)
            else :
                convetedstrs_new.append(s_str)
        return convetedstrs_new