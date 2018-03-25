import configparser
import requests

# Load config
config = configparser.ConfigParser()
config.read("config.ini")

# Api url
API_ADDR = "http://{0}:{1}".format(
    config["API"]["host"],
    config["API"]["port"],
)

# Load versions
WEB_VER = config["Website"]["version"]
try: CORE_VER = requests.get(API_ADDR+"/version").text 
except: CORE_VER = "Error"
try: PLUGIN_VER = open("static/plugin/ver").read() 
except: PLUGIN_VER = "Error"

