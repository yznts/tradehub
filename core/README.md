# Core

## Map
1. Install
2. Architecture

## Install
1. Copy source to server
```
rsync -avz --exclude=venv tradehub root@<host>:~/
```
2. Go to core directory
```
cd tradehub/core
```
3. Install dependencies
```
pip3 install res/requirements.txt
```
4. Edit config
```
editor res/conf.json
```
4. Entry command
```
python3 src
```

## Architecture
Entry point - src/\__main__.py  
Core - process-based application. Processes types: cache_layer, legacy_api, parser_wrapper.  
**cache_layer** - created for comfortable and fast storing cached info.  
**legacy_api** - backport for plugin support.  
**parser_wrapper** - created for abstracted items processing.  
Parsers are stored in src/parsers and separated by type.  
All processes are inited in \__main__.py  
