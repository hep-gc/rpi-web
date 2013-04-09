import cherrypy
import datetime
import json
import logging
from utils import HtmlUtils

class RpiService():
    """
    An abstract base class for all services.
    """

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
        acceptHeader = cherrypy.lib.cptools.accept()
        logging.debug('Accept header: %s' % (acceptHeader))

        d = {}
        d['name'] = self.getName()
        d['synopsis'] = self.getSynopsis()
        d['version'] = self.getVersion()
        d['institution'] = self.getInstitution()
        dt = self.getReleaseTime()
        if (dt.tzinfo != None) and (dt.utcoffset() != None):
            dt = dt.astimezone(pytz.utc)
        d['releaseTime'] = dt.strftime('%a %b %d %Y %H:%M:%S')

        if acceptHeader == 'application/json':
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
        acceptHeader = cherrypy.lib.cptools.accept()
        d = {}
        d['invocations'] = str(self.getInvocations())
        dt = self.getLastReset()
        if (dt.tzinfo != None) and (dt.utcoffset() != None):
            dt = dt.astimezone(pytz.utc)
        d['lastReset'] = dt.strftime('%a %b %d %Y %H:%M:%S')

        if acceptHeader == 'application/json':
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
        return self.getDoc()


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
        return self.getReleaseNotes()


    def support(self):
        """
        Provide users with information on how to get support for your
        RPI.

        When an HTTP GET is performed, return instructions for users
        on how to get support for your service, in human-readable
        format. Include help desk contact info, a link to any bug
        tracking systems and/or forums, etc.
        """
        return self.getSupport()


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
        return self.getSource()


    def tryme(self):
        """
        Allow users to try out your RPI online.

        This URI returns a page that allows the user to try your
        service, possibly with fixed input. Consider displaying the
        text of the HTTP request and response for reference
        purposes. If you are not providing this capability, please
        return status code 204 (No Content).
        """
        return self.getTryMe()



    def connectRoutes(self, d):
        d.connect(self.__class__.__name__ + '-info', '/%s/service/info' % (self.getUrlBase()), controller = self, action = 'info')
        d.connect(self.__class__.__name__ + '-stats', '/%s/service/stats' % (self.getUrlBase()), controller = self, action = 'stats')
        d.connect(self.__class__.__name__ + '-doc', '/%s/service/doc' % (self.getUrlBase()), controller = self, action = 'doc')
        d.connect(self.__class__.__name__ + '-releasenotes', '/%s/service/releasenotes' % (self.getUrlBase()), controller = self, action = 'releasenotes')
        d.connect(self.__class__.__name__ + '-support', '/%s/service/support' % (self.getUrlBase()), controller = self, action = 'support')
        d.connect(self.__class__.__name__ + '-source', '/%s/service/source' % (self.getUrlBase()), controller = self, action = 'source')
        d.connect(self.__class__.__name__ + '-tryme', '/%s/service/tryme' % (self.getUrlBase()), controller = self, action = 'tryme')








    #
    # The following abastract methods needs to be implemented in
    # each RPI service subclasses.
    # These are defined in the "RPI API Enhancements for CANARIE 
    # Service Registry and Monitoring System" document.
    #

    def getUrlBase(self):
        raise NotImplementedError()
        
    def getName(self):
        return self.__class__.__name__

    def getSynopsis(self):
        raise NotImplementedError()

    def getVersion(self):
        raise NotImplementedError()

    def getInstitution(self):
        raise NotImplementedError()

    def getReleaseTime(self):
        """
        Must return a datetime.datetime object.
        """
        raise NotImplementedError()

    def getInvocations(self):
        raise NotImplementedError()

    def getLastReset(self):
        """
        Must return a datetime.datetime object.
        """
        raise NotImplementedError()

    def getDoc(self):
        raise NotImplementedError()

    def getReleaseNotes(self):
        raise NotImplementedError()

    def getSupport(self):
        raise NotImplementedError()

    def getSource(self):
        # Defaults to 'No Content' if not implemented in subclass.
        cherrypy.response.status = 204
        
    def getTryMe(self):
        # Defaults to 'No Content' if not implemented in subclass.
        cherrypy.response.status = 204
        


