import re

def parse_msg(msg, rawtxt):
    print("-> Received #{}# as command".format(rawtxt))
    parts = msg.split(' ')

    # No command
    if len(parts) == 1:
        return "help", ""
    
    # Power User
    if parts[1] == "pu":
        try:
            if len(parts) > 3 and parts[2] in ("check", "add", "remove"):
                return parts[1] + parts[2], parse_mentions(parts[3:])
        except ValueError:
            print("ALERT! Incorrect PU command")
            return "help", ""
    if (len(parts) == 2 and parts[1] == "status"):
        return "svrstatus", ""
    if (len(parts) == 3 and parts[1] in ("start", "stop")):
        try:
            svrtype = get_server_type(parts[2])
            return "svr" + parts[1], svrtype
        except ValueError:
            print("Incorrect start/stop command")
            return "svrerror", ""
    return parts[1], " ".join(parts[2:])


def get_server_type(id):
    if id in ('v', 'vanilla'):
        return 'vanilla'
    if id in ('f', 'forge'):
        return 'forge'
    if id in ('b', 'bedrock'):
        return 'bedrock'
    raise ValueError


pat = r"\<\@\!\d+\>"
def parse_mentions(parts):
    ids = []
    for p in parts:
        if not re.match(pat, p):
            raise ValueError
        ids.append(p[3:-1])
    return ids


if __name__ == "__main__":
    print(parse_msg("svr start b", "svr start b"))