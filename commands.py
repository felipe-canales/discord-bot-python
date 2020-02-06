import asyncio

# Aux

def process_users(users, method):
    processed = []
    for uid in users:
        if method(uid):
            processed.append("<@{}>".format(uid))
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
    return "Aqui es donde iniciaria el server.\nSI PUDIERA HACERLO!!!"

def stop_server(**kwargs):
    return "Aqui es donde pararia el server.\nSI PUDIERA HACERLO!!!"

# Normal commands

def ping(**kwargs):
    return "Pong!"

def server_status(**kwargs):
    return "Aqui es donde verificaria si el server esta corriendo.\nSI PUDIERA HACERLO!!!"

def server_bad_command(**kwargs):
    return "Comando incorrecto para server."

def help(**kwargs):
    pass

def bad_syntax(**kwargs):
    pass

# Dicts

normal_c = {
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