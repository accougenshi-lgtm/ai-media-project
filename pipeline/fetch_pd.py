"""Download PUBLIC-DOMAIN-only images from Wikimedia Commons; logs source+license to credits.json."""
import json, sys, time, urllib.request, urllib.parse, pathlib
UA = {"User-Agent": "AIMediaResearch/0.1 (research script)"}
OUT = pathlib.Path("assets/pd"); CRED = OUT / "credits.json"
def get(url):
    import subprocess
    for attempt in range(4):
        r = subprocess.run(["curl", "-sf", "-m", "60", "-A", UA["User-Agent"], url], capture_output=True)
        if r.returncode == 0: return r.stdout
        time.sleep(10 * (attempt + 1))
    raise RuntimeError("fetch failed: " + url)
def fetch(term, name, min_w=1500):
    p = {"action":"query","format":"json","generator":"search","gsrsearch":f"{term} filetype:bitmap","gsrnamespace":6,"gsrlimit":10,"prop":"imageinfo","iiprop":"url|extmetadata|size"}
    d = json.loads(get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(p)))
    for pg in d.get("query", {}).get("pages", {}).values():
        ii = pg["imageinfo"][0]; md = ii["extmetadata"]
        lic = md.get("LicenseShortName", {}).get("value", "")
        if "public domain" in lic.lower() and min_w <= ii["width"] <= 5000:
            import subprocess; time.sleep(4); r = subprocess.run(["curl","-sf","-m","120","-A",UA["User-Agent"],"-o",str(OUT/f"{name}.jpg"),ii["url"].split("?")[0]])
            if r.returncode: print("  skip (download failed)", pg["title"]); continue
            cred = json.loads(CRED.read_text()) if CRED.exists() else {}
            cred[name] = {"file": pg["title"], "page": ii["descriptionurl"], "license": lic,
                          "credit": md.get("Artist", {}).get("value", "")[:200]}
            CRED.write_text(json.dumps(cred, indent=2)); print("ok", name, pg["title"], lic); return True
    print("none", term); return False
if __name__ == "__main__":
    for spec in sys.argv[1:]:
        name, term = spec.split("=", 1); fetch(term, name); time.sleep(3)
