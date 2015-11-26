# -*- coding: utf-8 -*-
import unittest
from homescreen.public_transport_source import parse_transport_for_stop, parse_stopid_for_location
from homescreen.public_transport import DepartureResponse

class PublicTansportSourceTests(unittest.TestCase):
    def setUp(self):
        # <Place i:type="Stop"><District>Bærum</District><ID>2190017</ID><Name>Fornebu vest</Name><PlaceType i:nil="true"/><IsHub>false</IsHub><ShortName>FBUV</ShortName><X>590700</X><Y>6640619</Y><Zone>1</Zone></Place>
        self.northing_forenebu_vest = '590700'
        self.easting_fornebu_vest = '6640619'
        self.json = 'application/json'
        self.xml = 'application/xml'


    def tearDown(self):
        pass


    def test_parse_stopid_for_location_xml(self):
        departures = parse_stopid_for_location(XML_RESPONSE, self.xml)
        self.assertIsNotNone(departures)


#    def test_parse_stopid_for_location(self):
#        departures = parse_stopid_for_location(STOPID_FOR_LOCATION_RESPONSE, self.json)
#        self.assertIsNotNone(departures)


    def test_parse_transport_for_stop(self):
        departures = parse_transport_for_stop(RESPONSE, self.json)
        self.assertIsNotNone(departures)


    def test_parse_transport_for_stop_returnsResponse(self):
        departures = parse_transport_for_stop(RESPONSE, self.json)
        self.assertIsInstance(departures, list)


    def test_parse_stopid_for_location(self):
        response = parse_stopid_for_location(STOPID_FOR_LOCATION_RESPONSE, self.json)
        self.assertIsInstance(response, list)


    def test_parse_stopid_for_location_response_has_stop_name(self):
        response = parse_stopid_for_location(STOPID_FOR_LOCATION_RESPONSE, self.json)
        self.assertIsNotNone(response)
        self.assertNotEqual(0, len(response))


    def test_(self):
        pass


STOPID_FOR_LOCATION_RESPONSE = """[{"AlightingAllowed":false,"BoardingAllowed":false,"RealTimeStop":false,"Lines":[],"StopPoints":[],"Deviations":[],"X":0,"Y":0,"Zone":"Marker","ShortName":"","IsHub":false,"ID":1197385,"Name":"Yterbøl","District":"Marker","PlaceType":"Stop"},{"AlightingAllowed":false,"BoardingAllowed":false,"RealTimeStop":false,"Lines":[],"StopPoints":[],"Deviations":[],"X":0,"Y":0,"Zone":"0","ShortName":"","IsHub":false,"ID":4170623,"Name":"Espa E6 Syd","District":"Stange","PlaceType":"Stop"},{"AlightingAllowed":false,"BoardingAllowed":false,"RealTimeStop":false,"Lines":[],"StopPoints":[],"Deviations":[],"X":0,"Y":0,"Zone":"0","ShortName":"","IsHub":false,"ID":4170624,"Name":"Espa E6 Nord","District":"Stange","PlaceType":"Stop"}]"""

PROXIMITY_RESPONSE = """\
[
  {
    "ID": 1,
    "Name": "sample string 2",
    "District": "sample string 3",
    "PlaceType": "sample string 4"
  },
  {
    "ID": 1,
    "Name": "sample string 2",
    "District": "sample string 3",
    "PlaceType": "sample string 4"
  }
]
"""

