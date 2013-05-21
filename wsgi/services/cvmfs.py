from base import RpiService
import redis

class CvmfsService(RpiService):
    def __init__(self, d):
        RpiService.__init__(self, d)
        self.r = redis.StrictRedis(host='localhost', port=6379, db=0)


    def getInvocations(self):
        return self.r.get('nep52-cvmfs-boot')

    def getLastReset(self):
        return self.r.get('nep52-reset-date')


