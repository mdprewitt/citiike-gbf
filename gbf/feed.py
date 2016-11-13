import requests


class GeneralBikeshareFeed(object):
    gbfs_feed = 'http://gbfs.citibikenyc.com/gbfs/gbfs.json'

    def __init__(self):
        """
        { "last_updated":1478918732,
          "ttl":10,
          "data":{
              "en":{
                  "feeds":[
                      { "name":"system_information",
                        "url":"https://gbfs.citibikenyc.com/gbfs/en/system_information.json" },
                      { "name":"system_alerts",
                        "url":"https://gbfs.citibikenyc.com/gbfs/en/system_alerts.json" },
                      { "name":"station_information",
                        "url":"https://gbfs.citibikenyc.com/gbfs/en/station_information.json" },
                      { "name":"station_status",
                        "url":"https://gbfs.citibikenyc.com/gbfs/en/station_status.json" },
                      { "name":"system_regions",
                        "url":"https://gbfs.citibikenyc.com/gbfs/en/system_regions.json" }]}}}
        """
        r = requests.get(GeneralBikeshareFeed.gbfs_feed)
        data = r.json()
        self.feeds = dict()
        for feed in data['data']['en']['feeds']:
            self.feeds[feed['name']] = feed['url']

    def system_information(self):
        r = requests.get(self.feeds['system_information'])
        data = r.json()
        return data['data']

    def system_alerts(self):
        r = requests.get(self.feeds['system_alerts'])
        data = r.json()
        return data['data']['alerts']

    def station_information(self):
        r = requests.get(self.feeds['station_information'])
        data = r.json()
        return data['data']['stations']

    def station_status(self):
        r = requests.get(self.feeds['station_status'])
        data = r.json()
        return data['data']['stations']

    def system_regions(self):
        r = requests.get(self.feeds['system_regions'])
        data = r.json()
        return data['data']['regions']
