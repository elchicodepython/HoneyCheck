
from configparser import ConfigParser
import os.path

BASEDIR = os.path.dirname(__file__)

CONFIG_FILE = os.path.join(BASEDIR, 'config.cnf')

config = ConfigParser()
config.read(CONFIG_FILE)