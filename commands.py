import asyncio

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
        (svr_type == "vanilla" and 'v' in perms) or\
        (svr_type == "bedrock" and 'b' in perms)

def validate_pu_command(auth, perms, admin):
    return admin or ('o' not in perms) or (perms in auth)

# Admin commands

def add_p_user(**kwargs):
    receiver, permissions = kwargs['message']
    if not validate_pu_command(kwargs['perms'], permissions, kwargs['admin']):
        return "Permisos insuficientes."
    if kwargs['config'].add_p_user(receiver,permissions):
        resp = "Se ha dado privilegios a <@!{}>."\
            .format(kwargs['message'][0])
        print("Added {}".format(kwargs['message']))
    else: resp = "PU ya existe."
    return resp

def remove_p_user(**kwargs):
    receiver, _ = kwargs['message']
    permissions = kwargs['config'].get_p_user(receiver)
    if not validate_pu_command(kwargs['perms'], permissions, kwargs['admin']):
        return "Permisos insuficientes."
    if kwargs['config'].remove_p_user(receiver):
        resp = "Se ha quitado privilegios a <@!{}>."\
            .format(kwargs['message'][0])
        print("Removed {}".format(kwargs['message']))
    else: resp = "PU no existe."
    return resp

def check_p_user(**kwargs):
    receiver, _ = kwargs['message']
    p = kwargs['config'].get_p_user(receiver)
    resp = "El usuario {} tiene privilegios: {}"\
        .format(kwargs['message'][0], p)
    return resp

# Power user commands

def start_server(**kwargs):
    svr_type = server_type(kwargs["message"])
    if svr_online()[svr_type]:
        return "El server ya está online."
    svr_start(svr_type)
    return "Se ha iniciado el server."

def stop_server(**kwargs):
    svr_type = server_type(kwargs["message"])
    if not svr_online()[svr_type]:
        return "El server no está online."
    send_command("stop", svr_type)
    return "Cerrando el server."

# Normal commands

def ping(**kwargs):
    return "Pong!"

def server_status(**kwargs):
    stt = ["\u2714" if online else "\u274c" for online in svr_online()]
    return """Estado:
    - {} Minecraft **Vanilla** Survival 1.14 puerto 25565
    - {} Minecraft Vanilla **Creative** 1.14 puerto 25564
    - {} Minecraft **Forge** Survival 1.12 puerto 25566
    - {} Minecraft **Bedrock** Survival puerto 19132""".format(*stt)

def server_bad_command(**kwargs):
    return "El tipo de server no existe o no tiene los provilegios suficientes."

def help(**kwargs):
    return """**Maid bot de Doc Scratch**
    Bot para administrar los servidores de minecraft. Comandos empiezan con \"svr\".
    
Comandos disponibles:```
    help: Muestra este mensaje.
    status: Indica el estado de los servidores de minecraft.
    start [tipo]: Abre el servidor especificado (Requiere privilegios).
    stop [tipo]: Cierra el servidor especificado (Requiere privilegios).```
    """

def bad_syntax(**kwargs):
    return "El comando no existe. Escribe \"svr help\" para ver los comandos disponibles."

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