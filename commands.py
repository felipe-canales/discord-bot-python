import asyncio

from mcserver_interface import VANILLA, FORGE, BEDROCK, svr_online, send_command, svr_start

# Aux

def server_type(string):
    if string == "vanilla": return VANILLA
    elif string == "forge": return FORGE
    elif string == "bedrock": return BEDROCK
    return -1

def process_users(users, method):
    processed = []
    for uid in users:
        if method(uid):
            processed.append("<@!{}>".format(uid))
    return processed

# Admin commands

def add_p_user(**kwargs):
    l = len(kwargs['message'])
    if l == 0:
        return "No se mencionan usuarios"

    added = process_users(kwargs['message'],
                          kwargs['config'].add_p_user)

    resp = "Se ha dado privilegios a {} de {} usuarios. {}"\
        .format(len(added), l, ", ".join(added))
    print("Added {}".format(added))
    return resp

def remove_p_user(**kwargs):
    l = len(kwargs['message'])
    if l == 0:
        return "No se mencionan usuarios"

    removed = process_users(kwargs['message'],
                            kwargs['config'].remove_p_user)

    resp = "Se ha quitado privilegios a {} de {} usuarios. {}"\
        .format(len(removed), l, ", ".join(removed))
    print("Removed {}".format(removed))
    return resp

def check_p_user(**kwargs):
    l = len(kwargs['message'])
    if l == 0:
        return "No se mencionan usuarios"

    checked = process_users(kwargs['message'],
                            kwargs['config'].check_p_user)
    
    if len(checked) == 0:
        return "No hay usuarios con privilegios."
    resp = "Los siguientes usuarios tienen privilegios: {}"\
        .format(", ".join(checked))
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
    msg = ["corriendo", "abajo"]
    stt = svr_online()
    return "El servidor vanilla está {}.\nEl servidor forge está {}.\nEl servidor bedrock está {}."\
        .format(*[msg[0] if stt[i] else msg[1] for i in range(3)])

def server_bad_command(**kwargs):
    return "Comando incorrecto o priviliegios insuficientes."

def help(**kwargs):
    return """Maid bot de Doc Scratch

    Bot para administrar los servidores de minecraft. Comandos empiezan con \"trz \".
    
    Comandos disponibles:
    
    - help: Muestra este mensaje.
    - server status: Indica el estado de los servidores de minecraft.
    - server start [tipo]: Abre el servidor \"vanilla\" o \"forge\" de minecraft (Requiere privilegios).
    - server stop [tipo]: Cierra el servidor correspondiente (Requiere privilegios).
    """

def bad_syntax(**kwargs):
    pass

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

def admin_command(command, config):
    if command[0] in admin_c.keys():
        return admin_c[command[0]](message=command[1], config=config)
    else:
        return p_user_command(command)

def p_user_command(command):
    if command[0] in p_user_c.keys():
        return p_user_c[command[0]](message=command[1])
    else:
        return user_command(command)

def user_command(command):
    if command[0] in normal_c.keys():
        return normal_c[command[0]](message=command[1])
    else:
        return "El comando {} no existe".format(command[0])
