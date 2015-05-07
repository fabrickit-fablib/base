# coding: utf-8


from fabkit import env, Service, Package


class SimpleBase():
    def __init__(self):
        self.key = 'base'
        self.data = {}
        self.services = []
        self.packages = []

    def get_init_data(self):
        if not hasattr(self, 'is_init') or self.is_init is not True:
            if self.data_key in env.cluster:
                self.data.update(env.cluster[self.data_key])

            if hasattr(self, 'services'):
                services = []
                for service in self.services:
                    services.append(Service(service))
                self.services = services

            if hasattr(self, 'packages'):
                packages = []
                for package in self.packages:
                    packages.append(Package(package))
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
