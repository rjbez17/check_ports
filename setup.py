try:
    import ez_setup
    ez_setup.use_setuptools()
except ImportError:
    pass

from setuptools import setup

required = ['fabric']
packages = ['check_ports']

setup(
        name                 = 'check_ports',
        version              = '0.0.1',
        description          = 'Start services on a remote server if port is closed',
        author               = 'Ryan Bezdicek',
        author_email         = 'ryanjbezdicek@gmail.com',
        packages             = packages,
        include_package_data = True,
        install_requires     = required,
)
