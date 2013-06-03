import os
import cherrypy
import datetime
import json
import logging
import ConfigParser
from utils import HtmlUtils




class RpiService():
    """
    An abstract base class for all services.

    This base class will implement the required RPI REST API as
    specified by CANARIE.  Where it needs to needs to fetch dynamic
    data from the services, it will do so via a web service protocol
    (i.e., xmlrpm), and then format the data according to the RPI API
    specs and return the results to the caller.  This abstraction
    layer means that the services themselves do not need to know
    anything about the RPI API specs and can return the data using any
    formatting they want.

    This class also implements a configuration framework, allowing
    each child of this class to have a configuration section in the
    app configuration file.
    """

    def __init__(self, d):
        # Load configuration file
        self._config = ConfigParser.ConfigParser()
        configFile = os.path.expanduser('/etc/canarie-rpi/rpi-api.cfg')
        if os.path.exists(configFile):
            self._config.readfp(open(configFile))
        else:
            logging.info('%s configuration file does not exist.  Using defaults.' % (configFile))

        self._connectRoutes(d)


    def _getConfigSection(self):
        return self.__class__.__name__

    def _getFromConfig(self, option, default = None):
        if self._config.has_option(self._getConfigSection(), option):
            return self._config.get(self._getConfigSection(), option)
        else:
            return default

    def _connectRoutes(self, d):
        """
        Call this method to register the URL routes.
        This method will register the following URIs:
        
          <base>/service/info
          <base>/service/stats
          <base>/service/doc
          <base>/service/releasenotes
          <base>/service/support
          <base>/service/source
          <base>/service/tryme

        """
        d.connect(self.__class__.__name__ + '-info', 
                  '/%s/service/info' % (self._getUrlBase()), controller = self, action = 'info')
        d.connect(self.__class__.__name__ + '-stats', 
                  '/%s/service/stats' % (self._getUrlBase()), controller = self, action = 'stats')
        d.connect(self.__class__.__name__ + '-doc', 
                  '/%s/service/doc' % (self._getUrlBase()), controller = self, action = 'doc')
        d.connect(self.__class__.__name__ + '-releasenotes', 
                  '/%s/service/releasenotes' % (self._getUrlBase()), controller = self, action = 'releasenotes')
        d.connect(self.__class__.__name__ + '-support', 
                  '/%s/service/support' % (self._getUrlBase()), controller = self, action = 'support')
        d.connect(self.__class__.__name__ + '-source', 
                  '/%s/service/source' % (self._getUrlBase()), controller = self, action = 'source')
        d.connect(self.__class__.__name__ + '-tryme', 
                  '/%s/service/tryme' % (self._getUrlBase()), controller = self, action = 'tryme')


    def _getUrlBase(self):
        return self._getFromConfig('url_base', self.getName().lower())

        
    def _getXmlRpcServer(self):
        return self._getFromConfig('xmlrpc_server')

    def _processReturnValue(self, s):
        """
        This method will parse the return value and act on specific
        keywords found in the return value:

        - If s starts with a 'REDIRECT:' keyword, then the text on the left of
        the keyword will be put into a HTTP redirect response.
        """
        if s.find('REDIRECT:') == 0:
            raise cherrypy.HTTPRedirect(s.split(':', 1)[1])
        else:
            return s


    def _should_return_json(self):
        """
        This method will look at the Accept header to check if we should
        return JSON or not.
        """
        return cherrypy.request.headers['Accept'].lower() == "application/json"






    #
    # URL routes handlers.
    # The following route handlers will be called when specific URLs are visited.
    # These methods will call the subclass's methods to get the information and then
    # format it properly (i.e., json or html) before returning it to the caller.
    #

    def info(self):
        """
        Return basic identification and provenance information about
        the service. CANARIE's monitoring service will poll this URI
        periodically.

        When an HTTP GET is performed on this URI, and the Accept
        header specifies json (ie. application/json) please return the
        following:

        {
	"name" : "<name of service>",
	"synopsis": "<one or two sentences describing what the service is for>",
	"version" : "<service version identifier>",
	"institution": "<the name of the institution responsible for the service>",
	"releaseTime": <time at which this version of the service was published>"
        }

        where:
        The value of "version" will be taken as a string and can
        follow any versioning scheme you deem appropriate.
 
        The value of "dt" is in the format ddd mmm dd yyyy
        HH:MM:ss (example Sat Jun 09 2007 17:46:21). Please express in
        UTC rather than local time.

        If an HTTP GET is performed and the Accept header does not
        indicate json, or there is no Accept header, please return an
        HTML page providing the information listed above in
        human-readable format.
        """

        d = {}
        d['name'] = self.getName()
        d['synopsis'] = self.getSynopsis()
        d['version'] = self.getVersion()
        d['institution'] = self.getInstitution()
        d['releaseTime'] = str(self.getReleaseTime())

        if self._should_return_json():
            cherrypy.response.headers['Content-Type'] = "application/json"
            return json.dumps(d)
        else:
            return HtmlUtils().dictToPage(d)


    def stats(self):
        """
        Return information about the usage of your RPI. CANARIE's
        monitoring service will poll this URI periodically. If a
        request to this URI fails or times out, the monitoring service
        will flag your RPI as unavailable. With this in mind, please
        endeavor to architect your RPI such that that requests to this
        URI will fail if the rest of the service is not available.
 
        When an HTTP Get is performed on this URI, and the Accept
        header specifies json (ie. application/json) please return the
        following:

        {
	"invocations" : "<number of times service has been used since last reset>",
	"lastReset": "<the time and date at which invocations was last reset to zero>",
        }

        where:
        The value of "invocations" is a positive integer. This value
        should start at zero when the service is first published and
        should be incremented every time the service's API (excluding
        anything under <base>/service) is accessed.  The value of
        "lastReset" is in the format ddd mmm dd yyyy HH:MM:ss (example
        Sat Jun 09 2007 17:46:21). Please express in UTC rather than
        local time. If you reset your invocations value to zero or it
        wraps around, please update this value accordingly.
        """
        d = {}
        d['invocations'] = self.getInvocations()
        d['lastReset'] = str(self.getLastReset())
        if self._should_return_json():
            cherrypy.response.headers['Content-Type'] = "application/json"
            return json.dumps(d)
        else:
            return HtmlUtils().dictToPage(d)
        

    def doc(self):
        """
        Make the online documentation for your service available.

        When an HTTP GET is performed, return the user documentation
        for your service in a human-readable format. This information
        should include:

        A detailed description of the service and what it does

        A complete description of the API

        Sample code illustrating API usage, as appropriate

        If the documentation is hosted elsewhere, returning an HTTP
        redirect in response to this request is acceptable.
        """
        return self._processReturnValue(self.getDoc())


    def releasenotes(self):
        """
        Return release notes describing the current version of your
        service.

        When an HTTP GET is performed, return the release notes for
        the current version of your service. These notes should
        identify changes made from previous versions as well as any
        know issues with work-arounds (where applicable). If the
        release notes are hosted elsewhere, please return an HTTP
        redirect in response to this request.
        """
        return self._processReturnValue(self.getReleaseNotes())


    def support(self):
        """
        Provide users with information on how to get support for your
        RPI.

        When an HTTP GET is performed, return instructions for users
        on how to get support for your service, in human-readable
        format. Include help desk contact info, a link to any bug
        tracking systems and/or forums, etc.
        """
        return self._processReturnValue(self.getSupport())


    def source(self):
        """
        When an HTTP GET is performed, return link(s) to the source
        code for you service. This is only applicable if you are
        making your source code publicly available. If the source code
        is hosted elsewhere, please return and HTTP redirect in
        response to this request. If you are not providing access to
        your service's source code, please return status code 204 (No
        Content).
        """
        return self._processReturnValue(self.getSource())


    def tryme(self):
        """
        Allow users to try out your RPI online.

        This URI returns a page that allows the user to try your
        service, possibly with fixed input. Consider displaying the
        text of the HTTP request and response for reference
        purposes. If you are not providing this capability, please
        return status code 204 (No Content).
        """
        return self._processReturnValue(self.getTryMe())












    #
    # The following abstract methods can be overriden in
    # each RPI service subclasses.
    # These are defined in the "RPI API Enhancements for CANARIE 
    # Service Registry and Monitoring System" document.
    # The default implementation will try to read the value from
    # the /etc/canarie-rpi/rpi-api.cfg configuration file.
    #

    def getName(self):
        return self._getFromConfig('name', self.__class__.__name__)

    def getSynopsis(self):
        return self._getFromConfig('synopsis', '')

    def getVersion(self):
        return self._getFromConfig('version', '')

    def getInstitution(self):
        return self._getFromConfig('institution', '')

    def getReleaseTime(self):
        return self._getFromConfig('release_time')

    def getInvocations(self):
        return self._getFromConfig('invocations', '')

    def getLastReset(self):
        return self._getFromConfig('last_reset')

    def getDoc(self):
        return self._getFromConfig('documentation', '')

    def getReleaseNotes(self):
        return self._getFromConfig('release_notes', '')

    def getSupport(self):
        return self._getFromConfig('support', '')

    def getSource(self):
        # Defaults to 'No Content' if not implemented in subclass.
        source = self._getFromConfig('source')
        if source == None:
            cherrypy.response.status = 204
        else:
            return source
        
    def getTryMe(self):
        # Defaults to 'No Content' if not implemented in subclass.
        tryme = self._getFromConfig('tryme')
        if tryme == None:
            cherrypy.response.status = 204
        else:
            return tryme
        


