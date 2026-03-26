# RoshMusik Social Automation

## Overview
Automate downloading YouTube videos, create clips, add captions/branding, and post to TikTok, Instagram, and YouTube Shorts.

## Setup

1. Clone the repo.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Add your API credentials in a `.env` file.

## Usage

```bash
python main.py
```

## Logging & Testing
- All modules now use Python logging for better debugging.
- You can run the basic pipeline tests with:
  ```
  pytest tests/
  ```
- Add or expand test cases in `tests/test_basic_pipeline.py`.

## TODO/NEXT
- Implement YouTube API video listing in `src/youtube_handler.py`
- Implement real video clipping, captioning, and branding in `src/video_editor.py`
- Add platform upload credentials and logic to `src/social_poster.py`
- Integrate a scheduler for daily/weekly automation
- Add better logs/error handling

## Contributing

1. Fork the repo and make your changes.
2. Open a pull request with a clear description.
---