from asyncio import wait
from Detection.apriltagdetector import runVideo
from WebServer.server_manager import ServerManager

def update(frame):
    print("updated");

manager = ServerManager();
manager.startServerInNewThread();
runVideo(updateImage=update);