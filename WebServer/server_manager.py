from http.server import BaseHTTPRequestHandler, HTTPServer
from io import BytesIO
import os
import time
from PIL import Image;
import threading
import cv2;

# TODO: FIX THIS UGLY ASS SHIT
hostName = "localhost"
serverPort = 8080

class ServerManager:
    def __init__(self):
        self.updated_image = False;
        self.currImage = [];
    
    def updateImage(self, newImage):
        self.currImage = newImage;
        self.updated_image = True;
       
    def makeStreamServer(self_manager): 
        #TODO: Add comments theirs some ugly ass shit here
        #TODO: Add js support
        class StreamServer(BaseHTTPRequestHandler):
            def do_GET(self):
                extension = self.path.split(".").pop();
                content = "text/html";
                
                if (extension == "css"):
                    content = "text/css";
                elif (extension == "png"):
                    content = "image/png";
                
                if (self.path == "/stream.png"):
                    self.send_response(200)
                    self.send_header("Age", "0")
                    self.send_header("Cache-Control", "no-cache, private")
                    self.send_header("Pragma", "no-cache")
                    self.send_header("Content-Type", "multipart/x-mixed-replace; boundary=FRAME")
                    self.end_headers()
                    while True:
                        if self_manager.updated_image:
                            image = Image.fromarray(self_manager.currImage);
                            stream = BytesIO();
                            image.save(stream, format="PNG");
                            
                            self.wfile.write(b"--FRAME\r\n")
                            self.send_header("Content-Type", "image/jpeg")
                            self.send_header("Content-Length", str(len(stream.getvalue())))
                            self.end_headers()
                            self.wfile.write(stream.getvalue());
                            self.wfile.write(b"\r\n")
                            
                            self_manager.updated_image = False;
                        else:
                            time.sleep(0.1);
                else:
                    self.send_response(200);
                    self.send_header("Content-type", content);
                    self.end_headers(); 
                    self.wfile.write(self._getHtml(self._getPath(self.path)));
                    
            def _getAssetPath(self, originalPath):
                assetPath = originalPath.split("/");
                assetPath.pop();
                assetPath.append("assets");
                return "/".join(assetPath); 

            def _getPath(self, path):
                if (path == "/"):
                    path = "index.html";
                else:
                    path = path[1:len(path)];
                
                for root, dirs, files in os.walk(self._getAssetPath(os.path.realpath(__file__))):
                    if (path in files):
                        return self._getAssetPath(__file__) + "/" + path;
                return self._getAssetPath(__file__) + "/404.html"
                    
            def _getHtml(self, file):
                with open(file, mode='r', encoding='utf-8') as f:
                    content = f.read()
                return bytes(content, 'utf-8') 
        return StreamServer;

    def _run(self):
        self.webServer = HTTPServer((hostName, serverPort), self.makeStreamServer())
        # TODO: replace with sockets so this is not cringe
        self.webServer.serve_forever()
        
    def startServerInNewThread(self):
        self.thread = threading.Thread(target=self._run, daemon=True).start();