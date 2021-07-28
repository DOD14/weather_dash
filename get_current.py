import argparse
import configparser
import requests
import json

# use argument parser to get path of config file
parser = argparse.ArgumentParser()
parser.add_argument('--config', '-c', help='Path to file where user configuration is stored')
args = parser.parse_args()

# read config file
config = configparser.ConfigParser()
config.read(args.config)
api_key = config['API']['api_key']
city_code = config['API']['city_code']

# construct request url with city code and api key
url = "http://dataservice.accuweather.com/currentconditions/v1/%s?apikey=%s&details=true" % (city_code, api_key)

# process response
try:
    response = requests.get(url)
    data = json.loads(response.text)
    print(data)
    requests_remaining = response.headers['RateLimit-Remaining']
    print('[+] Requests remaining for today: ' + requests_remaining)
except exception as e:
    print('[!] error: ' + e)

# save downloaded data as json
with open('data.json', 'w') as outfile:
    json.dump(data, outfile)
