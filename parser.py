import re

def parse_msg(msg, rawtxt):
    print("-> Received #{}# as command".format(rawtxt))
    parts = [x for x in msg.split(' ') if x != '']

    # No command
    if len(parts) == 1:
        return "help", ""
    
    # Power User
    if parts[1] == "pu":
        try:
            if len(parts) > 4 and parts[2] == "add":
                return parts[1] + parts[2],\
                       (parse_mention(parts[3]), parse_permissions(parts[4:]))
            elif len(parts) == 4 and parts[2] in ("check", "remove"):
                return parts[1] + parts[2], (parse_mention(parts[3]), "")
        except ValueError:
            print("ALERT! Incorrect PU command")
            return "help", ""
    # Server Status
    if (len(parts) == 2 and parts[1] in ["status", "stt"]):
        return "svrstatus", ""
    # Server Operations
    if (len(parts) == 2 and parts[1] in ("start", "stop")):
        return "svr" + parts[1], 'bedrock'
    if (len(parts) == 3 and parts[1] in ("start", "stop")):
        try:
            svrtype = get_server_type(parts[2])
            return "svr" + parts[1], svrtype
        except ValueError:
            print("Incorrect start/stop command")
            return "svrerror", ""
    return parts[1], " ".join(parts[2:])


def get_server_type(id):
    if id in ('s', 'v', 'vanilla'):
        return 'vanilla'
    if id in ('f', 'forge'):
        return 'forge'
    if id in ('b', 'bedrock'):
        return 'bedrock'
    if id in ('c', 'creative'):
        return 'creative'
    raise ValueError

def parse_permissions(plist):
    perms = ""
    if "survival" in plist:
        perms += "s"
    if "all" in plist:
        perms += "a"
    if "bedrock" in plist:
        perms += "b"
    if "moderator" in plist:
        perms += "o"
    if len(perms) == 0:
        raise ValueError
    return perms

pat = r"\<\@\!\d+\>"
pat2= r"\<\@\d+\>"
#def parse_mentions(parts):
#    ids = []
#    for p in parts:
#        if not re.match(pat, p):
#            raise ValueError
#        ids.append(p[3:-1])
#    return ids

def parse_mention(id):
    if re.match(pat, id):
        return id[3:-1]
    if re.match(pat2, id):
        return id[2:-1]
    raise ValueError


if __name__ == "__main__":
    print(parse_msg("svr start b", "svr start b"))
