import logging
from os.path import exists

# logger instance
server_logger = logging.getLogger('server_logger')

# path to store log file
log_path = '/var/log/bet_server.log'

# retrieve all log messages
def get_log():
    if not exists(log_path):
        return '' # file does not exist
    with open(log_path) as f:
        return list(reversed(f.readlines())) # return reversed list so newest at top

# get [n] most recent log messages
def get_log_recent(n=5):
    return get_log()[slice(n)]

