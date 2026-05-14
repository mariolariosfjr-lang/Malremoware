import os
import hashlib
import shutil
from flask import Flask, jsonify

app = Flask(__name__)

MALICIOUS_HASHES = [
    "44d88612fea8a8f36de82e1278abb02f"
]

QUARANTINE = "quarantine"

def md5(file_path):
    hash_md5 = hashlib.md5()

    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)

    return hash_md5.hexdigest()

@app.route("/scan")
def scan():

    infected = []

    for root, dirs, files in os.walk("downloads"):

        for file in files:

            path = os.path.join(root, file)

            try:
                file_hash = md5(path)

                if file_hash in MALICIOUS_HASHES:

                    infected.append(path)

                    shutil.move(
                        path,
                        os.path.join(QUARANTINE, file)
                    )

            except:
                pass

    return jsonify({
        "infected_files": infected,
        "status": "done"
    })

app.run(port=5000)
