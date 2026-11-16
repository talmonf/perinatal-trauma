import base64
import json
import subprocess
import time
import urllib.request
from pathlib import Path
from websocket import create_connection

chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
out = Path(r"c:\gitreps\perinatal-trauma\.preview")
proc = subprocess.Popen(
    [chrome, "--headless=new", "--disable-gpu", "--remote-debugging-port=9331", "--window-size=1280,800", "about:blank"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)
time.sleep(2)
try:
    tabs = json.load(urllib.request.urlopen("http://127.0.0.1:9331/json"))
    ws = create_connection(tabs[0]["webSocketDebuggerUrl"], timeout=20)
    n = 0

    def call(method, params=None):
        global n
        n += 1
        ws.send(json.dumps({"id": n, "method": method, "params": params or {}}))
        while True:
            raw = json.loads(ws.recv())
            if raw.get("id") == n:
                return raw

    call("Page.enable")
    call("Page.navigate", {"url": "http://127.0.0.1:8899/"})
    time.sleep(0.8)

    def shoot(name, js):
        call("Runtime.evaluate", {"expression": js})
        time.sleep(0.3)
        shot = call("Page.captureScreenshot", {"format": "jpeg", "quality": 70})
        (out / name).write_bytes(base64.b64decode(shot["result"]["data"]))
        print(name)

    shoot("wa-close.jpg", "document.querySelector('.band-close').scrollIntoView()")
    shoot("wa-footer.jpg", "document.querySelector('.site-footer').scrollIntoView()")
    label = call("Runtime.evaluate", {"expression": "document.querySelectorAll('[data-whatsapp]').length + ' | ' + document.querySelector('.footer-name').textContent + ' | ' + document.querySelector('.footer-contact').innerText", "returnByValue": True})
    print(label["result"]["result"]["value"])
    ws.close()
finally:
    proc.terminate()
