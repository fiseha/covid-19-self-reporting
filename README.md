# COVID-19 Self Assessment and Reporting

## Introduction

These scripts will interact the python-telegram-bot with Google Sheet's API and create a simple Voluntary Self Reporting System.

The python-telegram-bot library is used as a base to create a bot, then the data collected will be piped to a Google Sheet, that can be used to create a data analysis and visualisation dashboard of your liking.

## How to have it working on your end

If you have Python version 3.3 or above installed, go into the folder
and run:

`python -m venv cov_env`

This will create a new virtual environment for you to play with. More about Virtual Enironments [here](https://docs.python.org/3/tutorial/venv.html).

Using your new virtual environment install the following python libraries

1. The Google Sheets API

   `cov_env/bin/pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`

   [Check offical site for more info](https://developers.google.com/sheets/api/quickstart/python)

2. The Pythong Telegram Bot

   `cov_env/bin/pip install python-telegram-bot`

   [Check offical site for more info](https://python-telegram-bot.org/)

Your script need to be authoried and a `token.pickele` file should be generated. Before doing so you can have the bot working but not the data recording functionality.

After the packages installed and you change the parameters inside the `config.ini` (important) run the `quickstart.py` to authorize your script to read/write a google sheet value.

`cov_env/bin/python quickstart.py`

This will open up a browser for you to authorize a google account to edit one of your prefered google sheets. `toke.pickle` and `credentials.json` files will be generated.

Once all set up run the `telegram_bot.py` to start a telegram server and start interacting with your bot. Make sure you created your bot first and get a telegram TOKEN from the `botfather` [All about telegram bots](https://core.telegram.org/bots)

(Here is a sample spreadhseet file from my test of the scripts)[https://docs.google.com/spreadsheets/d/1IgBlza2FAX96AoI47G20gK1t93ya3xAjlzt23jaGPFk/edit?usp=sharing]
