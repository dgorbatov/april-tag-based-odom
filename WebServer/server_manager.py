from http.server import BaseHTTPRequestHandler, HTTPServer
from io import BytesIO
import os
import socket
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
        self.stopServer = False;
    
    def updateImage(self, newImage):
        self.currImage = newImage;
        self.updated_image = True;
       
    def manageRequest(self, requestType, path, socket): 
        print("NEW THREAD IN MANAGAE REQUEST" + path);
        extension = path.split(".").pop();
        content = "text/html";
        
        if (extension == "css"):
            content = "text/css";
        elif (extension == "png"):
            content = "image/png";
        
        if (path == "/stream.png"):
            socket.send('HTTP/1.0 200 OK\n'.encode("utf8"));     
            socket.send("Age: 0".encode("utf8"));   
            socket.send("Cache-Control: no-cache, private".encode("utf8"))
            socket.send("Pragma: no-cache".encode("utf8"))
            socket.send("Content-Type: multipart/x-mixed-replace; boundary=FRAME".encode("utf8"))
            socket.send(("\n\n").encode("utf8"))
            while True:
                if self.updated_image:
                    image = Image.fromarray(self.currImage);
                    stream = BytesIO();
                    image.save(stream, format="PNG");
                    
                    socket.send("--FRAME\r\n".encode("utf8"));
                    socket.send("Content-Type: image/jpeg".encode("utf8"))
                    socket.send(("Content-Length: " + str(len(stream.getvalue()))).encode("utf8"))
                    socket.send(("\n\n").encode("utf8"))
                    socket.send(stream.getvalue());
                    socket.send(b"\r\n")
                    
                    self.updated_image = False;
                else:
                    time.sleep(0.1);
        else:
            file = self._getFile(self._getPath(path));
            socket.send('HTTP/1.0 200 OK\n'.encode("utf8"));                    
            socket.send(("Content-Type: " + content).encode("utf8"));
            socket.send(("\n\n").encode("utf8"))
            socket.send((f"""{file}""").encode("utf8"));
                
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
            
    def _getFile(self, file):
        with open(file, mode='r', encoding='utf-8') as f:
            content = f.read()
        return content;
    
    def _run(self):
        TCP_IP = '127.0.0.1'
        TCP_PORT = 8080;
        BUFFER_SIZE = 1028;
        addr = (TCP_IP, TCP_PORT);

        if socket.has_dualstack_ipv6():
            server = socket.create_server(addr, family=socket.AF_INET6, dualstack_ipv6=True)
        else:
            server = socket.create_server(addr, family=socket);

        while not self.stopServer:
            # Accept new connections in an infinite loop.
            client_sock, client_addr = server.accept()
            print('New connection from', client_addr)
            chunks = [];
            notRead = True;
            data = "";
            
            # FUCK PYTHON FOR NOT PUTTING IN DO WHILE LOOPS
            while (len(data) >= BUFFER_SIZE and data != "") or notRead:
                data = client_sock.recv(BUFFER_SIZE);
                chunks.append(data);
                notRead = False;
            clientHttpRequest = b''.join(chunks).decode("utf-8").split("\r\n");
            
            threading.Thread(
                target=self.manageRequest, 
                daemon=False, 
                args=(clientHttpRequest[0].split(" ")[0], clientHttpRequest[0].split(" ")[1], client_sock)
            ).start();
            
            # self.manageRequest(clientHttpRequest[0].split(" ")[0], clientHttpRequest[0].split(" ")[1], client_sock);
            
        server.close();
        
    def endServer(self):
        self.stopServer = True;
        
    def startServerInNewThread(self):
        self.thread = threading.Thread(target=self._run, daemon=True).start();