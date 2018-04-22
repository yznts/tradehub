# Tradehub (private project)


## Map
1. [Overview](##overview)
2. [Server setup](##server-setup-(centos-7.x))
3. [Supported markets](##supported-markets)


## Overview
Private project, created for arbitrage trading with plugin/table. Main task: compare markets and show price difference in percents(include commission).


## Server setup (CentOS 7.x)
1. Install IUS
```
curl http://setup.ius.io | sh
```
2. Install Python and deps
```
yum groupinstall -y development
yum -y install python36u python36u-pip python36u-devel
```


## Supported markets

### Parsers
| CSGO | H1Z1 | PUBG | DOTA2 |
| - | - | - | - |
| c5game.com(purchase) | c5game.com(purchase) | c5game.com(purchase) | bitskins.com |
| c5game.com(sale) | c5game.com(sale) | c5game.com(sale) | dota.money |
| tradeit.gg | tradeit.gg | tradeit.gg | opskins.com |
| opskins.com | opskins.com | opskins.com | |
| swap.gg | swap.gg | swap.gg | |
| loot.farm |  | loot.farm  | |
| cs.money |  |  | |
| cs.deals |  |  | |
| csgosell.com |  |  | |
| skinsjar.com |  |  | |
| tradeskinsfast.com |  |  | |

### Plugin
| Markets |
| - |
| cs.money |
| cs.deals |
| loot.farm |
| skinsjar.com |
| tradeskinsfast.com |
| tradeit.gg |