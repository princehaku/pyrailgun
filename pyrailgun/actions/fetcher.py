

__author__ = 'haku-mac'

import requests

from pyrailgun.actions.action import RailGunAction
from pyrailgun.modules.pattern import Pattern
from pyrailgun.modules import cwebbrowser


class FetcherAction(RailGunAction):

    def action(self, task_entry, shell_groups):
        if task_entry.get("webkit", False):
            return self.__fetch_webkit(task_entry, shell_groups)
        return self.__fetch_requests(task_entry, shell_groups)

    # using webkit to fetch url
    def __fetch_webkit(self, task_entry, shell_groups):
        p = Pattern(task_entry, self.get_current_shell(task_entry, shell_groups))

        task_entry['datas'] = []

        urls = p.convertPattern('url')
        timeout = task_entry.get('timeout', 30)
        delay = task_entry.get('delay', 0)

        for url in urls:
            self.logger.info("fetching " + url)
            data = ""
            if not url:
                # do not fetch null url
                continue
            browser = cwebbrowser.CWebBrowser()
            browser.setHeaders(task_entry.get('headers', []))
            # browser.show()
            try:
                browser.load(url=url, load_timeout=timeout, delay=delay)
            except cwebbrowser.Timeout:
                self.logger.error("fetch " + url + " timeout ")
            except Exception, exception:
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
        p = Pattern(task_entry, self.get_current_shell(task_entry, shell_groups))

        timeout = task_entry.get('timeout', 30)
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
                    self.logger.error("fetch " + url + " failed with code " + str(response.status_code))
                data = response.text
            except:
                self.logger.error("fetch " + url + " failed in sockets")
            task_entry['datas'].append(data)
        return task_entry
