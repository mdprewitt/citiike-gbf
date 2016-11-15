from elasticsearch_dsl import DocType, Text, Integer, Date, Boolean, GeoPoint


class StationStatus(DocType):
    """
    {
        "station_id":"72",
        "num_bikes_available":11,
        "num_bikes_disabled":1,
        "num_docks_available":27,
        "num_docks_disabled":0,
        "is_installed":1,
        "is_renting":1,
        "is_returning":1,
        "last_reported":1478989087,
        "eightd_has_available_keys":false
    }
    """
    station_id = Text()
    location = GeoPoint()
    num_bikes_available = Integer()
    num_docks_available = Integer()
    num_docs_disabled = Integer()
    is_installed = Integer()
    is_renting = Integer()
    is_returning = Integer()
    last_reported = Date()
    eightd_has_key_dispenser = Boolean()
    station_name = Text(analyzer='snowball')

    class Meta:
        index = 'station_status'


class StationInformation(DocType):
    """
    {
        u'capacity': 39,
        u'name': u'W 52 St & 11 Ave',
        u'short_name': u'6926.01',
        u'lon': -73.99392888,
        u'lat': 40.76727216,
        u'station_id': u'72',
        u'rental_methods': [u'KEY', u'CREDITCARD'],
        u'eightd_has_key_dispenser': False,
        u'region_id': 71
    },
    """
    capacity = Integer()
    name = Text(analyzer='snowball')
    short_name = Text(analyzer='snowball')
    # TODO convert lat/lon to location = GeoPoint()
    location = GeoPoint()
    lon = Text()
    lat = Text()
    station_id = Text(analyzer='snowball')
    rental_methods = Text()  # [u'KEY', u'CREDITCARD'],
    eightd_has_key_dispenser = Boolean()
    region_id = Integer()
    status_date = Date()

    class Meta:
        index = 'stations'

    """
    def save(self, ** kwargs):
        self.lines = len(self.body.split())
        return super(StationInformation, self).save(** kwargs)
    """
