from base import RpiService
import redis
import collections



class BatchService(RpiService):
    """
    This class implements the Batch Service.
    It will query the redis database to get information about
    the status of the service.
    """

    def __init__(self, d):
        RpiService.__init__(self, d)
        self.r = redis.StrictRedis(host='localhost', port=6379, db=0)


    def getUsage(self):
        return int(self.r.get('nep52-cs-boot')) + int(self.r.get('nep52-cs-clock')) + int(self.r.get('nep52-client-boot')) + int(self.r.get('nep52-client-clock'))


    def getLastReset(self):
        return self.r.get('nep52-reset-date')


