import logging
import datetime
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler

import cloudscheduler.__version__ as version



# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Create server
server = SimpleXMLRPCServer(("condor.heprc.uvic.ca", 8000),
                            requestHandler=RequestHandler)
server.register_introspection_functions()


# Register an instance; all the methods of the instance are
# published as XML-RPC methods (in this case, just 'div').
class ExternalFunctions():
    def ping(self):
        """
        Simple test method to check if the info server is up.
        Might sound redundant, but makes client code more explicit.
        """
        return 'OK'

    def get_version(self):
        """
        Returns the version of the currently installed Cloud Scheduler libraries.
        """
        return version.version

    def get_release_time(self):
        """
        Returns the release time of the currently installed Cloud Scheduler libraries,
        in ISO 8601 format (YYYY-MM-DDTHH:MM:SS.mmmmmm or, if microsecond is 0, YYYY-MM-DDTHH:MM:SS).
        """
        return '%s' % datetime.datetime.now().isoformat()

    def get_number_of_invocations(self):
        """
        Returns the number of time the Cloud Scheduler server was 'invoked', along with the timestamp
        at which this number was last reset.
        We define a Cloud Scheduler invocation as being the Cloud Scheduler accepting a new job submission.
        This method
        The format of the returned value is:
        <count>;<timestamp>
        The timestamp is in UTC and formatted in ISO 8601 format (YYYY-MM-DDTHH:MM:SS.mmmmmm or, if microsecond is 0, YYYY-MM-DDTHH:MM:SS)
        """
        return '0;%s' % (datetime.datetime.now().isoformat())



server.register_instance(ExternalFunctions())

# Run the server's main loop
logging.debug('Starting xmlrpc server loop ...')
server.serve_forever()
