# Pokemon Python
Pokemon Python is a Python tools for get all the data about Pokemon.

## Installation
Using MacOS, install Python3 and Pip3 using Homebrew

Install [Homebrew](ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)")
Use Homebrew to install Python3
```bash
brew install python3
```

Pip3 already installed together with Python3, check already installed:
```bash
which python3 pip3
```

Get API with using requests:
```bash
pip3 install requests
```

## Usage
```python
import requests
import enquiries
import os
import json
import datetime
import glob

## Documentation
Open Terminal and run
```bash
python3 pokemon.py
```

This Pokemon python have 3 Menu:
1. Save Pokemon: For save pokemon data based on ID or name of the Pokemon
2. Show Pokemon: Show pokemon data based on ID or name, if its never stored before, it will show status that the pokemon is being stored, and then show data. If its already stored, then it will only show data.
3. Display Pokemon Data: Show all stored Pokemon data.

All Pokemon data that stored for 7 days, will be removed and it will automatically save all the pokemon data that was stored before into the file.