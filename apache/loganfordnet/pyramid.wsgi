from pyramid.paster import get_app, setup_logging
import os

#Launch app
ini_path = '/home/retro/loganfordnet/configuration.ini'
setup_logging(ini_path)
application = get_app(ini_path, 'main')
