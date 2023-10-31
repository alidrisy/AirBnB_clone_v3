from flask import Flask, render_template, request
import pytube

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        video = pytube.YouTube(url)
        stream = video.streams.filter(only_audio=True).first()
        return render_template('play.html', url=stream.url)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
