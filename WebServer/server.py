from http.server import BaseHTTPRequestHandler, HTTPServer
import os;
import time

#TODO: Add comments theirs some ugly ass shit here
#TODO: Add js support
class StreamServer(BaseHTTPRequestHandler):
    def do_GET(self):
        extension = self.path.split(".").pop();
        content = "text/html";
        
        if (extension == "css"):
            content = "text/css";
        
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