RESPONSE = """\
[
  {
    "RecordedAtTime": "2015-11-15T01:11:09.4057023+01:00",
    "MonitoringRef": "sample string 2",
    "MonitoredVehicleJourney": {
      "LineRef": "sample string 1",
      "DirectionRef": "sample string 2",
      "FramedVehicleJourneyRef": {
        "DataFrameRef": "sample string 1",
        "DatedVehicleJourneyRef": "sample string 2"
      },
      "PublishedLineName": "sample string 3",
      "DirectionName": "sample string 4",
      "OperatorRef": "sample string 5",
      "OriginName": "sample string 6",
      "OriginRef": "sample string 7",
      "DestinationRef": 8,
      "DestinationName": "sample string 9",
      "OriginAimedDepartureTime": "2015-11-15T01:11:09.4057023+01:00",
      "DestinationAimedArrivalTime": "2015-11-15T01:11:09.4057023+01:00",
      "Monitored": true,
      "InCongestion": true,
      "Delay": "sample string 14",
      "TrainBlockPart": {
        "NumberOfBlockParts": 1
      },
      "BlockRef": "sample string 15",
      "VehicleRef": "sample string 16",
      "VehicleMode": 0,
      "VehicleJourneyName": "sample string 17",
      "MonitoredCall": {
        "VisitNumber": 1,
        "VehicleAtStop": true,
        "DestinationDisplay": "sample string 3",
        "AimedArrivalTime": "2015-11-15T01:11:09.4057023+01:00",
        "ExpectedArrivalTime": "2015-11-15T01:11:09.4057023+01:00",
        "AimedDepartureTime": "2015-11-15T01:11:09.4057023+01:00",
        "ExpectedDepartureTime": "2015-11-15T01:11:09.4057023+01:00",
        "DeparturePlatformName": "sample string 8"
      },
      "VehicleFeatureRef": "sample string 18"
    },
    "Extensions": {
      "IsHub": true,
      "OccupancyData": {
        "OccupancyAvailable": true,
        "OccupancyPercentage": 2
      },
      "Deviations": [
        {
          "ID": 1,
          "Header": "sample string 2"
        },
        {
          "ID": 1,
          "Header": "sample string 2"
        }
      ],
      "LineColour": "sample string 2"
    }
  },
  {
    "RecordedAtTime": "2015-11-15T01:11:09.4057023+01:00",
    "MonitoringRef": "sample string 2",
    "MonitoredVehicleJourney": {
      "LineRef": "sample string 1",
      "DirectionRef": "sample string 2",
      "FramedVehicleJourneyRef": {
        "DataFrameRef": "sample string 1",
        "DatedVehicleJourneyRef": "sample string 2"
      },
      "PublishedLineName": "sample string 3",
      "DirectionName": "sample string 4",
      "OperatorRef": "sample string 5",
      "OriginName": "sample string 6",
      "OriginRef": "sample string 7",
      "DestinationRef": 8,
      "DestinationName": "sample string 9",
      "OriginAimedDepartureTime": "2015-11-15T01:11:09.4057023+01:00",
      "DestinationAimedArrivalTime": "2015-11-15T01:11:09.4057023+01:00",
      "Monitored": true,
      "InCongestion": true,
      "Delay": "sample string 14",
      "TrainBlockPart": {
        "NumberOfBlockParts": 1
      },
      "BlockRef": "sample string 15",
      "VehicleRef": "sample string 16",
      "VehicleMode": 0,
      "VehicleJourneyName": "sample string 17",
      "MonitoredCall": {
        "VisitNumber": 1,
        "VehicleAtStop": true,
        "DestinationDisplay": "sample string 3",
        "AimedArrivalTime": "2015-11-15T01:11:09.4057023+01:00",
        "ExpectedArrivalTime": "2015-11-15T01:11:09.4057023+01:00",
        "AimedDepartureTime": "2015-11-15T01:11:09.4057023+01:00",
        "ExpectedDepartureTime": "2015-11-15T01:11:09.4057023+01:00",
        "DeparturePlatformName": "sample string 8"
      },
      "VehicleFeatureRef": "sample string 18"
    },
    "Extensions": {
      "IsHub": true,
      "OccupancyData": {
        "OccupancyAvailable": true,
        "OccupancyPercentage": 2
      },
      "Deviations": [
        {
          "ID": 1,
          "Header": "sample string 2"
        },
        {
          "ID": 1,
          "Header": "sample string 2"
        }
      ],
      "LineColour": "sample string 2"
    }
  }
]
"""

XML_RESPONSE = "<ArrayOfDepartures></ArrayOfDepartures>"