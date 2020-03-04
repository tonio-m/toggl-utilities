import sys
import json
import pprint
import requests
import configparser
from base64 import b64encode
from datetime import datetime

workspace_id = 1628116
cred = b''

headers = {
    "Content-Type": "application/json",
    'Authorization': 'Basic ' + b64encode(cred).decode('utf-8')
}

pp = pprint.PrettyPrinter()

def parse_time(timespan,date):
    date = [s.strip() for s in date.split('/')]

    timespan = [s.strip() for s in timespan.split('-')]
    timespan_datetime = [] 

    for time in timespan:
        time = time.replace('h',':').replace('m',':').replace('s',':')
        time = time.split(':')
        time = list(filter(lambda s: s != '',time))
        datetime_ = [int(s) for s in [*date,*time]]

        timespan_datetime.append(datetime(*datetime_))
        
    return timespan_datetime

def post_entry(start,end,description):
    # TODO: remove hard-coded timezone 
    startstr = start.isoformat() + '-03:00'
    duration = (end - start).total_seconds()
    payload = {
        "time_entry": {
            "wid": workspace_id,
            "description": description,
            "duration": duration, 
            "start": startstr,
            "created_with": "python script"
        }
    }
    
    r = requests.post("https://www.toggl.com/api/v8/time_entries",
                      data=json.dumps(payload),
                      headers=headers)
    pp.pprint(json.loads(r.text))
    return

def main(filename):
    config = configparser.ConfigParser()

    with open(filename,'r') as f:
        config.read_file(f)

    all_entries = []
    dates = list(config.keys())[1:]
    
    for date in dates:
        for time, description in dict(config[date]).items():
            all_entries.append((*parse_time(time,date),description))
            
    for entry in all_entries:
        post_entry(*entry)

if __name__ == '__main__':
    main(sys.argv[1])
    # start = datetime(2020,1,11,9,10)
    # end = datetime(2020,1,11,11,10)
    # post_entry(start, end, "teste")
