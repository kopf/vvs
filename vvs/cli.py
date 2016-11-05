from datetime import datetime
import json
import time

import click
import requests
from bs4 import BeautifulSoup


URL = ('http://www2.vvs.de/vvs/widget/XML_DM_REQUEST?zocationServerActive=1'
       '&lsShowTrainsExplicit1&stateless=1&language=de&SpEncId=0&anySigWhenPerfectNoOtherMatches=1'
       '&depArr=departure&type_dm=any&anyObjFilter_dm=2&deleteAssignedStops=1&useRealtime=1'
       '&mode=direct&dmLineSelectionAll=1&name_dm={station_id}&itdDateYear={year}&itdDateMonth={month}'
       '&itdDateDay={day}&itdTimeHour={hour}&itdTimeMinute={minute}&limit=50')


@click.group()
def main():
    pass


@main.command()
@click.argument('station_id')
@click.option('--direction', '-d', multiple=True,
              help="Filter departures by those in a certain direction")
def scrape(station_id, direction):
    direction = [d.lower() for d in direction]
    ctx = {
        'station_id': station_id,
        'year': time.strftime('%y'),
        'month': time.strftime('%m'),
        'day': time.strftime('%d'),
        'hour': time.strftime('%H'),
        'minute': time.strftime('%M')
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
        result.append(dt.strftime('%Y-%m-%d %H:%M'))
    click.echo(json.dumps(result))
