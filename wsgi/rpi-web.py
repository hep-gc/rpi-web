#!/usr/local/bin/python2.7

import os
import sys
sys.stdout = sys.stderr
import cherrypy
import atexit
import threading
import logging
from cherrypy import _cperror

logger = None

# CherryPy configuration.
# This can be put in a config file.  We will do that later...
conf = {}
conf['global'] = {'environment': 'embedded', 'log.error_file':'/tmp/rpi-web-wsgi-error.log', 'log.access_file':'/tmp/rpi-web-wsgi-access.log', 'tools.sessions.name':'1'}

# The root CherryPy handler.
# It does nothing more than act as a parent
# for all handlers.
class Root():
    def test(self):
        return 'Test OK'





try:
    root = Root()


    logging.debug('Creating request dispatching routes...')
    d = cherrypy.dispatch.RoutesDispatcher()
    m = d.mapper


    conf['/'] = {'request.dispatch': d}

    d.connect('test', '/test', controller = root, action = 'test')

    def application(environ, start_response):
        #
        # Setup logging.
        # Do only once, else we might end up with multiple loggers that all do
        # the same thing.
        #
        global logger
        if not logger:
            logger = logging.getLogger()
            logger.setLevel(logging.DEBUG)
            h = logging.FileHandler('/tmp/rpi-web-wsgi.log')
            h.setFormatter(logging.Formatter('%(asctime)s %(thread)d : %(message)s'))
            logger.addHandler(h)
            logging.debug('Log handler added to root logger.')
        cherrypy.tree.mount(None, script_name='/wsgi/', config=conf)
        return cherrypy.tree(environ, start_response)

    logging.info('rpi-web WSGI  app started')

except Exception as e:
    logging.exception('Error in rpi-web WSGI app.')
