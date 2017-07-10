# Command context class
class CommandContext(object):
    name = ""
    message = None
    start_time = 0
    args = []
    database = None
    cursor = None
    client_server_data = []
    client = None