# coding: utf-8

import re
from fabkit import env, Service, Package


class SimpleBase():
    def __init__(self):
        self.data_key = None
        self.data = {}
        self.services = []
        self.packages = {}

    def is_tag(self, *tags):
        exec_tags = env.kwargs.get('t')
        if not exec_tags:
            return True

        exec_tags = exec_tags.split('+')

        for t in tags:
            if t in exec_tags:
                return True

        return False

    def init(self):
        if not hasattr(self, 'is_init') or self.is_init is not True:
            self.init_before()

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

            self.is_init = True

        self.init_after()
        return self.data

    def init_before(self):
        pass

    def init_after(self):
        pass

    def install_packages(self):
        self.init()
        for package in self.packages:
            package.install()
        return self

    def upgrade_packages(self):
        self.init()
        for package in self.packages:
            package.upgrade()
        return self

    def uninstall_packages(self):
        self.init()
        for package in self.packages:
            package.uninstall()
        return self

    def start_services(self, **kwargs):
        self.init()
        for service in self.services:
            service.start(**kwargs)
        return self

    def stop_services(self, **kwargs):
        self.init()
        for service in self.services:
            service.start(**kwargs)
        return self

    def restart_services(self, **kwargs):
        self.init()
        for service in self.services:
            service.restart(**kwargs)
        return self

    def reload_services(self, **kwargs):
        self.init()
        for service in self.services:
            service.reload(**kwargs)
        return self

    def status_services(self, **kwargs):
        self.init()
        for service in self.services:
            service.reload(**kwargs)
        return self

    def enable_services(self, **kwargs):
        self.init()
        for service in self.services:
            service.enable(**kwargs)
        return self
