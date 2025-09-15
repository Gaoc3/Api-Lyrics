# API-Lyrics 🎵

**A powerful API to fetch song lyrics by name, along with precise timing for each line—perfect for building karaoke apps, lyric viewers, or music analysis tools.**

---

## Features

* **Comprehensive Lyric Retrieval:** Get the full lyrics of any song using its name or specific track details.
* **Precise Line Timestamps (SRT-like):** Receive detailed timing for each lyric line, enabling accurate synchronized display (ideal for karaoke applications).
* **Lightweight & Easy-to-Use:** A straightforward API for quick integration into your projects.
* **Multiple Output Formats:** Supports various output formats (JSON recommended).

---

## API Endpoints

This API provides two main endpoints for fetching lyrics: `GetLyrics` for general search by song name, and `GetLyrPrecisily` for more accurate results using specific track identifiers.

### 1. Get Lyrics by Song Name (`GetLyrics`)

**GET** `http://localhost:8000/lyrics/GetLyrics?q=<song_name>&srt=<true/false>`

#### Parameters

* `q` (required) → The name of the song (e.g., `Shape of You`).
* `srt` (optional) → `true` or `false`
    * `true` → Returns lyrics with timestamps (in an SRT-like format).
    * `false` → Returns plain lyric text.

#### Example Request

```http
GET http://localhost:8000/lyrics/GetLyrics?q=Shape of You&srt=true
```

---

### 2. Get Lyrics Precisely by Track Details (`GetLyrPrecisily`)

**GET** `http://localhost:8000/lyrics/GetLyrPrecisily?t=<track_id>&a=<artist_name>&d=<duration_ms>&srt=<true/false>`

#### Parameters

* `t` (required) → Track ID (a specific identifier for the song).
* `a` (required) → Artist name (e.g., `Ed Sheeran`).
* `d` (optional) → Duration of the song in minutes (e.g., `04:32`).
* `srt` (optional) → `true` or `false`
    * `true` → Returns lyrics with timestamps.
    * `false` → Returns plain lyric text.

#### Example Request

```http
GET http://localhost:8000/lyrics/GetLyrPrecisily?t=5z0tM4Jc9W00DqG7b1S8&a=Ed%20Sheeran&d=237000&srt=true
```

---

### Example Responses (Common for both endpoints)

#### SRT-like Format

```json
[
  {
    "00:02": "The club isn't the best place to find a lover"
  },
  {
    "00:04": "So the bar is where I go"
  },
]
```

#### Plain Text Format

```json
{
  "lyrics": "The club isn't the best place to find a lover\nSo the bar is where I go\nMe and my friends at the table doing shots\nDrinking fast and then we talk slow..."
}
```

-----

## Getting Started

To use this API, send HTTP GET requests to the specified endpoints with the required parameters. The API will respond with JSON data containing the requested lyrics.
