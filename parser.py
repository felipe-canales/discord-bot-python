import re

def parse_msg(msg, rawtxt):
    print("-> Received #{}# as command".format(rawtxt))
    parts = msg.split(' ')
    #text = rawtxt.split(' ')
    if len(parts) == 1:
        return "help", ""
    if parts[1] == "pu":
        try:
            if len(parts) > 3 and parts[2] in ("check", "add", "remove"):
                return parts[1] + parts[2], parse_mentions(parts[3:])
        except ValueError:
            return "help", ""
    if parts[1] == "server":
        if (len(parts) == 3 and parts[2] == "status"):
            return "svrstatus", ""
        elif (len(parts) == 4 and parts[2] in ("start", "stop")\
             and parts[3] in ("vanilla", "forge", "bedrock")):
            return "svr" + parts[2], parts[3]
        return "svrerror", ""
    return parts[1], " ".join(parts[2:])

pat = r"\<\@\!\d+\>"
def parse_mentions(parts):
    ids = []
    for p in parts:
        if not re.match(pat, p):
            raise ValueError
        ids.append(p[3:-1])
    return ids
