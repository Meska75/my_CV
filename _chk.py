import urllib.request
from pathlib import Path

home = urllib.request.urlopen("http://127.0.0.1:8000/").read().decode("utf-8")
key = 'data-title="سامانه پایش و تحلیل پرواز"'
i = home.find(key)
Path("_chk.txt").write_text(home[i:i + 1600], encoding="utf-8")
