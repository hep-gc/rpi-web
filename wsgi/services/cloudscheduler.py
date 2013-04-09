from base import RpiService
import datetime

class CloudSchedulerService(RpiService):
    def getUrlBase(self):
        return 'cloudscheduler'

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
        return 0

    def getLastReset(self):
        return datetime.datetime.now()

    def getDoc(self):
        return 'This is the Cloud Scheuler service documentation page.'

    def getReleaseNotes(self):
        return 'These are the Cloud Scheuler service release notes.'

    def getSupport(self):
        return 'These are the Cloud Scheuler service support notes.'

    def getSource(self):
        return '<a href="https://github.com/hep-gc/cloud-scheduler">https://github.com/hep-gc/cloud-scheduler</a>'
        
