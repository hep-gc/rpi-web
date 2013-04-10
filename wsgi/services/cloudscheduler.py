from base import RpiService
import datetime
import xmlrpclib

class CloudSchedulerService(RpiService):
#    def getVersion(self):
#        proxy = xmlrpclib.ServerProxy(self._getXmlRpcServer())
#        return proxy.get_version()

#    def getReleaseTime(self):
#        """
#        Must return a datetime.datetime object.
#        """
#        return datetime.datetime.now()

#    def getInvocations(self):
#        return 0

    def getLastReset(self):
        return datetime.datetime.now()

