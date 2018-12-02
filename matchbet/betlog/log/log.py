import logging
import platform
from pathlib import Path

import os

# logger instance
server_logger = logging.getLogger('server_logger')

log_name = 'bet_server.log'

log_path = '{}/{}'.format(os.getcwd(), log_name)


# retrieve all log messages
def get_log():
    with open(log_path) as f:
        return list(reversed(f.readlines())) # return reversed list so newest at top

# get [n] most recent log messages
def get_log_recent(n=5):
    return get_log()[slice(n)]

