import json
import box

# Load config
with open('res/conf.json') as f:
    cfg = json.load(f)

config = box.Box(cfg['configs'][cfg['conf_name']])
