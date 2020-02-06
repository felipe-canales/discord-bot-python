import asyncio

# Aux

def process_users(user_list, method):
    processed = []
    for user in user_list:
        if method(user.id):
            processed.append(user.name)
    return processed

# Admin commands

def shutdown(**kwargs):
    kwargs['config'].save_p_users()
    kwargs['message'].channel.send("Shutting down :(")
    kwargs['config'].close()

def add_p_user(**kwargs):
    l = len(kwargs['message'].mentions)
    if l == 0:
        return "No se mencionan usuarios"

    added = process_users(kwargs['message'].mentions,
                          kwargs['config'].add_p_user)

    resp = "Se ha dado privilegios a {} de {} usuarios. {}"\
        .format(len(added), l, ", ".join(added))
    print("Added {}".format(added))
    return resp

def remove_p_user(**kwargs):
    l = len(kwargs['message'].mentions)
    if l == 0:
        return "No se mencionan usuarios"

    removed = process_users(kwargs['message'].mentions,
                            kwargs['config'].remove_p_user)

    resp = "Se ha quitado privilegios a {} de {} usuarios. {}"\
        .format(len(removed), l, ", ".join(removed))
    print("Removed {}".format(removed))
    return resp

def check_p_user(**kwargs):
    l = len(kwargs['message'].mentions)
    if l == 0:
        return "No se mencionan usuarios"

    checked = process_users(kwargs['message'].mentions,
                            kwargs['config'].check_p_user)
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

# Dicts

normal_c = {
    "ping": ping,
}

p_user_c = dict(normal_c)
p_user_c['start'] = start_server
p_user_c['stop'] = stop_server

admin_c = dict(p_user_c)
admin_c['checkpu'] = check_p_user
admin_c['addpu'] = add_p_user
admin_c['removepu'] = remove_p_user
admin_c['shutdown'] = shutdown


def admin_command(message, command, config):
    if command[1] in admin_c.keys():
        return admin_c[command[1]](message=message, config=config)
    else:
        return "El comando no existe"

def p_user_command(message, command):
    if command[1] in p_user_c.keys():
        return p_user_c[command[1]](message=message)
    else:
        return "El comando no existe"

def user_command(message, command):
    if command[1] in normal_c.keys():
        return normal_c[command[1]](message=message)
    else:
        return "El comando no existe"