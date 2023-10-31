from flask import Flask, render_template, request
from flask_socketio import SocketIO
import pytube

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_url = request.form['video_url']
        yt = pytube.YouTube(video_url)
        audio = yt.streams.filter(only_audio=True).first()
        audio.download()
        return render_template('play.html', audio_path=audio.default_filename)
    return render_template('index.html')


@socketio.on('play audio')
def play_audio(data):
    audio_path = data['audio_path']
    with open(audio_path, 'rb') as audio_file:
        while True:
            chunk = audio_file.read(4096)
            if not chunk:
                break
            socketio.sleep(0)
            socketio.emit('audio data', {'data': chunk.decode('latin-1')}, namespace='/audio')



if __name__ == '__main__':
    socketio.run(app)
