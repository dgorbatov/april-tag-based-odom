from asyncio import wait
from WebServer.server_manager import ServerManager


ServerManager().startServerInNewThread();

i =0
while True:
    i = 1