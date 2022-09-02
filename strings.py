from http.client import UNAUTHORIZED


UNAUTHORIZED = "Permisos insuficientes."
PU_ADD = "Se ha dado privilegios a <@!{}>."
PU_DEL = "Se ha quitado privilegios a <@!{}>."
PU_EXISTS = "PU ya existe."
PU_NOT_FOUND = "PU no existe."
PU_LIST = "El usuario tiene privilegios: {}"
PU_NONE = "El usuario no tiene privilegios"
SVR_ONLINE = "El server ya está online."
SVR_OFFLINE = "El server no está online."
SVR_OPEN = "Se ha iniciado el server."
SVR_CLOSE = "Cerrando el server."

NO_COMMAND = "El comando no existe. Escribe \"svr help\" para ver los comandos disponibles."
BAD_COMMAND = "El tipo de server no existe o no tiene los provilegios suficientes."

HELP = """**Maid bot de Doc Scratch**
    Bot para administrar los servidores de minecraft. Comandos empiezan con \"svr\".
    
Comandos disponibles:```
    help: Muestra este mensaje.
    status: Indica el estado de los servidores de minecraft.
    start [tipo]: Abre el servidor especificado (Requiere privilegios).
    stop [tipo]: Cierra el servidor especificado (Requiere privilegios).```
    """

OLD_STATUS = """    - Minecraft **Vanilla** Survival puerto 25565 {}
    - Minecraft Vanilla **Creative** puerto 25564 {}
    - Minecraft **Forge** Survival puerto 25566 {}
    - Minecraft **Bedrock** Survival {}"""

STATUS = """Minecraft Bedrock Survival {}"""

PLAYERS = "{}/{} jugadores"