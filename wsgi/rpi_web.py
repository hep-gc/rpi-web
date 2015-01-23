#!/usr/local/bin/python2.7

import os
import sys
sys.stdout = sys.stderr
import cherrypy
import atexit
import threading
import logging
from cherrypy import _cperror
from services.batch import BatchService
from services.softrepo import SoftwareRepository
from services.glint import GlintService
from services.shoal import ShoalService
from services.hdidcc import HdidccService

logger = None

# CherryPy configuration.
# This can be put in a config file.  We will do that later...
conf = {}
conf['global'] = {'environment': 'embedded', 'log.error_file':'/tmp/rpi_web_wsgi_error.log', 'log.access_file':'/tmp/rpi_web_wsgi_access.log', 'tools.sessions.name':'1'}






try:
    logging.debug('Creating request dispatching routes...')
    d = cherrypy.dispatch.RoutesDispatcher()

    conf['/'] = {'request.dispatch': d}

    # Create the handlers.
    batchService = BatchService(d)
    softRepo = SoftwareRepository(d)
    glintService = GlintService(d)
    shoalService = ShoalService(d)
    hdidccService = HdidccService(d)
    






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
            h = logging.FileHandler('/tmp/rpi_web_wsgi.log')
            h.setFormatter(logging.Formatter('%(asctime)s %(thread)d : %(message)s'))
            logger.addHandler(h)
            logging.debug('Log handler added to root logger.')
        cherrypy.tree.mount(None, script_name='/wsgi/', config=conf)
        return cherrypy.tree(environ, start_response)

    logging.info('rpi_web WSGI app started')

except Exception as e:
    logging.exception('Error in rpi_web WSGI app.')
