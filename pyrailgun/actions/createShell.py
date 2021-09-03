__author__ = 'haku-mac'


def action(self, task_entry):
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
        # task entry splitted into pieces
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
