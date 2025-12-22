import os
from uuid import uuid4
from beet import ResourcePack
from configparser import ConfigParser
from hashlib import sha1
from http.server import HTTPServer, SimpleHTTPRequestHandler
from io import BytesIO
from threading import Thread
from zipfile import ZipFile, ZIP_DEFLATED

TCP_PORT = 8080 # Change this to an open TCP port for the pack manager server
DEBUG = False # Set to True to enable debug mode (dumping pack to disk instead of running server)

# Gather packs
packs = []
for pack in os.listdir("resourcepacks"):
    if pack.endswith(".zip") or os.path.isdir(os.path.join("resourcepacks", pack)):
        packs.append(ResourcePack(path=os.path.join("resourcepacks", pack)))

# Merge packs
merged_pack = ResourcePack()
for pack in packs:
    merged_pack.merge(pack)
merged_pack.description = "Server Resource Pack"

# Save merged pack to an in-memory zip file
in_mem_pack = BytesIO()
merged_pack.dump(ZipFile(in_mem_pack, 'w', ZIP_DEFLATED))
if DEBUG:
    with open("debug_server_resources.zip", "wb") as f:
        f.write(in_mem_pack.getvalue())
        exit(0)

# Modify server.properties to use the current sha1 of the pack and a random UUID
config = ConfigParser()
with open("server.properties", "r") as f:
    config.read_string("[server]\n" + f.read())

config.set("server", "resource-pack-id", str(uuid4()))

pack_sha1 = sha1(in_mem_pack.getvalue()).hexdigest().lower()
config.set("server", "resource-pack-sha1", pack_sha1)

with open("server.properties", "w") as f:
    for key, value in config['server'].items():
        f.write(f"{key}={value}\n")

# Start pack manager server
class PackManagerHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/pack.zip":
            self.send_response(200)
            self.send_header("Content-Type", "application/zip")
            self.send_header("Content-Disposition", 'attachment; filename="server_resources.zip"')
            self.end_headers()
            self.wfile.write(in_mem_pack.getvalue())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")
    def log_message(self, format, *args):
        pass

httpd = HTTPServer(("", TCP_PORT), PackManagerHandler)
print(f"Serving resource pack at http://0.0.0.0:{TCP_PORT}...")
Thread(target=httpd.serve_forever, daemon=True).start()
os.system("./run.sh")
