from http.server import HTTPServer
import threading

from WebServer.server import StreamServer

# TODO: FIX THIS UGLY ASS SHIT
hostName = "localhost"
serverPort = 8080

class ServerManager:
    def _run(self):
        self.webServer = HTTPServer((hostName, serverPort), StreamServer)
        
        # TODO: replace with sockets so this is not cringe
        self.webServer.serve_forever()

    def startServerInNewThread(self):
        self.thread = threading.Thread(target=self._run, daemon=True).start();