"""Flask application exposing lyrics endpoints."""

from __future__ import annotations

import re
from collections import OrderedDict
from typing import Dict, List

from flask import Flask, jsonify, request

from .musix_match_api import Musix

app = Flask(__name__)
musix = Musix()
AUTHOR_URL = "https://OverGroundOfWall.t.me"

@app.get("/health")
def health():
    return {"status": "ok"}, 200

@app.route('/', methods=['GET'])
def health():
    """Simple endpoint that can be used for health checks."""
    return jsonify({"status": "ok"})


def _base_payload() -> OrderedDict:
    payload = OrderedDict({"lyrics": []})
    payload["info"] = {
        "Dev": "~ ZHAN",
        "my_account": AUTHOR_URL,
    }
    return payload


def _parse_lyrics(raw_lyrics: str, drop_milliseconds: bool) -> List[Dict[str, str]]:
    lyrics: List[Dict[str, str]] = []
    for line in raw_lyrics.strip().splitlines():
        match = re.search(r"\[(.*?)\](.*?)$", line)
        if not match:
            continue
        timestamp, content = match.group(1), match.group(2)
        if drop_milliseconds:
            timestamp = timestamp.split('.')[0]
            if timestamp and timestamp[0] == '0':
                timestamp = timestamp[-4:]
        if content in {'"""""', '', '♪'}:
            continue
        lyrics.append({timestamp: content})
    return lyrics


@app.route('/lyrics/GetLyrics', methods=['GET'])
def get_default_lyrics():
    """Retrieve lyrics using the MusixMatch track search endpoint."""
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({"error": "Missing q parameter.", "isError": True, "status_code": 400}), 400

    srt_param = request.args.get('srt')
    srt = srt_param.strip().lower() if srt_param else 'false'

    try:
        track_id = musix.search_track(query)
        response = musix.get_lyrics(track_id)
    except Exception as exc:  # pragma: no cover - network errors propagated to client
        return jsonify({
            "error": "Track ID not found.",
            "isError": True,
            "SynTex": str(exc),
            "status_code": 404,
        }), 404

    payload = _base_payload()
    drop_milliseconds = srt in {'', 'false'}

    if srt in {'', 'false', 'true'}:
        payload['lyrics'] = _parse_lyrics(response, drop_milliseconds=drop_milliseconds)
        return jsonify(payload)

    return jsonify({
        "error": "Invalid srt value provided.",
        "isError": True,
        "status_code": 400,
    }), 400


@app.route('/lyrics/GetLyrPrecisily', methods=['GET'])
def get_alternative_lyrics():
    """Retrieve lyrics using the MusixMatch alternative endpoint."""
    title = request.args.get('t', '').strip()
    artist = request.args.get('a', '').strip()
    duration = request.args.get('d', '').strip()

    if not title or not artist:
        return jsonify({
            "error": "Missing title or artist parameter.",
            "isError": True,
            "status_code": 400,
        }), 400

    srt_param = request.args.get('srt')
    srt = srt_param.strip().lower() if srt_param else 'false'

    try:
        if duration:
            try:
                parsed_duration = convert_duration(duration)
            except ValueError:
                return jsonify({
                    "status_code": 400,
                    "error": "Invalid duration format. Use mm:ss.",
                    "isError": True,
                    "title": title,
                    "artist": artist,
                    "duration": duration,
                }), 400
            raw_lyrics = musix.get_lyrics_alternative(title, artist, parsed_duration)
        else:
            raw_lyrics = musix.get_lyrics_alternative(title, artist)
    except Exception as exc:  # pragma: no cover - network errors propagated to client
        return jsonify({
            "status_code": 404,
            "error": "Lyrics not found.",
            "isError": True,
            "title": title,
            "artist": artist,
            "duration": duration,
            "SynTex": str(exc),
        }), 404

    payload = _base_payload()
    if srt in {'', 'false', 'true'}:
        drop_milliseconds = srt in {'', 'false'}
        payload['lyrics'] = _parse_lyrics(raw_lyrics, drop_milliseconds=drop_milliseconds)
        return jsonify(payload)

    return jsonify({
        "status_code": 400,
        "error": "Invalid srt value provided.",
        "isError": True,
        "title": title,
        "artist": artist,
        "duration": duration,
    }), 400


def convert_duration(time_value: str) -> int:
    minutes, seconds = map(int, time_value.split(":"))
    total_seconds = (minutes * 60) + seconds
    return total_seconds


if __name__ == '__main__':
    app.run(debug=True)
