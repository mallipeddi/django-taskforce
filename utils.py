from django.conf import settings

def get_server_loc():
    if hasattr(settings, 'TASKFORCE_SERVER'):
        address, port = settings.TASKFORCE_SERVER.split(':')
        port = int(port)
    else:
        address = '127.0.0.1'
        port = 9000
    return address, port

def get_server_base_uri():
    address, port = get_server_loc()
    return "http://%s:%d" % (address, port)