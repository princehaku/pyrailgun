from pyrailgun.modules.logger import Logger

__author__ = 'princehaku'

class RailGunAction:

    def __init__(self):
        self.logger = Logger.getLogger()
        pass

    @staticmethod
    def get_current_shell(task_entry, shell_groups):
        if None == task_entry.get('shellgroup'):
            return None
        shell_group = task_entry['shellgroup']
        if None == shell_groups.get(shell_group):
            return None
        shell_id = task_entry['shellid']
        shell = shell_groups[shell_group][shell_id]
        return shell
