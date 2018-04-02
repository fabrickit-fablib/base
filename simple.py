# coding: utf-8

import re
from fabkit import env, sudo, Service, Package


class SimpleBase():
    def __init__(self):
        self.data_key = None
        self.data = {}
        self.services = []
        self.packages = {}
        self.node_services = []
        self.node_packages = {}
        self.handlers = {}

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

            if not hasattr(self, 'handlers'):
                self.handlers = {}

            if not hasattr(self, 'exec_handlers'):
                self.exec_handlers = {}

            self.update_services()
            self.update_packages()

            self.is_init = True

            self.init_after()

        return self.data

    def update_services(self):
        node_os = env.node['os']

        if hasattr(self, 'services'):
            if isinstance(self.services, list):
                node_services = []
                for service_name in self.services:
                    service = Service(service_name)
                    node_services.append(service)
                    key = 'restart_{0}'.format(service_name)
                    self.handlers[key] = False

                self.node_services = node_services

            elif isinstance(self.services, dict):
                node_services = []
                for os_pattern, service_names in self.services.items():
                    if re.match(os_pattern, node_os):
                        for service_name in service_names:
                            service = Service(service_name)
                            node_services.append(service)
                            key = 'restart_{0}'.format(service_name)
                            self.handlers[key] = False
                        break
                self.node_services = node_services

    def update_packages(self):
        node_os = env.node['os']

        if hasattr(self, 'packages'):
            if isinstance(self.packages, list):
                self.node_packages = [Package(package) for package in self.packages]
            if isinstance(self.packages, dict):
                node_packages = []
                for os_pattern, package_names in self.packages.items():
                    if re.match(os_pattern, node_os):
                        for package_name in package_names:
                            if isinstance(package_name, str):
                                node_packages.append(Package(package_name))
                            if isinstance(package_name, dict):
                                node_packages.append(Package(
                                    package_name['name'],
                                    path=package_name['path']
                                ))
                        break
                self.node_packages = node_packages

    def init_before(self):
        pass

    def init_after(self):
        pass

    def init_package_manager(self):
        if env.node['package_manager'] == 'apt':
            sudo('apt update')
        elif env.node['package_manager'] == 'yum':
            sudo('yum clean all')

    def install_packages(self, option=''):
        self.init()
        for package in self.node_packages:
            package.install(option)
        return self

    def upgrade_packages(self):
        self.init()
        for package in self.node_packages:
            package.upgrade()
        return self

    def uninstall_packages(self):
        self.init()
        for package in self.node_packages:
            package.uninstall()
        return self

    def start_services(self, **kwargs):
        self.init()
        for service in self.node_services:
            service.start(**kwargs)
        return self

    def stop_services(self, **kwargs):
        self.init()
        for service in self.node_services:
            service.start(**kwargs)
        return self

    def restart_services(self, **kwargs):
        self.init()
        for service in self.node_services:
            service.restart(**kwargs)
        return self

    def reload_services(self, **kwargs):
        self.init()
        for service in self.node_services:
            service.reload(**kwargs)
        return self

    def status_services(self, **kwargs):
        self.init()
        for service in self.node_services:
            service.reload(**kwargs)
        return self

    def enable_services(self, **kwargs):
        self.init()
        for service in self.node_services:
            service.enable(**kwargs)
        return self

    def exec_handlers(self):
        for handler, enable in self.handlers.items():
            if enable:
                action, target = handler.split('_')
                if action == 'restart':
                    if target == 'all':
                        self.restart_services()
                    else:
                        for service in self.node_services:
                            if re.match(target, service.name):
                                service.restart()
