# coding: utf-8

import re
from fabkit import env, Service, Package


class SimpleBase():
    def __init__(self):
        self.key = 'base'
        self.data = {}
        self.services = []
        self.packages = {}

    def get_init_data(self):
        if not hasattr(self, 'is_init') or self.is_init is not True:
            if self.data_key in env.cluster:
                self.data.update(env.cluster[self.data_key])
              
            node_os = env.node['os']
            if hasattr(self, 'services'):
                services = []
                for os_pattern, service_names in self.services.items():
                    if re.match(os_pattern, node_os):
                        for service_name in service_names:
                            services.append(Service(service_name))
                        break
                self.services = services

            if hasattr(self, 'packages'):
                packages = []
                for os_pattern, package_names in self.packages.items():
                    if re.match(os_pattern, node_os):
                        for package_name in package_names:
                            packages.append(Package(package_name))
                        break
                self.packages = packages

            self.init_data()
            self.is_init = True

        return self.data

    def init_data(self):
        self.data.update({})

    def install_packages(self):
        for package in self.packages:
            package.install()
        return self

    def restart_services(self, **kwargs):
        for service in self.services:
            service.restart(**kwargs)
        return self

    def start_services(self, **kwargs):
        for service in self.services:
            service.start(**kwargs)
        return self

    def enable_services(self, **kwargs):
        for service in self.services:
            service.enable(**kwargs)
        return self
