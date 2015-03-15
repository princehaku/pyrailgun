from pyrailgun.modules.logger import Logger

__author__ = 'haku-mac'

class RailGunAction:

    def __init__(self):
        self.logger = Logger.getLogger()
        pass

    @staticmethod
    def get_current_shell(task_entry, shell_groups):
        if None == task_entry.get('shellgroup'):
            return None
        shellgroup = task_entry['shellgroup']
        if None == shell_groups.get(shellgroup):
            return None
        shellid = task_entry['shellid']
        shell = shell_groups[shellgroup][shellid]
        return shell