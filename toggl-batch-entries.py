
import sys
import json
import requests
from base64 import b64encode
from datetime import datetime

cred = b'email:password'

headers = {
    "Content-Type": "application/json",
    'Authorization': 'Basic ' + b64encode(cred).decode('utf-8')
}

def parse_time(string):
    time = []
    sep = 0
    for i in range(len(string)):
        # TODO: make parsing more fault tolerant
        c = string[i]
        if c == 'h':
            time.insert(0,string[sep:i])
            sep = i
        elif c == 'm':
            time.insert(1,string[sep+1:i])
            sep = i
        elif c == 's':
            time.insert(2,string[sep+1:i])
            sep = i
        print(time)
    return [int(i) for i in time]

def post_entry(start,end,description):
    # %Y-%m-%dT%H:%M:%S' (lacking timezone, dunno how to write)
    # "2020-01-11T07:58:58.000-03:00"
    # TODO: remove hard-coded timezone 
    startstr = start.isoformat() + '-03:00'
    duration = (end - start).total_seconds()
    payload = {
        "time_entry": {
            "wid": 1628116,
            "description": description,
            "duration": duration, 
            "start": startstr,
            "created_with": "command line utility"
        }
    }
    
    r = requests.post("https://www.toggl.com/api/v8/time_entries",
                      data=json.dumps(payload),
                      headers=headers)
    print(r.text)
    return

def main(args):
    year = int()
    month = int()
    day = int()

    with open(args[1],'r') as f:
        # TODO: encapsulate file reading in function
        # TODO: modularize parsing and add syntax sugar
        # TODO: parse more efficiently
        text = f.read()
        lines = text.split('\n')
        dayloop = False

        for line in lines:
            if len(line) == 0:
                dayloop = False

            elif line[0] == '#':
                dayloop = True
                year, month, day = [int(i) for i in line[2:].split('/')]                
            
            elif dayloop:
                data = [i.strip() for i in line.split('-')]
                start = datetime(year, month, day, *parse_time(data[0]))
                end = datetime(year, month, day, *parse_time(data[1]))
                description = data[2].strip('"')
                
                post_entry(start, end, description)

if __name__ == '__main__':
    main(sys.argv)
    # start = datetime(2020,1,11,9,10)
    # end = datetime(2020,1,11,11,10)
    # post_entry(start, end, "teste")
