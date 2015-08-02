# coding: utf-8

import re
from fabkit import env, Service, Package


class SimpleBase():
    def __init__(self):
        self.data_key = None
        self.data = {}
        self.services = []
        self.packages = {}

    def init(self):
        self.is_package = False
        self.is_conf = False
        self.is_data = False
        if len(env.args) == 0:
            self.is_package = True
            self.is_conf = True
            self.is_data = True
        if 'package' in env.args:
            self.is_package = True
        if 'conf' in env.args:
            self.is_conf = True
        if 'data' in env.args:
            self.is_data = True

        if not hasattr(self, 'is_init') or self.is_init is not True:
            if not hasattr(self, 'data'):
                self.data = {}
            if hasattr(self, 'data_key') and self.data_key in env.cluster:
                self.data.update(env.cluster[self.data_key])

            node_os = env.node['os']
            if hasattr(self, 'services'):
                if isinstance(self.services, list):
                    self.services = [Service(service) for service in self.services]
                elif isinstance(self.services, dict):
                    services = []
                    for os_pattern, service_names in self.services.items():
                        if re.match(os_pattern, node_os):
                            for service_name in service_names:
                                services.append(Service(service_name))
                            break
                    self.services = services

            if hasattr(self, 'packages'):
                if isinstance(self.packages, list):
                    self.packages = [Package(package) for package in self.packages]
                if isinstance(self.packages, dict):
                    packages = []
                    for os_pattern, package_names in self.packages.items():
                        if re.match(os_pattern, node_os):
                            for package_name in package_names:
                                if isinstance(package_name, str):
                                    packages.append(Package(package_name))
                                if isinstance(package_name, dict):
                                    packages.append(Package(
                                        package_name['name'],
                                        path=package_name['path']
                                    ))
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

    def upgrade_packages(self):
        for package in self.packages:
            package.upgrade()
        return self

    def uninstall_packages(self):
        for package in self.packages:
            package.uninstall()
        return self

    def start_services(self, **kwargs):
        for service in self.services:
            service.start(**kwargs)
        return self

    def stop_services(self, **kwargs):
        for service in self.services:
            service.start(**kwargs)
        return self

    def restart_services(self, **kwargs):
        for service in self.services:
            service.restart(**kwargs)
        return self

    def reload_services(self, **kwargs):
        for service in self.services:
            service.reload(**kwargs)
        return self

    def status_services(self, **kwargs):
        for service in self.services:
            service.reload(**kwargs)
        return self

    def enable_services(self, **kwargs):
        for service in self.services:
            service.enable(**kwargs)
        return self
