from base import RpiService
import redis
import collections



class SoftwareRepository(RpiService):
    """
    This class implements the Shared Software Repository service.
    It will query the redis database to get information about
    the status of the service.
    """

    def __init__(self, d):
        RpiService.__init__(self, d)
        self.r = redis.StrictRedis(host='localhost', port=6379, db=0)


    def getUsage(self):
        return int(self.r.get('nep52-cvmfs-boot')) + int(self.r.get('nep52-cvmfs-clock')) + int(self.r.get('nep52-iclient-boot')) + int(self.r.get('nep52-iclient-clock'))


    def getLastReset(self):
        return self.r.get('nep52-reset2-date')


