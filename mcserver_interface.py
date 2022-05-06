import os

from subprocess import Popen, PIPE
from dotenv import load_dotenv

load_dotenv()

VANILLA = 0
CREATIVE = 1
FORGE = 2
BEDROCK = 3

def svr_online():
    comv = Popen(["pgrep", "-f", "runserver_minecraft_vanilla"],
                stdout=PIPE)
    comf = Popen(["pgrep", "-f", "runserver_ftb"],
                stdout=PIPE)
    comb = Popen(["pgrep", "-f", "runserver_minecraft_bedrock"],
                stdout=PIPE)
    comc = Popen(["pgrep", "-f", "runserver_minecraft_creative"],
                stdout=PIPE)
    return (len(comv.stdout.read()) > 0,
            len(comc.stdout.read()) > 0,
            len(comf.stdout.read()) > 0,
            len(comb.stdout.read()) > 0)

def send_command(command, svr_type):
    if svr_type == VANILLA:
        with open("{}/pipe.str".format(os.getenv("MC_SERVER_VANILLA_DIR")), "w") as pipe:
            pipe.write(command + "\n")
    elif svr_type == FORGE:
        with open("{}/pipe.str".format(os.getenv("MC_SERVER_FORGE_DIR")), "w") as pipe:
            pipe.write(command + "\n")
    elif svr_type == BEDROCK:
        with open("{}/pipe.str".format(os.getenv("MC_SERVER_BEDROCK_DIR")), "w") as pipe:
            pipe.write(command + "\n")
    elif svr_type == CREATIVE:
        with open("{}/pipe.str".format(os.getenv("MC_SERVER_CREATIVE_DIR")), "w") as pipe:
            pipe.write(command + "\n")
    else:
        raise ValueError

def svr_start(svr_type):
    wd = os.getcwd()
    com = "./{} | java -Xmx2G -Xms2G -XX:+UseConcMarkSweepGC -XX:+UseParNewGC -jar server.jar nogui > /dev/null &"
    if svr_type == VANILLA:
        os.chdir(os.getenv("MC_SERVER_VANILLA_DIR"))
        Popen("./runserver.sh", shell=True)
    elif svr_type == FORGE:
        os.chdir(os.getenv("MC_SERVER_FORGE_DIR"))
        Popen("./start.sh", shell=True)
    elif svr_type == BEDROCK:
        os.chdir(os.getenv("MC_SERVER_BEDROCK_DIR"))
        Popen("./runserver_minecraft_bedrock | LD_LIBRARY_PATH=. ./bedrock_server > /dev/null &", shell=True)
    elif svr_type == CREATIVE:
        os.chdir(os.getenv("MC_SERVER_CREATIVE_DIR"))
        Popen(com.format("runserver_minecraft_creative"), shell=True)
    else:
        os.chdir(wd)
        raise ValueError
    os.chdir(wd)

if __name__ == "__main__":
    print(svr_online())
