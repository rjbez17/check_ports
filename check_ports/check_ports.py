#!/usr/bin/env python
import socket
import logging
from time import sleep
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from getpass import getpass

from service_control import ServiceControl

def get_parser():
    parser = ArgumentParser(description="Check remote ports", 
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('--ip', metavar="127.0.0.1", required=True,
                        default="127.0.0.1",
                        help='The IP address of the service to check')
    parser.add_argument('--username', required=True)
    parser.add_argument('--password', default='')
    parser.add_argument('-p', action='store_true', dest='prompt',
                        help='Prompt for the users password')
    parser.add_argument('--service', nargs=2, required=True, action='append',
                        help="Expects a port and service pair to be checked." \
                             " You can pass in multiple pairs",
                             metavar=("PORT", "SERVICE") )
    parser.add_argument('--log', default=".", help="Relative path to save logs")
    return parser


def get_logger(name, path):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    sh = logging.StreamHandler()
    fh = logging.FileHandler('%s/%s.log' % (path, name))
    fmt = '%(asctime)s - %(name)s - %(levelname)s: %(message)s'
    formatter = logging.Formatter(fmt)
    sh.setFormatter(formatter)
    fh.setFormatter(formatter)
    logger.addHandler(sh)
    logger.addHandler(fh)
    return logger


def get_args():
    args = get_parser().parse_args()
    if args.prompt and args.password == '':
        args.password = getpass()
    return args


def check_port_status(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return True if sock.connect_ex((ip, port)) == 0 else False


def check_output(string, words):
    return False if any(word in words for word in string.split()) else True


def start_service(service, verify=False):
    error_words = ['not', 'unrecognized']
    log.info("Checking if service is already running")
    if check_output(sc.get_service_status(service), error_words):
        log.info('%s service was not running, starting it' % service)
        log.info(sc.start_service(service))
    else:
        log.info("Attempting to restart %s service" % service)
        log.info(sc.restart_service(service))
    if verify:
        log.info("Sleeping for 5 seconds then verify service is started")
        sleep(5)
        return check_output(sc.get_service_status(service), error_words)
    return True


if __name__ == "__main__":
    args = get_args()
    log = get_logger(__file__.split('.')[0], args.log)
    to_start = []
    for service in args.service:
        port = int(service[0])
        service_name = service[1]
        if not check_port_status(args.ip, port):
            to_start.append({'port': port, 'service': service_name})
        else:
            log.info("Service %s is currently running" % service_name)
    if len(to_start) > 0:
        sc = ServiceControl(args.username, args.password, args.ip)
        log.info("Some ports were not open, attempting to start their services")
        for service in to_start:
            if start_service(service['service'], verify=True):
                log.info("Succesfully started %s service" % service['service'])
            else:
                log.info("Unable to start %s service" % service['service'])
    else:
        log.info("All ports are currently open, no need to start any services.")
    log.info('done.')
    
