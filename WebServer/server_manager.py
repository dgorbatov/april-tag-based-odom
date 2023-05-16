from http.server import HTTPServer
import threading

from WebServer.server import StreamServer

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
                
                self.send_response(200);
                self.send_header("Content-type", content);
                self.end_headers(); 
                
                if (self.path == "/stream.png"):
                            # print("IN");
                            # image = Image.fromarray(cv2.imread('image.png'));
                            image = Image.fromarray(self_manager.currImage);
                            stream = BytesIO();
                            image.save(stream, format="PNG");
                            self.wfile.write(stream.getvalue());
                            self.got_new_val = False;
                else:
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

    def _run(self):
        self.webServer = HTTPServer((hostName, serverPort), self.makeStreamServer())
        # TODO: replace with sockets so this is not cringe
        self.webServer.serve_forever()
        
    def startServerInNewThread(self):
        self.thread = threading.Thread(target=self._run, daemon=True).start();