from datetime import datetime
import json

import click
import requests
from bs4 import BeautifulSoup


URL = ('http://www2.vvs.de/vvs/widget/XML_DM_REQUEST?zocationServerActive=1'
       '&lsShowTrainsExplicit1&stateless=1&language=de&SpEncId=0&anySigWhenPerfectNoOtherMatches=1'
       '&depArr=departure&type_dm=any&anyObjFilter_dm=2&deleteAssignedStops=1&useRealtime=1'
       '&mode=direct&dmLineSelectionAll=1&name_dm={station_id}&itdDateYear={year}&itdDateMonth={month}'
       '&itdDateDay={day}&itdTimeHour={hour}&itdTimeMinute={minute}&limit=50')

TIME_FORMAT = '%Y-%m-%d %H:%M'


@click.group()
def main():
    pass


@main.command()
@click.argument('station_id')
@click.option('--direction', '-d', multiple=True,
              help="Filter departures by those in a certain direction")
def scrape(station_id, direction):
    direction = [d.lower() for d in direction]
    now = datetime.now()
    ctx = {
        'station_id': station_id,
        'year': now.year,
        'month': now.month,
        'day': now.day,
        'hour': now.hour,
        'minute': now.minute
    }
    url = URL.format(**ctx)
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    result = []
    for departure in soup.find_all('itddeparture'):
        if direction and departure.itdservingline['direction'].lower() not in direction:
            continue
        dt = datetime(int(departure.itddatetime.itddate['year']),
                      int(departure.itddatetime.itddate['month']),
                      int(departure.itddatetime.itddate['day']),
                      int(departure.itddatetime.itdtime['hour']),
                      int(departure.itddatetime.itdtime['minute']))
        result.append(dt.strftime(TIME_FORMAT))
    click.echo(json.dumps(result))


@main.command()
@click.argument('file', type=click.File('r'))
@click.option('--format', '-f', help="Format string for datetimes")
@click.option('--limit', '-l', type=int, default=3,
              help="Limit the number of departure times displayed")
def display(file, format, limit):
    departures = [datetime.strptime(d, TIME_FORMAT) for d in json.load(file)[:limit]]
    if format:
        click.echo(', '.join([d.strftime(format) for d in departures]))
    else:
        now = datetime.now()
        deltas = [str(int((d - now).seconds / 60)) for d in departures]
        click.echo("In {} min".format(', '.join(deltas)))
