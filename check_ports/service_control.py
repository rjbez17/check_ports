from fabric.tasks import execute
from fabric.api import env

from fab_commands import service_command


class ServiceControl(object):

    def __init__(self, username, password, ip):
        env.user = username
        env.password = password
        env.host_string = ip

    def start_service(self, service):
        return service_command(service, 'start')

    def restart_service(self, service):
        return service_command(service, 'restart')

    def get_service_status(self, service):
        return service_command(service, 'status')
