#!/usr/bin/env python3

'''
HoneyCheck Fase ALFA

Version 0.1

Autor: Samuel López ~ @elchicodepython

Esta aplicación se ha desarrollado para ser incluida en un artículo del blog de HoneySEC

https://honeysec.blogspot.com.es

Estoy totalmente seguro de que hay mil formas de hacer mucho mejor determinadas soluciones
dadas a problemas que me he encontrado durante el desarrollo y he resuelto como he podido.

No conozco apenas gente que desarrolle en Python en mis círculos cercanos así que...
Si quieres aportar o cambiar algo en la misma siénte cómodo de hacerlo.

Me queda mucho por aprender y toda aportación es invaluable.

Agradecimientos a Julián: @txambe y a Robledo: @jantoniorobledo por su invalorable ayuda y ánimos en el
desarrollo de esta aplicación.

'''


from threading import Thread
from config import config, CONFIG_FILE
from dhcp_watchmen import DHCPWatchmen



import logging.handlers
import sys
import os.path
import Actions

LOG_LEVEL = logging.DEBUG

# logging.basicConfig(level = LOG_LEVEL)

logger = logging.getLogger('elchicodepython.honeycheck')
logger.setLevel(LOG_LEVEL)

ch = logging.StreamHandler()
ch.setLevel(LOG_LEVEL)
formatter = logging.Formatter(fmt = '%(asctime)s - %(levelname)s - HoneyCheck %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def get_control_objects(iface, name):
    '''
    :param iface:
    :param name:
    :return: list of objects inherited from honeycheckModule
    :rtype list
    '''

    control_objects_str = [co.strip() for co in config[iface][name].split(',')]
    control_objects = []

    for control_object in control_objects_str:
        # Recursive search of control objects inside Actions in order to find and create the object
        # and the corresponding method defined in the configuration
        actual = Actions
        for part in control_object.split('.'):
            parent = actual
            actual = getattr(actual, part)

        control_object = parent(iface, name) # Instance of the Control Object
        if control_object.check_dependencies():
            if control_object.check_requirements():
                # actual = method of the control object to be executed
                control_objects.append((control_object, actual))
            else:
                logger.critical('Requirements ' + str(control_object.config_requirements) +' check failed in ' +
                                control_object.__class__.__name__)
                return []
        else:
            logger.critical('Dependencies check failed in module ' + control_object.__class__.__name__)
            return []


    return control_objects



# If HoneyCHECK is not configured exit
if len(config.sections()) == 0:
    logger.error('Debes configurar honeycheck antes de usarlo\n'
          'Puedes encontrar documentación en http://honeycheck.curiosoinformatico.com')

    sys.exit(1)


def start_the_party():
    ifaces = config.sections()

    if len(ifaces) == 0:
        logger.critical('Fail to check the configuration file in ' + os.path.abspath(CONFIG_FILE))
        sys.exit(2)

    for iface in ifaces:
        logger.info(iface + ': FOUND IN ' + CONFIG_FILE)
        try:
            timeout = int(config[iface]['discover_timeout'])
            logger.info('Stablished timeout = %s seconds' % timeout)
        except KeyError:
            timeout = 10
            logger.info('Stablished timeout = 10 for sending DHCP DISCOVER packets as DEFAULT')

        whitelist = [] if 'whitelist' not in config[iface] else [ip.strip() for ip in config[iface]['whitelist'].split(',')]

        fail_objects = [] if 'fail_test' not in config[iface] else get_control_objects(iface, 'fail_test')
        pass_objects = [] if 'pass_test' not in config[iface] else get_control_objects(iface, 'pass_test')
        final_objects = [] if 'final_exec' not in config[iface] else get_control_objects(iface, 'final_exec')

        watchmen = DHCPWatchmen(iface, fail_objects, pass_objects, final_objects, whitelist)
        Thread(target = watchmen.sniff_dhcp).start()
        Thread(target  = watchmen.dhcp_discovery_daemon, args = (timeout,)).start()


if __name__ == '__main__':
    start_the_party()
