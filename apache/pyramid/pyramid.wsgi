from pyramid.paster import get_app, setup_logging
import os

#Load configurations
environment_variables = '/home/retro/loganfordnet/environments/prod'

with open(environment_variables) as f:
    for line in f:
        tokens = line.split()
        if len(tokens) == 2:
            os.environ[tokens[0]] = tokens[1]

#Launch app
ini_path = '/home/retro/loganfordnet/production.ini'
setup_logging(ini_path)
application = get_app(ini_path, 'main')
