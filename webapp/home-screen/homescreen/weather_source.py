# -*- coding: utf-8 -*-
import urllib2
import xml, xml.sax
import cStringIO
from homescreen.weather import WeatherResponse, Credit, Time
import logging

logger = logging.getLogger(__name__)


class YrException(Exception):
    pass

class WeatherHandler(xml.sax.handler.ContentHandler):
    """
    kilde: http://om.yr.no/verdata/xml/spesifikasjon/

    om.yr.no har hjelpesider, kontaktinformasjon og artiklar om dei siste endringane på yr.no.

    På www.yr.no finn du den vanlege yr.no-framsida med bl.a. dei siste nyheitssakene vi har publisert om vêr.
    Om yr.no

      Fakta om Yr.no

    Informasjon

      Vil du registrere badetemperaturer?
      Redaktøransvar på Yr
      Pressekontaktar for Yr
      Nettkamera
      Fakta om Yr
          yr.no 5 år: 2007-2012
          Prisar og utmerkingar til Yr
      Data Policy and Data Services
      Vilkår for bruk av innhald frå Yr

    Om varsla på yr.no

      Snøskred
          Hva betyr skredproblemene?
          Faregradskala for snøskred
      Slik forstår du varslene på Yr
          Tidssoner
          Slik utnytter du langtidsvarslene best
          Hvorfor varsles snø i millimeter?
          Sommerbyger er hodebry
          Nedbør
      Nedbørobservasjonar
      Kart
      Slik lagar vi varsla på yr.no
      Vêrsymbol på yr.no
          Vindpiler og -skala
          Effektiv temperatur
          Mørketidssymboler
      Hvor gode er værvarslene på yr.no?
      Radar
      Satellittbildene
      Tidsfaser i værutviklingen av ekstremvær
      Høgde over havet
      Klimastatistikk på yr.no

    Andre plattformer

      yr.no på iPhone
      yr.no på Android
      Beta.yr.no – nye nettsider tilpasset mobil
      Andre mobile «dingser»

    Arkiv

      september 2015
      april 2015
      desember 2014
      oktober 2014
      september 2014
      juli 2014
      juni 2014
      mai 2014
      april 2014
      februar 2014

    Emneord

    android badetemperatur Belgia beta.yr.no brett brukere Estland Finland Frankrike frie data Geonames Gibraltar hav og kyst iPad iPhone ISO3166 jerusalem Karibia kart kosovo kvalitet land mobil målestasjon måling måne nedbør OBS-varsel observasjon PDF radar sol sommerbyger stadnamn statistikk stilling-ledig symbol søk tekstvarsel utlandet varsel verdata verifikasjon Vind xml
    Spesifikasjon av XML-formatet i varsel.xml
    Få gratis vêrdata frå yr.no

      Informasjon om gratis vêrdata
      Information about the free weather data service
          “You have been blocked”
      Hvorfor er norske værdata gratis?
      Vilkår for bruk av gratis data frå Yr
      Vêrvarsel i XML-format
          Spesifikasjon av XML-formatet i varsel.xml
      Vêrvarsel i PHP-format
      Værdata i GRIB-format
      Javascript-varsel
      Gratis klimadata og observasjoner

    Denne sida forklarer innhaldet i XML-ane for yr.no.

    Du bør lese artikkelen Vêrvarsel i XML-format fyrst.

    Denne artikkelen forklarer innhaldet i vêrdata-XML-ane frå yr.no, f.eks. yr.no/sted/Norge/Oslo/Oslo/Blindern/varsel.xml og
    yr.no/sted/Norge/Oslo/Oslo/­Blindern/varsel_time_for_time.xml.

    Du må ha kjennskap til XML og programmering med XML for å forstå denne artikkelen.
    Location

    Noden har informasjon om offisielt stadnamn, type stad, land og tidssone. Timezone har namnet på tidssona og avvik i minutt samanlikna med UTC-tid. Alle tidspunkt er i lokal tid.

    Location/Location har informasjon om lengde-/breiddegrad, høgde over havet + informasjon om kva database yr.no har brukt for å plassere staden.
    Det er to hovuddatabaser som ligg bak yr.no: SSR frå Statens kartverk og Geonames (geonames.org).

    Ver merksam på at ein del av høgdene (altitude) som er spesifisert i XML-ane kjem frå høgdemodellar. D.v.s. at ikkje alle høgdene er heilt nøyaktige.
    Meta

    Noden har informasjon om når varselet er laga og cirkatidspunkt for neste oppdatering. Varsla blir oppdatert fleire gongar i døgeret, sjekk dei vanlege varselsidene for meir informasjon om dette.
    Links

    I fylgje retningslinene våre MÅ du lage lenke til URL-en som står spesifisert i <link id=»overview»>..

    Dei andre lenkene som er spesifisert i Links, kan du sjølv velje om du vil lenke opp eller ikkje.

    Framlegg til lenketekst:

      overview. Varsel for stadnamn på yr.no
      hourByhour. Time for time-varsel for på yr.no
      longTermForecast. Langtidsvarsel for stadnamn på yr.no
      radar. Værradar for stadnamn på yr.no

    Text

    Denne bolken inneheld tekstvarsel for staden. Dersom du har plass, bør du ta med denne teksten.

    Time from/to spesifiserer tidsintervallet kvart tekstvarsel gjeld for. Du finn den same informasjonen i Title (her er dagnamna spesifisert).

    location name inneheld namnet på området. Det er svært viktig at du tek med dette namnet, elles blir varselet delvis uforståeleg.

    Du bør merke tekstvarselet slik: «Meteorologens tekstvarsel for Buskerud for tirsdag». Har du dårleg plass, kan du forkorte til «Buskerud tirsdag» før den aktuelle teksten.
    Tabular

    I denne bolken finn du det vanlege varselet for punktet. Varselet er rekna ut nøyaktig for staden som er spesifisert i toppen av XML-en.
    Time from / to / period

    Dato og klokkeslett for intervallet varselet gjeld for. Alle tidspunkt er i lokal tid for staden du ser på (tidssoneinformasjonen er spesifisert i toppen av sida).

    Vi delar inn varsla i fire periodar:

      natt (vanlegvis kl 00-06)
      morgon (vanlegvis kl 06-12)
      dag (vanlegvis kl 12-18)
      kveld (vanlegvis kl 18-24)

    Dersom du berre skal vise eitt varsel per dag bør du bruke periode 2.

    Tidspunkta kan variere noko: India har f.eks. avvikande lokaltid, og der er varselet for periode 2 vanlegvis laga for 11:30 til 17:30, ikkje 12-18.

    Symbola og nedbøren gjeld for heile intervallet. Temperatur og vind gjeld for det fyrste tidspunktet i intervallet.
    Symbol

    Symbola er spesifisert med symbolnummer og symbolnamn. Det er attributten «numberEx» som skal brukas. Denne er ny frå 27. mai 2014 og gjer eit meir detaljert nedbørsymbol enn attributten «number».

    Symbola er tilgjengelege i PNG-format i 5 storleikar + SVG. Katalogstrukturen er slik og namnet angjer storleiken i pixlar:

      sym/b30
          /mf
      sym/b38
          /mf
      sym/b48
          /mf
      sym/b100
          /mf
      sym/b200
          /mf
      sym/svg
          /mf

    Nedbørsymbol kjem i 3 variantar avhengig, av kor mykje nedbør som blir varsla/observert.

    Regn:

    symbolsymbolsymbol

    Sludd:

    symbolsymbolsymbol

    Snø:

    symbolsymbolsymbol

    Desse symbola kan kombineres med andre elementar som sol, måne, mørketid og lyn og utgjer tilsaman 83 vêrsymbol totalt.
    I tillegg brukar Yr også månefasar i symbola (totalt gjer dette over 13.000 filer). Hvis du ynskjer å ta dei i bruk, kan du hente ut id’en i attributten «var».

    F.eks. (mf/40n.73/)
    Du finn eit oversyn over alle hovedsymbola våre (med nummer) på http://om.yr.no/forklaring/symbol/.
    Precipitation

    Nedbørsvarsel i millimeter. Dersom du skal vise nedbøren direkte, bør du runde av og ikkje vise desimalar.

    Kvifor blir snø varsla i millimeter nedbør?
    WindDirection

    Vindretning i gradar, med vindretningskode og tekst. Kodane er engelske, vindretningane på det aktuelle språket XML-en gjeld for.

    Vindretningskodar som er i bruk: N, NNE, NE, ENE, E, ESE, SE, SSE, S, SSW, SW, WSW, W, WNW, NW, NNW.

    Vindpiler og -skala.
    WindSpeed

    Vindstyrke i meter per sekund (m/s) med tilhøyrande Beufort-namn.

    Vindpiler og -skala.
    Temperature

    Temperaturvarsel i Celsius.

    Dersom du skal vise temperaturen direkte, må du runde av og ikkje vise desimalar.
    Pressure

    Luftrykk i hektopascal ved havnivå.

    Dersom du skal vise lufttrykket direkte, må du runde av og ikkje vise desimalar.
    Observations

    Syner siste observasjonar frå dei tre nærmaste målestasjonane. Ver merksam på at ikkje alle målestasjonar måler alle parametre som temperatur, nedbør, vind og symbol. Nokre gjer til dømes berre nedbørsmengde.

    Attributten «distance» er avstanden frå punktet du hentar varsel for, til punktet kor målestasjonen står.
    Symbol

    Same som i «Tabular»
    Temperature

    Gjer målt temperatur i Celsius, med ein desimal oppløysing.
    WindDirection og WindSpeed

    Same som i «Tabluar»
    Sist oppdatert 12. mai 2014 kl 14:09
    """
    def __init__(self):
        self.time_forecasts = []
        self.in_tabular = False
        self.in_credit = False
        self.time = Time()
        self.credit = Credit()

    def startElement(self, name, attrs):

        if name == 'tabular':
            self.in_tabular = True
        elif name == 'credit':
            self.in_credit = True
        elif self.in_tabular:
            if name == 'time':
                self.time = Time()
                self.time.start = attrs.get('from', '')
                self.time.to = attrs.get('to', '')
                self.time.period = int(attrs.get('period', '9999999'))
            elif name == 'symbol':
                self.time.symbol_number = int(attrs.get('number', '0'))
                self.time.symbol_name = attrs.get('name', '')
                self.time.symbol_number_ex = int(attrs.get('numberEx', '0'))
            elif name == 'temperature':
                self.time.temperature = int(attrs.get('value', '0'))
        elif self.in_credit:
            if name == 'link':
                self.credit.text = attrs.get('text', '')
                self.credit.url = attrs.get('url', '')

    def endElement(self, name):
        if name == 'tabular':
            self.in_tabular = False
        elif name == 'credit':
            self.in_credit = False
        elif name == 'time' and self.in_tabular:
            self.time_forecasts.append(self.time)


