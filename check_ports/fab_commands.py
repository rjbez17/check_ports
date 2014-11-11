from fabric.api import sudo, task, settings


@task
def service_command(service, command="status"):
    with settings(warn_only=True):
        return sudo('service %s %s' % (service, command))
