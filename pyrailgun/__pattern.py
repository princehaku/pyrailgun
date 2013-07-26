#    coding: UTF-8
#    User: haku
#    Date: 13-2-24
#    Time: 上午1:01
#
import re
from __logging import Logger


class Pattern:
    def __init__(self, task_entry=None, shell=None, global_data=None):
        assert (task_entry != None), "task_entry can't be None"
        self.task_entry = task_entry
        self.shell = shell
        self.global_data = global_data
        self.logger = Logger.getLogger()

    # deep.. and deep recursion
    def convertPattern(self, area, resource_str=None):
        """
        :param area: dict
        :param resource_str: string
        :return:
        >>> Pattern({'url':'http://is.me/${0,1}'}).convertPattern('url')  # doctest: +ELLIPSIS
        load logging configure from logging.conf
        [...] (INFO) : Pattern Found as 0,1
        ['http://is.me/0', 'http://is.me/1']
        """

        # specify field required in task_entry
        assert self.task_entry.get(area, None) != None, "specify field required in task_entry"

        text = resource_str \
            if resource_str is not None \
            else self.task_entry.get(area)

        pattern = re.compile(r'\$\{(.*?)\}')

        matched = pattern.findall(text)
        # if doesn't match. just return it
        if not matched:
            return [text]

        self.logger.info("Pattern Found as " + matched[0])

        converted_strings = []
        # support ${#} as shell's Field
        if matched[0].startswith('#'):
            key_name = matched[0][1:]
            assert self.shell != None, "shell can't be empty when using #"
            if self.shell.get(key_name) == None:
                return None
            assert len(self.shell[key_name]) <= 1, " shell 'src length is greater than 1"

            replacedst = self.shell[key_name][0] \
                if len(self.shell[key_name]) == 1 \
                else ""

            converted_strings.append(pattern.sub(replacedst, text, 1))

        # support ${@} as pyrailgun's global data sets
        if matched[0].startswith('@'):
            key_name = matched[0][1:]
            replacedst = self.global_data.get(key_name)
            assert None != replacedst, "config_data " + key_name + " is empty"
            converted_strings.append(pattern.sub(replacedst, text, 1))

        # expand ${n,m} as n,n+1,n+2...m
        if re.match(r'\d*,\d*', matched[0]):
            assert None == self.shell, "rule " + matched[0] + " can't be set in shells"
            regxp = re.search(r'(\d*),(\d*)', matched[0])
            lower = int(regxp.group(1))
            max = int(regxp.group(2))
            for i in range(lower, max + 1):
                if (lower == 0):
                    pass
                replaced_text = format(i, "0" + str(len(regxp.group(1))) + "d")
                new_str = pattern.sub(replaced_text, text, 1)
                converted_strings.append(new_str)

        # recursion
        converted_list = []
        for s_str in converted_strings:
            converted_sub = self.convertPattern(area, resource_str=s_str)
            if not isinstance(converted_sub, list):
                converted_sub = [converted_sub]
            converted_list.extend(converted_sub)
            # if converted_strings is null set the raw input into it
        if not converted_list:
            converted_list.append(text)
        return converted_list