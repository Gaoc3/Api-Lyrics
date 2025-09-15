# API-Lyrics 🎵

A powerful API that allows you to fetch song lyrics by song name, along with precise timing for each line—perfect for building karaoke apps, lyric viewers, or music analysis tools.

---

## Features

- Retrieve full lyrics of any song using its name.
- Get timestamps for each line of lyrics for synchronized display.
- Lightweight and easy-to-use API.
- Supports multiple formats for output (JSON recommended).


## API Endpoint

**GET** `http://localhost:8000/lyrics/GetLyrics?q=<song_name>&srt=<true/false>`

### Parameters

- `q` (required) → Song name (e.g., `Shape of You`)
- `srt` (optional) → `true` or `false`  
  - `true` → returns lyrics with timestamps (SRT format)  
  - `false` → returns plain lyrics text

---

### Example Request

```http
GET http://localhost:8000/lyrics/GetLyrics?q=Shape of You&srt=true