def _parse_forecast(raw):
    sax_xmlreader = xml.sax.make_parser()
    stream = cStringIO.StringIO(raw)
    try:
        weather_handler = WeatherHandler()
        sax_xmlreader.setContentHandler(weather_handler)
        sax_xmlreader.parse(stream)
        stream.close()
        wr = WeatherResponse()
        wr.credit = weather_handler.credit
        wr.time_forecasts = weather_handler.time_forecasts
        return wr
    except xml.sax.SAXParseException as e:
        logger.error(str(e))
        raise YrException(e)
    return None


def lookup_forecast_for_postnummer(postnummer):
    response_body, status_code = fetch_forecast_for_postnummer(postnummer)
    if status_code == 200:
        return _parse_forecast(response_body)
    else:
        return WeatherResponse()


def fetch_forecast_for_postnummer(postnummer):
    postnummer_s = postnummer
    source_url_template = 'http://yr.no/sted/Norge/postnummer/{postnummer}/varsel.xml'
    source_url = source_url_template.format(postnummer=postnummer_s)
    logger.debug(source_url)
    request = urllib2.Request(source_url)
    try:
        response = urllib2.urlopen(request)
        response_body = response.read()
        status_code = response.getcode()
        return response_body, status_code
    except urllib2.HTTPError as e:
        message = str(e)
        logger.error(message)
        return None, e.code
    except urllib2.URLError as e:
        message = str(e)
        logger.error(message)
        raise YrException(e)