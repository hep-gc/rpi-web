from base import RpiService
import datetime

class CvmfsService(RpiService):
    def getUrlBase(self):
        return 'cvmfs'

    def getSynopsis(self):
        return 'CVMFS is a scalable read-only HTTP file system designed for distributed software deployment that was developed at the CERN Laboratory.'

    def getVersion(self):
        return '???'

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
        return 'This is the CVMFS service documentation page.'

    def getReleaseNotes(self):
        return 'These are the CVMFS service release notes.'

    def getSupport(self):
        return 'These are the CVMFS service support notes.'

