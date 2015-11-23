# -*- coding: utf-8 -*-
import unittest
from homescreen.weather import Credit, Time, WeatherResponse
from homescreen.weather_source import parse_forecast

class WeatherSourceTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parse_forecast(self):
        weather_forecast = parse_forecast(RESPONSE)
        self.assertIsInstance(weather_forecast, WeatherResponse)

    def test_parse_forecast_containsTimeList(self):
        weather_forecast = parse_forecast(RESPONSE)
        tf = weather_forecast.time_forecasts
        self.assertIsNotNone(tf)
        self.assertIsInstance(tf, list)

    def test_parse_forecast_containsTimeListWithElements(self):
        weather_forecast = parse_forecast(RESPONSE)
        tf = weather_forecast.time_forecasts
        self.assertTrue(len(tf) > 0, 'The time forecast list is empty. No forecasts were returned')
        self.assertIsInstance(tf[0], Time)

    def test_parse_forecast_hasSourceCredits(self):
        weather_forecast = parse_forecast(RESPONSE)
        self.assertIsInstance(weather_forecast.credit, Credit)

# source http://m.yr.no/sted/Norge/Postnummer/1364/varsel.xml 15.11.2015 12:28
RESPONSE = """\
<?xml version="1.0" encoding="UTF-8"?>
<weatherdata>
  <location>
    <name>1364 Fornebu</name>
    <type>Poststed</type>
    <country>Norge</country>
    <timezone id="Europe/Oslo" utcoffsetMinutes="60"/>
    <location altitude="9" latitude="59.8949" longitude="10.6258" geobase="postnummer" geobaseid="1364"/>
  </location>
  <credit>
    <!--For å bruke gratis værdata fra yr.no, MÅ du vise følgende tekst godt synlig på nettsiden din. Teksten skal være en lenke til URL-en som er spesifisert.-->
    <!--Les mer om vilkår for bruk av gratis værdata + retningslinjer på
http://om.yr.no/verdata/ -->
    <link text="Værvarsel fra yr.no, levert av NRK og Meteorologisk institutt" url="http://www.yr.no/sted/Norge/Postnummer/1364_Fornebu/"/>
  </credit>
  <links>
    <link id="xmlSource" url="http://www.yr.no/sted/Norge/Postnummer/1364_Fornebu/varsel.xml"/>
    <link id="xmlSourceHourByHour" url="http://www.yr.no/sted/Norge/Postnummer/1364_Fornebu/varsel_time_for_time.xml"/>
    <link id="overview" url="http://www.yr.no/sted/Norge/Postnummer/1364_Fornebu/"/>
    <link id="hourByHour" url="http://www.yr.no/sted/Norge/Postnummer/1364_Fornebu/time_for_time.html"/>
    <link id="longTermForecast" url="http://www.yr.no/sted/Norge/Postnummer/1364_Fornebu/langtidsvarsel.html"/>
    <link id="radar" url="http://www.yr.no/sted/Norge/Postnummer/1364_Fornebu/radar.html"/>
  </links>
  <meta>
    <lastupdate>2015-11-14T09:41:01</lastupdate>
    <nextupdate>2015-11-14T17:00:00</nextupdate>
  </meta>
  <sun rise="2015-11-14T08:11:18" set="2015-11-14T15:51:42"/>
  <forecast>
    <text>
      <location name="1364 Fornebu">
        <time from="2015-11-14" to="2015-11-14">
          <title>lørdag</title>
          <body>&lt;strong&gt;Østlandet og Telemark:&lt;/strong&gt; Sørvestlig bris, på kysten av Østfold og Vestfold opp i stiv kuling. Stort sett oppholdsvær og perioder med sol.</body>
        </time>
        <time from="2015-11-15" to="2015-11-15">
          <title>søndag</title>
          <body>&lt;strong&gt;Østlandet og Telemark:&lt;/strong&gt; Vestlig bris. Lange perioder med sol, men først på dagen lokal tåke, enkelte regnbyger i nordlige områder av Østlandet.</body>
        </time>
        <time from="2015-11-16" to="2015-11-16">
          <title>mandag</title>
          <body>&lt;strong&gt;Østlandet:&lt;/strong&gt; Sørøstlig bris. Oppholdsvær. Fra formiddagen periodevis sørøstlig kuling på kysten. Regn fra sør, nedbør som snø i indre høyere strøk først på dagen, senere snø nord på Østlandet. Omtrent uendret temperatur.</body>
        </time>
        <time from="2015-11-17" to="2015-11-18">
          <title>tirsdag og onsdag</title>
          <body>&lt;strong&gt;Sør-Norge:&lt;/strong&gt; Et lavtrykk beveger seg mot Sør-Norge. Det ventes sørvestlig vind, periodevis kuling på kysten og i fjellet. Perioder med regn, snø i fjellet, lavere snøgrense nord på Østlandet. Onsdag ventes nedbøraktiviteten å fortsette. Små temperaturendringer.</body>
        </time>
      </location>
    </text>
    <tabular>
      <time from="2015-11-14T13:00:00" to="2015-11-14T18:00:00" period="2">
        <!-- Valid from 2015-11-14T13:00:00 to 2015-11-14T18:00:00 -->
        <symbol number="3" numberEx="3" name="Delvis skyet" var="03d"/>
        <precipitation value="0"/>
        <!-- Valid at 2015-11-14T13:00:00 -->
        <windDirection deg="275.2" code="W" name="Vest"/>
        <windSpeed mps="0.6" name="Flau vind"/>
        <temperature unit="celsius" value="4"/>
        <pressure unit="hPa" value="997.1"/>
      </time>
      <time from="2015-11-14T18:00:00" to="2015-11-15T00:00:00" period="3">
        <!-- Valid from 2015-11-14T18:00:00 to 2015-11-15T00:00:00 -->
        <symbol number="3" numberEx="3" name="Delvis skyet" var="mf/03n.09"/>
        <precipitation value="0"/>
        <!-- Valid at 2015-11-14T18:00:00 -->
        <windDirection deg="225.7" code="SW" name="Sørvest"/>
        <windSpeed mps="3.1" name="Svak vind"/>
        <temperature unit="celsius" value="3"/>
        <pressure unit="hPa" value="997.2"/>
      </time>
      <time from="2015-11-15T00:00:00" to="2015-11-15T06:00:00" period="0">
        <!-- Valid from 2015-11-15T00:00:00 to 2015-11-15T06:00:00 -->
        <symbol number="2" numberEx="2" name="Lettskyet" var="mf/02n.12"/>
        <precipitation value="0"/>
        <!-- Valid at 2015-11-15T00:00:00 -->
        <windDirection deg="236.7" code="WSW" name="Vest-sørvest"/>
        <windSpeed mps="2.8" name="Svak vind"/>
        <temperature unit="celsius" value="3"/>
        <pressure unit="hPa" value="997.3"/>
      </time>
      <time from="2015-11-15T06:00:00" to="2015-11-15T12:00:00" period="1">
        <!-- Valid from 2015-11-15T06:00:00 to 2015-11-15T12:00:00 -->
        <symbol number="2" numberEx="2" name="Lettskyet" var="02d"/>
        <precipitation value="0"/>
        <!-- Valid at 2015-11-15T06:00:00 -->
        <windDirection deg="354.7" code="N" name="Nord"/>
        <windSpeed mps="2.0" name="Svak vind"/>
        <temperature unit="celsius" value="0"/>
        <pressure unit="hPa" value="996.4"/>
      </time>
      <time from="2015-11-15T12:00:00" to="2015-11-15T18:00:00" period="2">
        <!-- Valid from 2015-11-15T12:00:00 to 2015-11-15T18:00:00 -->
        <symbol number="1" numberEx="1" name="Klarvær" var="01d"/>
        <precipitation value="0"/>
        <!-- Valid at 2015-11-15T12:00:00 -->
        <windDirection deg="223.5" code="SW" name="Sørvest"/>
        <windSpeed mps="0.7" name="Flau vind"/>
        <temperature unit="celsius" value="3"/>
        <pressure unit="hPa" value="997.5"/>
      </time>
      <time from="2015-11-15T18:00:00" to="2015-11-16T00:00:00" period="3">
        <!-- Valid from 2015-11-15T18:00:00 to 2015-11-16T00:00:00 -->
        <symbol number="2" numberEx="2" name="Lettskyet" var="mf/02n.12"/>
        <precipitation value="0"/>
        <!-- Valid at 2015-11-15T18:00:00 -->
        <windDirection deg="357.0" code="N" name="Nord"/>
        <windSpeed mps="2.8" name="Svak vind"/>
        <temperature unit="celsius" value="0"/>
        <pressure unit="hPa" value="1001.9"/>
      </time>
      <time from="2015-11-16T00:00:00" to="2015-11-16T06:00:00" period="0">
        <!-- Valid from 2015-11-16T00:00:00 to 2015-11-16T06:00:00 -->
        <symbol number="4" numberEx="4" name="Skyet" var="04"/>
        <precipitation value="0"/>
        <!-- Valid at 2015-11-16T00:00:00 -->
        <windDirection deg="72.3" code="ENE" name="Øst-nordøst"/>
        <windSpeed mps="2.8" name="Svak vind"/>
        <temperature unit="celsius" value="-1"/>
        <pressure unit="hPa" value="1007.2"/>
      </time>
      <time from="2015-11-16T06:00:00" to="2015-11-16T12:00:00" period="1">
        <!-- Valid from 2015-11-16T06:00:00 to 2015-11-16T12:00:00 -->
        <symbol number="12" numberEx="12" name="Sludd" var="12"/>
        <precipitation value="4.4" minvalue="3.6" maxvalue="5.2"/>
        <!-- Valid at 2015-11-16T06:00:00 -->
        <windDirection deg="55.5" code="NE" name="Nordøst"/>
        <windSpeed mps="3.7" name="Lett bris"/>
        <temperature unit="celsius" value="-2"/>
        <pressure unit="hPa" value="1006.1"/>
      </time>
      <time from="2015-11-16T12:00:00" to="2015-11-16T18:00:00" period="2">
        <!-- Valid from 2015-11-16T12:00:00 to 2015-11-16T18:00:00 -->
        <symbol number="13" numberEx="50" name="Kraftig snø" var="50"/>
        <precipitation value="6.2" minvalue="5.2" maxvalue="7.2"/>
        <!-- Valid at 2015-11-16T12:00:00 -->
        <windDirection deg="40.4" code="NE" name="Nordøst"/>
        <windSpeed mps="3.8" name="Lett bris"/>
        <temperature unit="celsius" value="1"/>
        <pressure unit="hPa" value="1002.0"/>
      </time>
      <time from="2015-11-16T18:00:00" to="2015-11-17T00:00:00" period="3">
        <!-- Valid from 2015-11-16T18:00:00 to 2015-11-17T00:00:00 -->
        <symbol number="8" numberEx="8" name="Snøbyger" var="mf/08n.15"/>
        <precipitation value="1.0" minvalue="0.7" maxvalue="1.4"/>
        <!-- Valid at 2015-11-16T18:00:00 -->
        <windDirection deg="35.1" code="NE" name="Nordøst"/>
        <windSpeed mps="4.5" name="Lett bris"/>
        <temperature unit="celsius" value="0"/>
        <pressure unit="hPa" value="992.9"/>
      </time>
      <time from="2015-11-17T01:00:00" to="2015-11-17T07:00:00" period="0">
        <!-- Valid from 2015-11-17T01:00:00 to 2015-11-17T07:00:00 -->
        <symbol number="3" numberEx="3" name="Delvis skyet" var="mf/03n.19"/>
        <precipitation value="0"/>
        <!-- Valid at 2015-11-17T01:00:00 -->
        <windDirection deg="349.9" code="N" name="Nord"/>
        <windSpeed mps="2.8" name="Svak vind"/>
        <temperature unit="celsius" value="-1"/>
        <pressure unit="hPa" value="995.7"/>
      </time>
      <time from="2015-11-17T07:00:00" to="2015-11-17T13:00:00" period="1">
        <!-- Valid from 2015-11-17T07:00:00 to 2015-11-17T13:00:00 -->
        <symbol number="4" numberEx="4" name="Skyet" var="04"/>
        <precipitation value="0"/>
        <!-- Valid at 2015-11-17T07:00:00 -->
        <windDirection deg="187.6" code="S" name="Sør"/>
        <windSpeed mps="2.0" name="Svak vind"/>
        <temperature unit="celsius" value="4"/>
        <pressure unit="hPa" value="991.5"/>
      </time>
      <time from="2015-11-17T13:00:00" to="2015-11-17T19:00:00" period="2">
        <!-- Valid from 2015-11-17T13:00:00 to 2015-11-17T19:00:00 -->
        <symbol number="3" numberEx="3" name="Delvis skyet" var="03d"/>
        <precipitation value="0"/>
        <!-- Valid at 2015-11-17T13:00:00 -->
        <windDirection deg="208.5" code="SSW" name="Sør-sørvest"/>
        <windSpeed mps="2.4" name="Svak vind"/>
        <temperature unit="celsius" value="5"/>
        <pressure unit="hPa" value="991.3"/>
      </time>
      <time from="2015-11-17T19:00:00" to="2015-11-18T01:00:00" period="3">
        <!-- Valid from 2015-11-17T19:00:00 to 2015-11-18T01:00:00 -->
        <symbol number="3" numberEx="3" name="Delvis skyet" var="mf/03n.19"/>
        <precipitation value="0"/>
        <!-- Valid at 2015-11-17T19:00:00 -->
        <windDirection deg="203.0" code="SSW" name="Sør-sørvest"/>
        <windSpeed mps="2.0" name="Svak vind"/>
        <temperature unit="celsius" value="5"/>
        <pressure unit="hPa" value="990.2"/>
      </time>
      <time from="2015-11-18T01:00:00" to="2015-11-18T07:00:00" period="0">
        <!-- Valid from 2015-11-18T01:00:00 to 2015-11-18T07:00:00 -->
        <symbol number="4" numberEx="4" name="Skyet" var="04"/>
        <precipitation value="0"/>
        <!-- Valid at 2015-11-18T01:00:00 -->
        <windDirection deg="196.1" code="SSW" name="Sør-sørvest"/>
        <windSpeed mps="1.7" name="Svak vind"/>
        <temperature unit="celsius" value="4"/>
        <pressure unit="hPa" value="987.6"/>
      </time>
      <time from="2015-11-18T07:00:00" to="2015-11-18T13:00:00" period="1">
        <!-- Valid from 2015-11-18T07:00:00 to 2015-11-18T13:00:00 -->
        <symbol number="4" numberEx="4" name="Skyet" var="04"/>
        <precipitation value="0"/>
        <!-- Valid at 2015-11-18T07:00:00 -->
        <windDirection deg="212.8" code="SSW" name="Sør-sørvest"/>
        <windSpeed mps="1.5" name="Flau vind"/>
        <temperature unit="celsius" value="3"/>
        <pressure unit="hPa" value="986.9"/>
      </time>
      <time from="2015-11-18T13:00:00" to="2015-11-18T19:00:00" period="2">
        <!-- Valid from 2015-11-18T13:00:00 to 2015-11-18T19:00:00 -->
        <symbol number="4" numberEx="4" name="Skyet" var="04"/>
        <precipitation value="0"/>
        <!-- Valid at 2015-11-18T13:00:00 -->
        <windDirection deg="309.2" code="NW" name="Nordvest"/>
        <windSpeed mps="1.5" name="Flau vind"/>
        <temperature unit="celsius" value="2"/>
        <pressure unit="hPa" value="989.7"/>
      </time>
      <time from="2015-11-18T19:00:00" to="2015-11-19T01:00:00" period="3">
        <!-- Valid from 2015-11-18T19:00:00 to 2015-11-19T01:00:00 -->
        <symbol number="3" numberEx="3" name="Delvis skyet" var="mf/03n.22"/>
        <precipitation value="0"/>
        <!-- Valid at 2015-11-18T19:00:00 -->
        <windDirection deg="306.6" code="NW" name="Nordvest"/>
        <windSpeed mps="1.3" name="Flau vind"/>
        <temperature unit="celsius" value="3"/>
        <pressure unit="hPa" value="992.0"/>
      </time>
      <time from="2015-11-19T01:00:00" to="2015-11-19T07:00:00" period="0">
        <!-- Valid from 2015-11-19T01:00:00 to 2015-11-19T07:00:00 -->
        <symbol number="4" numberEx="4" name="Skyet" var="04"/>
        <precipitation value="0"/>
        <!-- Valid at 2015-11-19T01:00:00 -->
        <windDirection deg="23.0" code="NNE" name="Nord-nordøst"/>
        <windSpeed mps="1.5" name="Flau vind"/>
        <temperature unit="celsius" value="2"/>
        <pressure unit="hPa" value="993.4"/>
      </time>
      <time from="2015-11-19T07:00:00" to="2015-11-19T13:00:00" period="1">
        <!-- Valid from 2015-11-19T07:00:00 to 2015-11-19T13:00:00 -->
        <symbol number="4" numberEx="4" name="Skyet" var="04"/>
        <precipitation value="0"/>
        <!-- Valid at 2015-11-19T07:00:00 -->
        <windDirection deg="315.7" code="NW" name="Nordvest"/>
        <windSpeed mps="1.8" name="Svak vind"/>
        <temperature unit="celsius" value="1"/>
        <pressure unit="hPa" value="993.7"/>
      </time>
      <time from="2015-11-19T13:00:00" to="2015-11-19T19:00:00" period="2">
        <!-- Valid from 2015-11-19T13:00:00 to 2015-11-19T19:00:00 -->
        <symbol number="4" numberEx="4" name="Skyet" var="04"/>
        <precipitation value="0"/>
        <!-- Valid at 2015-11-19T13:00:00 -->
        <windDirection deg="336.4" code="NNW" name="Nord-nordvest"/>
        <windSpeed mps="1.9" name="Svak vind"/>
        <temperature unit="celsius" value="1"/>
        <pressure unit="hPa" value="993.9"/>
      </time>
      <time from="2015-11-19T19:00:00" to="2015-11-20T01:00:00" period="3">
        <!-- Valid from 2015-11-19T19:00:00 to 2015-11-20T01:00:00 -->
        <symbol number="3" numberEx="3" name="Delvis skyet" var="mf/03n.26"/>
        <precipitation value="0"/>
        <!-- Valid at 2015-11-19T19:00:00 -->
        <windDirection deg="295.1" code="WNW" name="Vest-nordvest"/>
        <windSpeed mps="1.7" name="Svak vind"/>
        <temperature unit="celsius" value="2"/>
        <pressure unit="hPa" value="996.5"/>
      </time>
      <time from="2015-11-20T01:00:00" to="2015-11-20T07:00:00" period="0">
        <!-- Valid from 2015-11-20T01:00:00 to 2015-11-20T07:00:00 -->
        <symbol number="4" numberEx="4" name="Skyet" var="04"/>
        <precipitation value="0"/>
        <!-- Valid at 2015-11-20T01:00:00 -->
        <windDirection deg="333.6" code="NNW" name="Nord-nordvest"/>
        <windSpeed mps="2.0" name="Svak vind"/>
        <temperature unit="celsius" value="1"/>
        <pressure unit="hPa" value="996.7"/>
      </time>
      <time from="2015-11-20T07:00:00" to="2015-11-20T13:00:00" period="1">
        <!-- Valid from 2015-11-20T07:00:00 to 2015-11-20T13:00:00 -->
        <symbol number="4" numberEx="4" name="Skyet" var="04"/>
        <precipitation value="0"/>
        <!-- Valid at 2015-11-20T07:00:00 -->
        <windDirection deg="198.2" code="SSW" name="Sør-sørvest"/>
        <windSpeed mps="2.2" name="Svak vind"/>
        <temperature unit="celsius" value="0"/>
        <pressure unit="hPa" value="997.1"/>
      </time>
      <time from="2015-11-20T13:00:00" to="2015-11-20T19:00:00" period="2">
        <!-- Valid from 2015-11-20T13:00:00 to 2015-11-20T19:00:00 -->
        <symbol number="4" numberEx="4" name="Skyet" var="04"/>
        <precipitation value="0"/>
        <!-- Valid at 2015-11-20T13:00:00 -->
        <windDirection deg="313.6" code="NW" name="Nordvest"/>
        <windSpeed mps="1.9" name="Svak vind"/>
        <temperature unit="celsius" value="1"/>
        <pressure unit="hPa" value="999.7"/>
      </time>
      <time from="2015-11-20T19:00:00" to="2015-11-21T01:00:00" period="3">
        <!-- Valid from 2015-11-20T19:00:00 to 2015-11-21T01:00:00 -->
        <symbol number="3" numberEx="3" name="Delvis skyet" var="mf/03n.29"/>
        <precipitation value="0"/>
        <!-- Valid at 2015-11-20T19:00:00 -->
        <windDirection deg="358.5" code="N" name="Nord"/>
        <windSpeed mps="2.1" name="Svak vind"/>
        <temperature unit="celsius" value="1"/>
        <pressure unit="hPa" value="1000.4"/>
      </time>
      <time from="2015-11-21T01:00:00" to="2015-11-21T07:00:00" period="0">
        <!-- Valid from 2015-11-21T01:00:00 to 2015-11-21T07:00:00 -->
        <symbol number="4" numberEx="4" name="Skyet" var="04"/>
        <precipitation value="0"/>
        <!-- Valid at 2015-11-21T01:00:00 -->
        <windDirection deg="294.5" code="WNW" name="Vest-nordvest"/>
        <windSpeed mps="1.9" name="Svak vind"/>
        <temperature unit="celsius" value="0"/>
        <pressure unit="hPa" value="1000.6"/>
      </time>
      <time from="2015-11-21T07:00:00" to="2015-11-21T13:00:00" period="1">
        <!-- Valid from 2015-11-21T07:00:00 to 2015-11-21T13:00:00 -->
        <symbol number="4" numberEx="4" name="Skyet" var="04"/>
        <precipitation value="0"/>
        <!-- Valid at 2015-11-21T07:00:00 -->
        <windDirection deg="340.1" code="NNW" name="Nord-nordvest"/>
        <windSpeed mps="2.0" name="Svak vind"/>
        <temperature unit="celsius" value="-2"/>
        <pressure unit="hPa" value="1000.5"/>
      </time>
      <time from="2015-11-21T13:00:00" to="2015-11-21T19:00:00" period="2">
        <!-- Valid from 2015-11-21T13:00:00 to 2015-11-21T19:00:00 -->
        <symbol number="3" numberEx="3" name="Delvis skyet" var="03d"/>
        <precipitation value="0"/>
        <!-- Valid at 2015-11-21T13:00:00 -->
        <windDirection deg="293.7" code="WNW" name="Vest-nordvest"/>
        <windSpeed mps="1.7" name="Svak vind"/>
        <temperature unit="celsius" value="-1"/>
        <pressure unit="hPa" value="1001.5"/>
      </time>
      <time from="2015-11-21T19:00:00" to="2015-11-22T01:00:00" period="3">
        <!-- Valid from 2015-11-21T19:00:00 to 2015-11-22T01:00:00 -->
        <symbol number="3" numberEx="3" name="Delvis skyet" var="mf/03n.32"/>
        <precipitation value="0"/>
        <!-- Valid at 2015-11-21T19:00:00 -->
        <windDirection deg="317.0" code="NW" name="Nordvest"/>
        <windSpeed mps="2.1" name="Svak vind"/>
        <temperature unit="celsius" value="-1"/>
        <pressure unit="hPa" value="1000.7"/>
      </time>
      <time from="2015-11-22T01:00:00" to="2015-11-22T07:00:00" period="0">
        <!-- Valid from 2015-11-22T01:00:00 to 2015-11-22T07:00:00 -->
        <symbol number="4" numberEx="4" name="Skyet" var="04"/>
        <precipitation value="0"/>
        <!-- Valid at 2015-11-22T01:00:00 -->
        <windDirection deg="350.9" code="N" name="Nord"/>
        <windSpeed mps="2.0" name="Svak vind"/>
        <temperature unit="celsius" value="-1"/>
        <pressure unit="hPa" value="1002.7"/>
      </time>
      <time from="2015-11-22T07:00:00" to="2015-11-22T13:00:00" period="1">
        <!-- Valid from 2015-11-22T07:00:00 to 2015-11-22T13:00:00 -->
        <symbol number="3" numberEx="3" name="Delvis skyet" var="03d"/>
        <precipitation value="0"/>
        <!-- Valid at 2015-11-22T07:00:00 -->
        <windDirection deg="309.9" code="NW" name="Nordvest"/>
        <windSpeed mps="2.1" name="Svak vind"/>
        <temperature unit="celsius" value="-2"/>
        <pressure unit="hPa" value="1003.6"/>
      </time>
      <time from="2015-11-22T13:00:00" to="2015-11-22T19:00:00" period="2">
        <!-- Valid from 2015-11-22T13:00:00 to 2015-11-22T19:00:00 -->
        <symbol number="3" numberEx="3" name="Delvis skyet" var="03d"/>
        <precipitation value="0"/>
        <!-- Valid at 2015-11-22T13:00:00 -->
        <windDirection deg="308.2" code="NW" name="Nordvest"/>
        <windSpeed mps="1.7" name="Svak vind"/>
        <temperature unit="celsius" value="-1"/>
        <pressure unit="hPa" value="1003.9"/>
      </time>
      <time from="2015-11-22T19:00:00" to="2015-11-23T01:00:00" period="3">
        <!-- Valid from 2015-11-22T19:00:00 to 2015-11-23T01:00:00 -->
        <symbol number="3" numberEx="3" name="Delvis skyet" var="mf/03n.36"/>
        <precipitation value="0"/>
        <!-- Valid at 2015-11-22T19:00:00 -->
        <windDirection deg="328.6" code="NNW" name="Nord-nordvest"/>
        <windSpeed mps="2.0" name="Svak vind"/>
        <temperature unit="celsius" value="-2"/>
        <pressure unit="hPa" value="1004.3"/>
      </time>
      <time from="2015-11-23T01:00:00" to="2015-11-23T07:00:00" period="0">
        <!-- Valid from 2015-11-23T01:00:00 to 2015-11-23T07:00:00 -->
        <symbol number="4" numberEx="4" name="Skyet" var="04"/>
        <precipitation value="0"/>
        <!-- Valid at 2015-11-23T01:00:00 -->
        <windDirection deg="209.2" code="SSW" name="Sør-sørvest"/>
        <windSpeed mps="1.7" name="Svak vind"/>
        <temperature unit="celsius" value="-3"/>
        <pressure unit="hPa" value="1005.4"/>
      </time>
      <time from="2015-11-23T07:00:00" to="2015-11-23T13:00:00" period="1">
        <!-- Valid from 2015-11-23T07:00:00 to 2015-11-23T13:00:00 -->
        <symbol number="4" numberEx="4" name="Skyet" var="04"/>
        <precipitation value="0"/>
        <!-- Valid at 2015-11-23T07:00:00 -->
        <windDirection deg="340.4" code="NNW" name="Nord-nordvest"/>
        <windSpeed mps="1.7" name="Svak vind"/>
        <temperature unit="celsius" value="-3"/>
        <pressure unit="hPa" value="1005.1"/>
      </time>
      <time from="2015-11-23T13:00:00" to="2015-11-23T19:00:00" period="2">
        <!-- Valid from 2015-11-23T13:00:00 to 2015-11-23T19:00:00 -->
        <symbol number="4" numberEx="4" name="Skyet" var="04"/>
        <precipitation value="0"/>
        <!-- Valid at 2015-11-23T13:00:00 -->
        <windDirection deg="304.8" code="NW" name="Nordvest"/>
        <windSpeed mps="1.5" name="Flau vind"/>
        <temperature unit="celsius" value="-2"/>
        <pressure unit="hPa" value="1006.3"/>
      </time>
    </tabular>
  </forecast>
  <observations>
    <weatherstation stno="18815" sttype="eklima" name="Bygdøy" distance="3372" lat="59.90500" lon="10.68280" source="Meteorologisk Institutt">
      <temperature unit="celsius" value="3.1" time="2015-11-14T10:00:00Z"/>
    </weatherstation>
    <weatherstation stno="18700" sttype="eklima" name="Oslo (Blindern)" distance="7441" lat="59.94230" lon="10.72000" source="Meteorologisk Institutt">
      <symbol number="4" name="Skyet" time="2015-11-14T09:00:00Z"/>
      <temperature unit="celsius" value="3.3" time="2015-11-14T11:00:00Z"/>
      <windDirection deg="206.0" code="SSW" name="Sør-sørvest" time="2015-11-14T11:00:00Z"/>
      <windSpeed mps="2.2" name="Svak vind" time="2015-11-14T11:00:00Z"/>
    </weatherstation>
    <weatherstation stno="18950" sttype="eklima" name="Tryvannshøgda" distance="10278" lat="59.98470" lon="10.66930" source="Meteorologisk Institutt">
      <temperature unit="celsius" value="-0.1" time="2015-11-14T11:00:00Z"/>
      <windDirection deg="207.0" code="SSW" name="Sør-sørvest" time="2015-11-14T11:00:00Z"/>
      <windSpeed mps="4.3" name="Lett bris" time="2015-11-14T11:00:00Z"/>
    </weatherstation>
  </observations>
</weatherdata>
"""