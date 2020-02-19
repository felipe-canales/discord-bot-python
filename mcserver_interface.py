import os

from subprocess import Popen, PIPE
from dotenv import load_dotenv

load_dotenv()

FORGE = 1
VANILLA = 0

def svr_online():
    comv = Popen(["pgrep", "-f", "runserver_minecraft_vanilla"],
                stdout=PIPE)
    comf = Popen(["pgrep", "-f", "runserver_minecraft_forge"],
                stdout=PIPE)
    return (len(comv.stdout.read()) > 0,
            len(comf.stdout.read()) > 0)

def send_command(command, svr_type):
    if svr_type == VANILLA:
        with open("{}/pipe.str".format(os.getenv("MC_SERVER_VANILLA_DIR")), "w") as pipe:
            pipe.write(command)
    elif svr_type == FORGE:
        with open("{}/pipe.str".format(os.getenv("MC_SERVER_FORGE_DIR")), "w") as pipe:
            pipe.write(command)
    else:
        raise ValueError

if __name__ == "__main__":
    print(svr_online())