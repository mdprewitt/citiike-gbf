#!/usr/bin/env python
# encoding: utf-8


import argparse
import logging
import sys
import time
from datetime import datetime

import pytz
from elasticsearch_dsl.connections import connections

from gbf import GeneralBikeshareFeed
from gbf.es import StationStatus, StationInformation

__version__ = '1.0.0'
module = sys.modules['__main__'].__file__
log = logging.getLogger(module)

STATIONS = dict()


def load_stations(gbf):
    for station_data in gbf.station_information():
        try:
            log.info("Loading Station {0}".format(station_data['name']))
            station_data['rental_methods'] = ", ".join(station_data['rental_methods'])
            station = StationInformation(_id=station_data['station_id'], **station_data)
            station.status_date = datetime.utcnow()
            station.location = {'lon': station['lon'], 'lat': station['lat']}
            station.save()
            STATIONS[station_data['station_id']] = station
        except Exception as e:
            log.exception(e)


def load_station_metrics(gbf):
    while True:
        for station_status in gbf.station_status():
            try:
                unique_id = ":".join([str(station_status['station_id']), str(station_status['last_reported'])])
                if station_status['last_reported']:
                    station_status['last_reported'] = datetime.fromtimestamp(
                        station_status['last_reported'],
                        tz=pytz.UTC
                    )
                status = StationStatus(_id=unique_id, **station_status)
                try:
                    station_name = STATIONS[station_status['station_id']].name
                except:
                    load_stations(gbf)
                    station_name = STATIONS[station_status['station_id']].name
                status.station_name = station_name
                status.location = STATIONS[station_status['station_id']].location
                log.info("Loading Station Metrics {0}".format(status.station_name))
                status.save()
            except Exception as e:
                log.exception(e)

        print "Waiting..."
        time.sleep(10 * 60)


def parse_command_line(argv):
    """Parse command line argument. See -h option

    :param argv: arguments on the command line must include caller file name.
    """
    formatter_class = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(description=module,
                                     formatter_class=formatter_class)
    parser.add_argument("--es",
                        dest="eshosts",
                        action="append",
                        help="use specified elastic search host",
                        )
    parser.add_argument("--version", action="version",
                        version="%(prog)s {}".format(__version__))
    parser.add_argument("-v", "--verbose", dest="verbose_count",
                        action="count", default=0,
                        help="increases log verbosity for each occurence.")
    arguments = parser.parse_args(argv[1:])
    # Sets log level to WARN going more verbose for each new -v.
    log.setLevel(max(3 - arguments.verbose_count, 0) * 10)
    return arguments


def main():
    """Main program. Sets up logging and do some work."""
    logging.basicConfig(stream=sys.stderr, level=logging.WARN,
                        format='%(name)s (%(levelname)s): %(message)s')
    try:
        args = parse_command_line(sys.argv)
        connections.create_connection(hosts=args.eshosts)
        StationInformation.init()
        StationStatus.init()

        gbf = GeneralBikeshareFeed()
        gbf.system_information()
        gbf.system_alerts()
        gbf.system_regions()
        load_station_metrics(gbf)
    except KeyboardInterrupt:
        log.error('Program interrupted!')
    finally:
        logging.shutdown()

if __name__ == "__main__":
    sys.exit(main())
