import strings as s
from mcserver_interface import VANILLA, FORGE, BEDROCK, CREATIVE, svr_online, send_command, svr_start

# Aux

def server_type(string):
    if string == "vanilla": return VANILLA
    elif string == "forge": return FORGE
    elif string == "bedrock": return BEDROCK
    elif string == "creative": return CREATIVE
    return -1

def validate_server_permissions(svr_type, perms):
    return 'a' in perms or\
        (svr_type == "vanilla" and 's' in perms) or\
        (svr_type == "bedrock" and 'b' in perms)

def validate_pu_command(auth, perms, admin):
    return admin or (('o' not in perms and 'a' not in perms) and (perms in auth))

# Admin commands

def add_p_user(**kwargs):
    receiver, permissions = kwargs['message']
    if not validate_pu_command(kwargs['perms'], permissions, kwargs['admin']):
        return s.UNAUTHORIZED
    if kwargs['config'].add_p_user(receiver,permissions):
        resp = s.PU_ADD.format(kwargs['message'][0])
        print("Added {}".format(kwargs['message']))
    else: resp = s.PU_EXISTS
    kwargs['config'].save_p_users()
    return resp

def remove_p_user(**kwargs):
    receiver, _ = kwargs['message']
    permissions = kwargs['config'].get_p_user(receiver)
    if not validate_pu_command(kwargs['perms'], permissions, kwargs['admin']):
        return s.UNAUTHORIZED
    if kwargs['config'].remove_p_user(receiver):
        resp = s.PU_DEL.format(kwargs['message'][0])
        print("Removed {}".format(kwargs['message']))
    else: resp = s.PU_NOT_FOUND
    kwargs['config'].save_p_users()
    return resp

def check_p_user(**kwargs):
    receiver, _ = kwargs['message']
    p = kwargs['config'].get_p_user(receiver)
    if len(p) > 0:
        resp = s.PU_LIST.format(p)
    else: resp = s.PU_NONE
    return resp

# Power user commands

def start_server(**kwargs):
    svr_type = server_type(kwargs["message"])
    if svr_online()[svr_type]:
        return s.SVR_ONLINE
    svr_start(svr_type)
    return s.SVR_OPEN

def stop_server(**kwargs):
    svr_type = server_type(kwargs["message"])
    if not svr_online()[svr_type]:
        return s.SVR_OFFLINE
    send_command("stop", svr_type)
    return s.SVR_CLOSE

# Normal commands

def ping(**kwargs):
    return "Pong!"

def server_status(**kwargs):
    status = svr_online()[BEDROCK]
    status_string = s.PLAYERS.format(status.players_online, status.players_max) if status else "\u274c"
    return s.STATUS.format(status_string)

def server_bad_command(**kwargs):
    return s.BAD_COMMAND

def help(**kwargs):
    return s.HELP

def bad_syntax(**kwargs):
    return s.NO_COMMAND

# Dicts

normal_c = {
    "help": help,
    "ping": ping,
    "svrstatus": server_status,
    "svrerror": server_bad_command
}

p_user_c = {
    'svrstart': start_server,
    'svrstop': stop_server
}

admin_c = {
    'pucheck' : check_p_user,
    'puadd' : add_p_user,
    'puremove' : remove_p_user
}

#def admin_command(command, config):
#    if command[0] in admin_c.keys():
#        return admin_c[command[0]](message=command[1], config=config)
#    else:
#        return p_user_command(command)
#
#def p_user_command(command):
#    if command[0] in p_user_c.keys():
#        return p_user_c[command[0]](message=command[1])
#    else:
#        return user_command(command)
#
#def user_command(command):
#    if command[0] in normal_c.keys():
#        return normal_c[command[0]](message=command[1])
#    elif command[0][:3] == "svr":
#        return server_bad_command()
#    else:
#        return "El comando {} no existe".format(command[0])


def process_command(command, config, author, admin = False):
    print("-> command: {} by {}".format(command,author))
    # Admin level command requires 'o' flag
    if command[0] in admin_c.keys() and\
        (config.check_p_user(author,'o') or admin):
        return admin_c[command[0]](message=command[1],
                                   config=config,
                                   perms=config.get_p_user(author).replace('o',''),
                                   admin=admin)
    # PU level commands requires the flag for the server
    elif command[0] in p_user_c.keys() and\
        (validate_server_permissions(command[1], config.get_p_user(author)) or admin):
        return p_user_c[command[0]](message=command[1])
    elif command[0] in normal_c.keys():
        return normal_c[command[0]](message=command[1])
    else: return bad_syntax()
