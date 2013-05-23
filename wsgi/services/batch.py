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


    def getInvocations(self):
        values = collections.OrderedDict()
        values['Number of Cloud Scheduler boots'] = self.r.get('nep52-cs-boot')
        values['Cloud Scheduler hours'] = self.r.get('nep52-cs-clock')

        values['Number of CVMFS appliance boots'] = self.r.get('nep52-cvmfs-boot')
        values['CVMFS appliance hours'] = self.r.get('nep52-cvmfs-clock')

        values['Number of batch client boots'] = self.r.get('nep52-client-boot')
        values['Batch client hours'] = self.r.get('nep52-client-clock')
        return values


    def getLastReset(self):
        return self.r.get('nep52-reset-date')


