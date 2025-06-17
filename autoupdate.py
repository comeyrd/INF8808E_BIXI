import os
import subprocess
import hmac
import hashlib
from flask import Flask, request, abort
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)

GITHUB_SECRET = os.getenv("GITHUB_SECRET", "").encode()
SCRIPT_PATH = "/home/comero/INF8808E_BIXI/update.sh"  

def verify_signature(payload, signature):
    sha_name, signature = signature.split('=')
    if sha_name != 'sha256':
        return False
    mac = hmac.new(GITHUB_SECRET, msg=payload, digestmod=hashlib.sha256)
    return hmac.compare_digest(mac.hexdigest(), signature)

@app.route('/webhook', methods=['POST'])
def webhook():
    signature = request.headers.get('X-Hub-Signature-256')
    if signature is None:
        abort(403)

    payload = request.data
    if not verify_signature(payload, signature):
        abort(403)

    event = request.headers.get('X-GitHub-Event', 'ping')
    if event == "ping":
        return "pong", 200

    data = request.json
    if event == "push" and data.get("ref") == "refs/heads/main":
        try:
            result = subprocess.run(
                ["/bin/bash", SCRIPT_PATH],
                check=True,
                capture_output=True,
                text=True  
            )
            return result.stdout, 200
        except subprocess.CalledProcessError as e:
            return f"Script failed:\n{e.stdout}\n{e.stderr}", 500

    return "Ignored", 200