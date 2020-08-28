# Python Trading Robot

## Table of Contents

- [Overview](#overview)
- [Setup](#setup)
- [Usage](#usage)
- [Support These Projects](#support-these-projects)

## Overview

Current Version: **0.1.0**

A trading robot written in Python that can run automated strategies using a technical analysis.
The robot is designed to mimic a few common scenarios:

1. Maintaining a portfolio of multiple instruments. The `Portfolio` object will be able
   to calculate common risk metrics related to a portfolio and give real-time feedback
   as you trade.

2. Define an order that can be used to trade a financial instrument. With the `Trade` object,
   you can define simple or even complex orders using Python. These orders will also help similify
   common scenarios like defining both a take profit and stop loss at the same time.

3. A real-time data table that includes both historical and real-time prices as they change. The
   `StockFrame` will make the process of storing your data easy and quick. Additionally, it will be
   setup so that way you can easily select your financial data as it comes in and do further analysis
   if needed.

4. Define and calculate indicators using both historical and real-time prices. The `Indicator` object
   will help you easily define the input of your indicators, calculate them, and then update their values
   as new prices come.

## Setup

**Setup - Local Install:**

If you are planning to make modifications to this project or you would like to access it
before it has been indexed on `PyPi`. I would recommend you either install this project
in `editable` mode or do a `local install`. For those of you, who want to make modifications
to this project. I would recommend you install the library in `editable` mode.

If you want to install the library in `editable` mode, make sure to run the `setup.py`
file, so you can install any dependencies you may need. To run the `setup.py` file,
run the following command in your terminal.

```console
pip install -e .
```

If you don't plan to make any modifications to the project but still want to use it across
your different projects, then do a local install.

```console
pip install .
```

This will install all the dependencies listed in the `setup.py` file. Once done
you can use the library wherever you want.

**Setup - PyPi Install:**

The project can be found at PyPI, if you'd like to view the project please use this
[link](https://pypi.org/project/python-trading-robot/). To **install** the library,
run the following command from the terminal.

```bash
pip install python-trading-robot
```

**Setup - PyPi Upgrade:**

To **upgrade** the library, run the following command from the terminal.

```bash
pip install --upgrade python-trading-robot
```

## Usage

To run the robot, you will need to provide a few pieces of information from your TD Ameritrade Developer account.
The following items are need for authentication:

- Client ID: Also, called your consumer key, this was provided when you registered an app with the TD Ameritrade
  Developer platform. An example of a client ID could look like the following `MMMMYYYYYA6444VXXXXBBJC3DOOOO`.

- Redirect URI: Also called the callbakc URL or redirect URL, this was specified by you when you regiestered your app with
  the TD Ameritrade Developer platform. Here is an example of a redirect URI <https://localhost/mycallback>

- Credentials Path: This is a file path that will point to a JSON file where your state info will be saved. Keep in mind
  that it is okay if it points to a non-existing file as once you run the script the file will be auto generated. For example,
  if I want my state info to be saved to my desktop, then it would look like the following: `C:\Users\Desktop\ts_state.json`

Once you've identfied those pieces of info, you can run the robot. Here is a simple example that will create a new instance
of it:

```python
from pyrobot.robot import PyRobot

# Initialize the robot
trading_robot = PyRobot(
    client_id='XXXXXX111111YYYY22',
    redirect_uri='https://localhost/mycallback',
    credentials_path='path/to/td_state.json'
)
```

For more detailed examples, go to the `trading_robot.py` file to see an example of how to use the library along with all
the different objects inside.

## Support these Projects

**Patreon:**
Help support this project and future projects by donating to my [Patreon Page](https://www.patreon.com/sigmacoding). I'm always
looking to add more content for individuals like yourself, unfortuantely some of the APIs I would require me to pay monthly fees.

**YouTube:**
If you'd like to watch more of my content, feel free to visit my YouTube channel [Sigma Coding](https://www.youtube.com/c/SigmaCoding).

<!-- **Hire Me:**
If you have a project, you think I can help you with feel free to reach out at [coding.sigma@gmail.com](mailto:coding.sigma@gmail.com?subject=[GitHub]%20Project%20Proposal) or fill out the [contract request form](https://forms.office.com/Pages/ResponsePage.aspx?id=ZwOBErInsUGliXx0Yo2VfcCSWZSwW25Es3vPV2veU0pUMUs5MUc2STkzSzVQMFNDVlI5NjJVNjREUi4u) -->
