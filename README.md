# Fantasy Football Draft Tool
This tool will print the top 10 undrafted players in each position given a ranking of players in each position pasted from thehuddle.com cheatsheets.

# Installation
Install python 3.10  
Install python3.10-venv:
```
sudo apt install python3.10-venv
```
Create and activate python virtual env:
```
python -m venv create .venv
source .venv/bin/activate
```
Install requests package:
```
pip install requests
```

# Usage
In order to authenticate with the MyFantasyLeague API a username and password are required. The tool looks for these in the `FF_USER` and `FF_PASSWORD` env vars. These can be set using:
```
export FF_USER=<username>
export FF_PASSWORD=<password>
```
Run the tool using:
```
python3 ff-draft.py
```