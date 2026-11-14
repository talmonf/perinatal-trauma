import base64
import json
import subprocess
import time
import urllib.request
from pathlib import Path
from websocket import create_connection

OUT = Path(r"c:\gitreps\perinatal-trauma\.preview")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

proc = subprocess.Popen(
    [
        CHROME,
        "--headless=new",
        "--disable-gpu",
        "--remote-debugging-port=9223",
        "--window-size=1440,900",
        "about:blank",
    ],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)
time.sleep(1.2)

try:
    tabs = json.load(urllib.request.urlopen("http://127.0.0.1:9223/json"))
    ws = create_connection(tabs[0]["webSocketDebuggerUrl"], timeout=20)
    seq = 0

    def call(method, params=None, timeout=20):
        global seq
        seq += 1
        mid = seq
        ws.send(json.dumps({"id": mid, "method": method, "params": params or {}}))
        ws.settimeout(timeout)
        while True:
            raw = json.loads(ws.recv())
            if raw.get("id") == mid:
                return raw

    call("Page.enable")
    call("Page.navigate", {"url": "http://127.0.0.1:8899/"})
    time.sleep(1.0)

    def shoot(name, width, height, mobile, scroll_js):
        call(
            "Emulation.setDeviceMetricsOverride",
            {
                "width": width,
                "height": height,
                "deviceScaleFactor": 1,
                "mobile": mobile,
            },
        )
        call("Runtime.evaluate", {"expression": scroll_js})
        time.sleep(0.4)
        shot = call("Page.captureScreenshot", {"format": "png"})
        data = shot["result"]["data"]
        path = OUT / name
        path.write_bytes(base64.b64decode(data))
        print(name, path.stat().st_size)

    top = "document.documentElement.style.scrollBehavior='auto'; window.scrollTo(0,0)"
    about = "document.documentElement.style.scrollBehavior='auto'; document.querySelector('.about-grid').scrollIntoView({block:'start'})"

    help = "document.documentElement.style.scrollBehavior='auto'; document.querySelector('.band-help').scrollIntoView({block:'start'})"
    shoot("hero-1440.png", 1440, 900, False, top)
    shoot("help-1440.png", 1440, 900, False, help)
    shoot("help-390.png", 390, 900, True, help)
    ws.close()
finally:
    proc.terminate()
