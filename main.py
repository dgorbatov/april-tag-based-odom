from asyncio import wait
from Detection.apriltagdetector import runVideo
from WebServer.server_manager import ServerManager

manager = ServerManager();
manager.startServerInNewThread();
runVideo(updateImage=manager.updateImage);