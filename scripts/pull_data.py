import argparse
import configparser
import datetime
from dateutil import parser
import json
import logging
import os

from garminconnect import Garmin


DEFAULT_OUT_DIR = os.path.abspath('../data')
JSON_OUT_DIR = os.path.join(DEFAULT_OUT_DIR, "jsons", "{activity}")
TODAY = datetime.datetime.now()

API_MAP = json.load(open(os.path.abspath('../api_map.json')))

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'activities', nargs='+',
        help="Activities to grab stats from Garmin Connect"
    )
    parser.add_argument(
        '--username', type=str,
        help="Garmin username", default=None
    )
    parser.add_argument(
        '--password', type=str, 
        help="Garmin password", default=None
    )
    parser.add_argument(
        '--ini', type=str,
        help="Location of ini file with Garmin username and password",
        default=None
    )
    parser.add_argument(
        '--since', type=str,
        help='Date since to get stats from in format MM/DD/YYYY',
        default=None
    )
    parser.add_argument(
        '--days', type=int,
        help="Number of days since today (inclusive) for which to get data. DEFAULT: 7",
        default=7
    )

    return parser.parse_args()


def get_activity(client: Garmin, activity: str, date: str) -> str:
    """
    Query Garmin Connect for daily stats of a specific activity

    Parameters
    ----------
    client: Garmin
        A Garmin client object from the `garminconnect` package
    activity: str
        String representation of activity to get stats for
    date: str
        Isoformat string version of date for which to get activity stats

    Returns
    -------
    str
        Path to output json with stats
    """
    # use Garmin api endpoint to get activity for certain day
    api_endpoint = getattr(client, API_MAP.get(activity))
    result = api_endpoint(date)

    json_dir = JSON_OUT_DIR.format(activity=activity)
    out_path = os.path.join(json_dir, f"{date}.json")
    os.makedirs(json_dir, exist_ok=True)

    logging.info(f"Saving `{activity}` data for {date} to `{out_path}`")
    with open(out_path, 'w') as f:
        json.dump(result, f)

    return out_path


def pull_data(activities: list,
              days: int,
              since: str = None,  
              username: str = None, 
              password: str = None):
    
    garmin_client = Garmin(email=username, password=password)
    garmin_client.login()

    if since:
        since_date = parser.parse(since)
        date_list = [
            TODAY.date() - datetime.timedelta(days=x) 
            for x in range((TODAY - since_date).days + 1)
        ]
    else:
        date_list = [
            TODAY.date() - datetime.timedelta(days=x) 
            for x in range(days)
        ]

    activity_jsons = {}
    for date in date_list:
        for activity in activities:
            output_json = get_activity(garmin_client, activity, date.isoformat())
            activity_jsons.update({activity: activity_jsons.get(activity, []) + [output_json]})

    results_json_loc = os.path.join(os.path.abspath('../data'), 
                                    f"{TODAY.isoformat()}_results.json")
    logging.info(f"Saving results to `{results_json_loc}`")
    json.dump(activity_jsons, open(results_json_loc, 'w'))


if __name__=='__main__':
    logging.basicConfig(level=logging.INFO)
    args = get_args()
    arg_dict = vars(args)

    if not args.username and not args.password:
        config = configparser.ConfigParser()
        ini_file = arg_dict.pop('ini')
        if ini_file:
            config.read(ini_file)
        else:
            config.read(r"../auth.ini")

        arg_dict.update({
            'username': str(config['auth']['username']),
            'password': str(config['auth']['password'])
        })

    pull_data(**arg_dict)