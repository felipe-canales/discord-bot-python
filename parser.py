def parse_msg(msg):
    print("-> Received {} message as command".format(msg))
    parts = msg.split(' ')
    if len(parts) == 1:
        return "help", ""
    if parts[1] == "server":
        if len(parts) != 3 or parts[2] not in ("status", "start", "stop"):
            return "srverror", ""
        else:
            return "svr" + parts[2], ""
    return parts[1], " ".join(parts[2:])