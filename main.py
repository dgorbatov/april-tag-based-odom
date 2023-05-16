from asyncio import wait
from Detection.apriltagdetector import runVideo
from WebServer.server_manager import ServerManager

def update(frame):
    i=0;

manager = ServerManager();
manager.startServerInNewThread();
runVideo(updateImage=update);