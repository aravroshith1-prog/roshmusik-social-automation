from src.youtube_handler import YouTubeAPIHandler
from src.video_editor import extract_clips, add_captions, add_branding
from src.social_poster import SocialMediaPoster

YOUTUBE_CHANNEL_ID = "your_channel_id"

def main():
    yt = YouTubeAPIHandler()
    # 1. Get latest video
    latest_vid = yt.get_latest_videos(YOUTUBE_CHANNEL_ID, 1)[0]
    youtube_url = f"https://www.youtube.com/watch?v={latest_vid['id']['videoId']}"

    # 2. Download video (replace output_dir with actual path)
    video_path = yt.download_video(youtube_url)
    
    # 3. Extract clips (implement logic in video_editor module)
    clip_paths = extract_clips(video_path, start_time=0, end_time=60)  # 1-minute clip as example

    for clip in clip_paths:
        # 4. Add captions
        captioned_path = add_captions(clip, captions="Follow @roshmusik 🎵")
        # 5. Add branding
        branded_path = add_branding(captioned_path, branding_image_path=None)  # Add a watermark if available

        # 6. Post to socials
        poster = SocialMediaPoster()
        poster.post_all(branded_path, caption="Check out the latest music! #shorts #music")
    
    print("Automation complete!")

if __name__ == "__main__":
    main()