# Tradehub (private project)

## Map
1. Overview
2. Install
3. Supported markets

## Overview
Private project, created for arbitrage trading with plugin/table. Main task: compare markets and show price difference in percents(include commission).

## Install (CentOS 7.x)

### Core
1. Copy sources to server
```
rsync -avz core root@<host>:~/
```
2. Install IUS
```
curl http://setup.ius.io | sh
```
3. Install Python and deps
```
yum groupinstall -y development
yum -y install python36u python36u-pip python36u-devel
pip3.6 install -r core/res/requirements.txt
```
4. Edit config
```
core/res/conf.json
```
5. Run
```
cd core
nohup python3.6 src &
```

### Panel (if the server is the same)
1. Copy sources to server
```
rsync -avz panel root@<host>:~/
```
2. Install deps
```
pip3.6 install -r panel/requirements.txt
```
3. Run
```
cd panel
sh scripts/start.sh
```

## Supported markets

### Parsers
| CSGO | H1Z1 | PUBG |
| - | - | - |
| c5game.com(purchase) | c5game.com(purchase) | c5game.com(purchase) |
| c5game.com(sale) | c5game.com(sale) | c5game.com(sale) |
| tradeit.gg | tradeit.gg | tradeit.gg |
| opskins.com | opskins.com | opskins.com |
| swap.gg | swap.gg | swap.gg |
| loot.farm |  | loot.farm  |
| cs.money |  |  |
| cs.deals |  |  |
| csgosell.com |  |  |
| skinsjar.com |  |  |
| tradeskinsfast.com |  |  |

### Plugin
| Markets |
| - |
| cs.money |
| cs.deals |
| loot.farm |
| skinsjar.com |
| tradeskinsfast.com |
| tradeit.gg |