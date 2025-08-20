from fastapi import FastAPI, Query
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os, secrets, string

app = FastAPI(title="Fixed+Random 64 API", version="1.1.0")

# ثابت من ENV
CIPHERTEXT = os.getenv(
    "CIPHERTEXT",
    "eeRa0KeingaJo4ohPhe0aek5weixeesh3aeL1ohnee9Lei7kaephiesa5euGh0oy"
)

ALPHABET = string.ascii_letters + string.digits  # A-Z a-z 0-9

def make_random(n: int = 64) -> str:
    return "".join(secrets.choice(ALPHABET) for _ in range(n))

# JSON: يرجّع الاتنين منفصلين + المجمّع
@app.get("/", response_class=JSONResponse)
def root(n: int = Query(64, ge=1, le=512), sep: str = Query(":"), as_text: bool = False):
    rnd = make_random(n)
    combined = f"{CIPHERTEXT}{sep}{rnd}"
    if as_text:
        return PlainTextResponse(combined)
    return {"ok": True, "fixed": CIPHERTEXT, "random": rnd, "combined": combined}

# نص صريح: fixed:random
@app.get("/token", response_class=PlainTextResponse)
def token(n: int = Query(64, ge=1, le=512), sep: str = Query(":")):
    rnd = make_random(n)
    return f"{CIPHERTEXT}{sep}{rnd}"

@app.get("/healthz", response_class=JSONResponse)
def health():
    return {"status": "ok"}
