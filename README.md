# ebc-health
Research repo looking into health data collected by my Garmin watch

## python-garminconnect
Install [python-garminconnect](https://github.com/cyberjunky/python-garminconnect) to use API to talk to Garmin Connect:


## Usage
### Scripts

`pull_data.py`

PURPOSE: Use `garminconnect` API to retrieve stats for any activity of interest. Stats are saved to a json file under the `data` directory of this repo. Additional metadata json is saved under the same directory. 

HOW TO: Change directory to `scripts`. Run `python pull_data.py` wit the following usage: 
```
usage: pull_data.py [-h] [--username USERNAME] [--password PASSWORD] [--ini INI] [--days DAYS]
                    activities [activities ...]

positional arguments:
  activities           Activities to grab stats from Garmin Connect

optional arguments:
  -h, --help           show this help message and exit
  --username USERNAME  Garmin username
  --password PASSWORD  Garmin password
  --ini INI            Location of ini file with Garmin username and password
  --days DAYS          Number of days since today (inclusive) for which to get data. DEFAULT: 7
```