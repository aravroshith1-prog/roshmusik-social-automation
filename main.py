from src.youtube_handler import YouTubeAPIHandler
from src.video_editor import extract_clips, add_captions, add_branding
from src.social_poster import SocialMediaPoster

# Nammal ippo kandupidicha Channel ID
YOUTUBE_CHANNEL_ID = "UCreRxKEs6gV6WErII4Vt2Eg"

def main():
    yt = YouTubeAPIHandler()
    
    # 1. Latest video fetch cheyyunnu
    print(f"Checking for latest videos in channel: {YOUTUBE_CHANNEL_ID}")
    latest_videos = yt.get_latest_videos(YOUTUBE_CHANNEL_ID, 1)
    
    if not latest_videos:
        print("Video onnum kandilla! Channel ID shariyanonnu check cheyyuka.")
        return

    video_id = latest_videos[0]['id']['videoId']
    youtube_url = f"https://www.youtube.com/watch?v={video_id}"
    
    # 2. Video download cheyyunnu
    print(f"Downloading video: {youtube_url}")
    video_path = yt.download_video(youtube_url)
    
    if video_path:
        # 3. Video cut cheyyunnu (First 60 seconds)
        print("Processing video for Shorts/Reels...")
        clips = extract_clips(video_path, 0, 60)
        
        if clips:
            print(f"Super! Ningalude video ready aayi: {clips[0]}")
            print("Check 'downloads' folder to see the clip.")
    else:
        print("Download failed. Internet connection check cheyyuka.")

if __name__ == "__main__":
    main()
