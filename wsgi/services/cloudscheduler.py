from base import RpiService
import datetime

class CloudSchedulerService(RpiService):
    def getName(self):
        return 'CloudScheduler'
    
    def getSynopsis(self):
        return 'A service to schedule work between clouds.'

    def getVersion(self):
        return '0.1'

    def getInstitution(self):
        return 'UVIC HEP Group'

    def getReleaseTime(self):
        """
        Must return a datetime.datetime object.
        """
        return datetime.datetime.now()

    def getInvocations(self):
        raise NotImplementedError()

    def getLastReset(self):
        raise NotImplementedError()

    def getDoc(self):
        return 'This is the service documentation page.'

    def getReleaseNotes(self):
        return 'These are the release notes.'


