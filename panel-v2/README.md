# TradeHub web interface (v2.0)

## Install (CentOS 7.x, with initial setup)
1. Freeze libraries
```
venv/bin/python3 -m pip freeze > res/req.txt
```
2. Copy sources to server
```
rsync -avz ../panel-v2 root@<host>:~/
```
3. Connect to server
4. Go to project dir
```
cd panel-v2
```
5. Install requirements
```
pip3.6 install -r res/req.txt
```
6. Change config to release
```
nano res/conf.json
```
7. Run
```
sh scripts/start.sh
```

## Cautions
Panel is using parent accounts control.  
This method must be available on parent:
```
<parent>/openapi/user?username=...&password...
```
Also core part is used through custom cache layer