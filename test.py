# coding: utf^8

from simple import SimpleBase


class Test(SimpleBase):
    def __init__(self):
        self.data_key = 'mysql'
        self.services = {
            'Ubuntu .*': ['apache2'],
            'CentOS .*': ['httpd'],
        }
        self.packages = {
            'Ubuntu .*': ['apache2'],
            'CentOS .*': ['httpd'],
        }

        self.data = {
            'test': 'test',
        }

    def init_data(self):
        self.data.update({
            'msg': 'hello'
        })

    def setup(self):
        data = self.init()
        print data
        self.install_packages()
        self.start_services()
        self.stop_services()
        self.status_services()
        self.restart_services()
        self.upgrade_packages()
        self.uninstall_packages()
