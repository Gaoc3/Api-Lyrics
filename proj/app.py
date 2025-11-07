from flask import Flask, request, jsonify 
import re
from werkzeug.wrappers import Request, Response
from musix_match_api import Musix 
from collections import OrderedDict
app = Flask(__name__)
musix = Musix()
author = 'https://OverGroundOfWall.t.me'
@app.route('/lyrics/GetLyrics', methods=['GET'])
def get_default_lyrics():
    # http://localhost:8000/lyrics/GetLyrics?q=&srt=.."
    resp = Request.content_type = 'application/health'
    srt = request.args.get('srt')
    query = request.args.get('q')
    if srt == 'false' or srt == None or srt == '' or srt == ' ':
        try: 
            dic = OrderedDict({'lyrics':[]})
            dic['info'] = {
                    'Dev':'~ ZHAN',
                    'my_account':f'{author}'  
                    }
            track_id = musix.search_track(query)
            response = musix.get_lyrics(track_id)
            for line in response.strip().splitlines():
                match = re.findall(r'\[(.*?)\](.*?)$', line)
                time, content = match[0][0].split('.')[0], match[0][1]
                time = time[-4:] if time[0] == '0' else time
                if content not in ['"""""', '', '♪']:
                    dic['lyrics'].append({time:content})
            return jsonify(dic) 
        except Exception as e:
            return jsonify({"error": "Track ID not found.", "isError": True, "SynTex": f"{e}" , 'status_code' : 404})
    elif srt == 'true':
        # try: 
            dic = OrderedDict({'lyrics':[]})
            dic['info'] = {
                    'Dev':'~ ZHAN',
                    'my_account':f'{author}'  
                    }
            track_id = musix.search_track(query)
            response = musix.get_lyrics(track_id)
            for line in response.strip().splitlines():
                match = re.findall(r'\[(.*?)\](.*?)$', line)
                time, content = match[0][0], match[0][1]
                if content not in ['"""""', '', '♪']:
                    dic['lyrics'].append({time:content})
            return jsonify(dic)     
        # except Exception as e:
        #     return jsonify({"error": "Track ID not found.", "isError": True, "SynTex": f"{e}" , 'status_code' : 404})
    else:
        return jsonify({"error": "Track ID not found.", "isError": True, "SynTex": f"{e}" , 'status_code' : 404})
@app.route('/lyrics/GetLyrPrecisily', methods=['GET'])
def get_alternative_lyrics():
    # http://localhost:8000/lyrics/GetLyrPrecisily?t=..&a=..&d=..&srt=..
    title = request.args.get('t')
    artist = request.args.get('a')
    duration = request.args.get('d')
    srt = request.args.get('srt')
    print(srt)
    if srt == 'false' or srt == None or srt == '' or srt == ' ':
        try:
            if duration or ':' in [duration]:
                dic = OrderedDict({'lyrics':[]})
                dic['info'] = {
                    'Dev':'~ ZHAN',
                    'my_account':f'{author}'  
                    }
                lyrics = musix.get_lyrics_alternative(title, artist, convert_duration(duration))
                for lyr in lyrics.strip().splitlines():
                    match = re.findall(r'\[(.*?)\](.*?)$', lyr)
                    time, content = match[0][0].split('.')[0], match[0][1]
                    time = time[-4:] if time[0] == '0' else time
                    if content not in ['"""""', '', '♪']:
                        dic['lyrics'].append({time:content})
                return jsonify(dic)
            else:
                dic = OrderedDict({'lyrics':[]})
                dic['info'] = {
                    'Dev':'~ ZHAN',
                    'my_account':f'{author}'  
                    }
                lyrics = musix.get_lyrics_alternative(title,artist)
                for lyr in lyrics.strip().splitlines():
                    match = re.findall(r'\[(.*?)\](.*?)$', lyr)
                    time, content = match[0][0].split('.')[0], match[0][1]
                    time = time[-4:] if time[0] == '0' else time
                    if content not in ['"""""', '', '♪']:
                        dic['lyrics'].append({time:content})
                return jsonify(dic)
        except Exception:
            return jsonify({'status_code': 404,"error": "Lyrics not found.", "isError": True, "title": title, "artist": artist, "duration": duration})
    elif srt == 'true':
        try:
            print(duration)
            if duration or ':' in [duration]:
                dic = OrderedDict({'lyrics':[]})
                dic['info'] = {
                    'Dev':'~ ZHAN',
                    'my_account':f'{author}'  
                    }
                lyrics = musix.get_lyrics_alternative(title, artist, convert_duration(duration))
                for lyr in lyrics.strip().splitlines():
                    match = re.findall(r'\[(.*?)\](.*?)$', lyr)
                    time, content = match[0][0], match[0][1]
                    if content not in ['"""""', '', '♪']:
                        dic['lyrics'].append({time:content})
                return jsonify(dic)
            else:
                dic = OrderedDict({'lyrics':[]})
                dic['info'] = {
                    'Dev':'~ ZHAN',
                    'my_account':f'{author}'  
                    }
                lyrics = musix.get_lyrics_alternative(title,artist)
                for lyr in lyrics.strip().splitlines():
                    match = re.findall(r'\[(.*?)\](.*?)$', lyr)
                    time, content = match[0][0] , match[0][1]
                    if content not in ['"""""', '', '♪']:
                        dic['lyrics'].append({time:content})
                return jsonify(dic)
        except Exception:
            return jsonify({'status_code': 404,"error": "Lyrics not found.", "isError": True, "title": title, "artist": artist, "duration": duration})
    else:
        return jsonify({'status_code': 404,"error": "Lyrics not found.", "isError": True, "title": title, "artist": artist, "duration": duration})
def convert_duration(time):
    minutes, seconds = map(int, time.split(":"))
    total_seconds = (minutes * 60) + seconds
    return total_seconds

if __name__ == '__main__':
    app.run(debug=True)

