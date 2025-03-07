from flask import Flask
import flask
import config
import os

app = Flask("alt_download")

@app.route("/<filename>")
def download(filename: str):
    if filename.count('/') or filename.count('\\'):
        return flask.abort(400)
    path = os.path.join(config.AUDIO_PATH, filename)
    if not os.path.exists(path):
        return flask.abort(404)

    return flask.send_file(path, mimetype='audio/m4a')

if __name__ == "__main__":
    app.run(port=5012)