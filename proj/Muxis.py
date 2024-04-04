from flask import Flask, request, jsonify 
import re
from musix_match_api import Musix  # افترضنا أنه تم إنشاء ملف musix_match_api.py للاستيراد
from collections import OrderedDict
app = Flask(__name__)
musix = Musix()

@app.route('/lyrics/GetLyrics', methods=['GET'])
def get_default_lyrics():
    print("http://localhost:5000/lyrics/GetLyrics?q=")

    query = request.args.get('q')
    try:
        dic = OrderedDict({'lyrics':[]})
        dic['info'] = [{'Dev':'~ ZHAN','my_account':'https://OverGroundOfWall.t.me'}]
        track_id = musix.search_track(query)
        response = musix.get_lyrics(track_id)
        for line in response.strip().splitlines():
            match = re.findall(r'\[(.*?)\](.*?)$', line)
            time, content = match[0][0].split('.')[0], match[0][1]
            time = time[-4:] if time[0] == '0' else time
            if content not in ['"""""', '', '♪']:
               print(time)
               dic['lyrics'].append({time:content})
        return jsonify(dic)            
    except Exception as e:
        return jsonify({"error": "Track ID not found.", "isError": True, "SynTex": f"{e}" , 'status_code' : 404})

@app.route('/lyrics/GetLyrPrecisily', methods=['GET'])
def get_alternative_lyrics():
    print("http://localhost:5000/lyrics/GetLyrPrecisily?t=..a=..d=..")
    title = request.args.get('t')
    artist = request.args.get('a')
    duration = request.args.get('d')
    try:
        if duration:
            lyrics = musix.get_lyrics_alternative(title, artist, convert_duration(duration))
        else:
            lyrics = musix.get_lyrics_alternative(title, artist)
        if lyrics:
            return lyrics
    except Exception:
        return jsonify({"error": "Lyrics not found.", "isError": True, "title": title, "artist": artist, "duration": duration}), 404

def convert_duration(time):
    minutes, seconds = map(int, time.split(":"))
    total_seconds = (minutes * 60) + seconds
    return total_seconds

if __name__ == '__main__':
    app.run(debug=True)
