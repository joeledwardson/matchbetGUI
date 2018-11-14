import logging
import platform
from pathlib import Path

# logger instance
server_logger = logging.getLogger('server_logger')

log_name = 'bet_server.log'

# path to store log file
if platform.system() == 'Windows':
    log_path = '{}\{}'.format(Path.home(), log_name)
elif platform.system() in ['Linux', 'Ubuntu']:
    log_path = '/home/pi/matchbet/{}'.format(log_name)
else:
    raise Exception('platform "{}" not recognised'.format(platform.system()))

# retrieve all log messages
def get_log():
    with open(log_path) as f:
        return list(reversed(f.readlines())) # return reversed list so newest at top

# get [n] most recent log messages
def get_log_recent(n=5):
    return get_log()[slice(n)]

