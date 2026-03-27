import logging
import yt_dlp

logger = logging.getLogger(__name__)

class YouTubeAPIHandler:
    def get_latest_videos(self, channel_id, max_results=1):
        """
        YouTube-il ninnu dummy-kku pakaram real latest video fetch cheyyunnu.
        """
        try:
            logger.info(f"Fetching latest videos for channel: {channel_id}")
            ydl_opts = {'quiet': True, 'extract_flat': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Channel videos search cheyyunnu
                info = ydl.extract_info(f"https://www.youtube.com/channel/{channel_id}/videos", download=False)
                if 'entries' in info and len(info['entries']) > 0:
                    video = info['entries'][0]
                    return [{"id": {"videoId": video['id']}}]
            return []
        except Exception as e:
            logger.error(f"Error fetching videos: {e}")
            return []

    def download_video(self, video_url):
        """
        Video download cheythu downloads/ folder-il save cheyyunnu.
        """
        try:
            ydl_opts = {'outtmpl': 'downloads/%(title)s.%(ext)s'}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                return ydl.prepare_filename(info)
        except Exception as e:
            logger.error(f"Error downloading video: {e}")
            return None
