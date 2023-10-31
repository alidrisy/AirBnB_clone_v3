from flask import Flask, render_template, request
import pafy
import re

app = Flask(__name__)


def getVideoUrl(content):
    fmtre = re.search('(?<=fmt_url_map=).*', content)
    if fmtre is None:
        return None         # if fmtre is None, it prove there is no match url, and return None to tell the calling function
    grps = fmtre.group(0).split('&amp;')
    vurls = urllib2.unquote(grps[0])
    videoUrl = None
    for vurl in vurls.split('|'):
        if vurl.find('itag=5') > 0:
            return vurl
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/play', methods=['GET', 'POST'])
def play():
    video_url = request.args.get('video_url')
#    video = getVideoUrl(video_url)
    video = pafy.new("https://youtu.be/OmwJcUg5i7w?si=MbJVsJ-RVu69idPF")
    audio = video.getbestaudio()
    return render_template('play.html', audio_url=audio.url)
    return "Error occurred. Please enter a valid YouTube video URL."

if __name__ == '__main__':
    app.run(debug=True)
