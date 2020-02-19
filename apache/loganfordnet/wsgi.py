from pyramid.paster import get_app, setup_logging
import os

ini_path = '/home/loganfordnet/configuration.ini'
setup_logging(ini_path)
app = get_app(ini_path, 'main')