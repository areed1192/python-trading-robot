# Python Trading Robot

## Overview

A trading robot written in Python that is able to run automated strategies using a technical analysis.

## Setup

After you clone the repo, make sure to run the setup file, so you can install any dependencies you may need. To run the `setup.py` file, run the following command in your terminal.

```console
pip install -e .
```

## Running the Robot

To run the robot you'll need to provide a few pieces of information from your TD Ameritrade Developer account. The following items are need for authentication:

- Client ID: Also, called your consumer key, this was provided when you registered an app with the TD Ameritrade Developer platform. An example of a clien ID could look like the following MMMMYYYYYA6444VXXXXBBJC3DOOOO.
- Redirect URI: Also called the callbakc URL or redirect URL, this was specified by you when you regiestered your app with the TD Ameritrade Developer platform. Here is an example of a redirect URI <https://localhost/mycallback>
- Credentials Path: This is a file path that will point to a JSON file where your state info will be saved. Keep in mind that it's okay if it points to a non-existing file as once you run the script the file will be auto generated. For example, if I want my state info to be saved to my desktop, then it would look like the following: `C:\Users\Desktop\ts_state.json`

Once you've identfied those pieces of info, you can run the robot. Here is a simple example that will create a new instance of it:

```python
from pyrobot.robot import PyRobot

# Initalize the robot
trading_robot = PyRobot(
    client_id='XXXXXX111111YYYY22',
    redirect_uri='https://localhost/mycallback',
    credentials_path='path/to/td_state.json'
)
```
