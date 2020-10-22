import configparser

# Parsing settings
config = configparser.ConfigParser()
config.read('../settings.ini')
ITAD_KEY = config['keys']['itad']
STEAM_ID = config['ids']['steam']
PRICE_CUT = config.getint('misc', 'price_level')
ACCOUNT_SID = config['sms']['account_sid']
AUTH_TOKEN = config['sms']['auth_token']
PHONE_NUM = config['sms']['phone_number']
TWILIO_NUM = config['sms']['twilio_number']