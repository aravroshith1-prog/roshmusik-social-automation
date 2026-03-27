"""Tests for main.py"""
import pytest
from unittest.mock import MagicMock, patch, call


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_yt_handler(video_id="dQw4w9WgXcQ", download_path="downloads/video.mp4"):
    handler = MagicMock()
    handler.get_latest_videos.return_value = [{"id": {"videoId": video_id}}]
    handler.download_video.return_value = download_path
    return handler


def _mock_video_editor(clip_paths=("clip.mp4",)):
    """Returns (extract_clips mock, add_captions mock, add_branding mock)."""
    extract_mock = MagicMock(return_value=list(clip_paths))
    captions_mock = MagicMock(side_effect=lambda path, captions: f"captioned_{path}")
    branding_mock = MagicMock(side_effect=lambda path, branding_image_path: f"branded_{path}")
    return extract_mock, captions_mock, branding_mock


# ---------------------------------------------------------------------------
# main() orchestration tests
# ---------------------------------------------------------------------------

class TestMain:
    """Tests for the main() function in main.py."""

    def _run_main(self, yt_handler, extract_mock, captions_mock, branding_mock, poster_mock):
        """Patch all dependencies and invoke main()."""
        with patch("main.YouTubeAPIHandler", return_value=yt_handler), \
             patch("main.extract_clips", extract_mock), \
             patch("main.add_captions", captions_mock), \
             patch("main.add_branding", branding_mock), \
             patch("main.SocialMediaPoster", return_value=poster_mock):
            import main as main_module
            main_module.main()

    def setup_method(self):
        self.yt_handler = _make_yt_handler()
        self.extract_mock, self.captions_mock, self.branding_mock = _mock_video_editor()
        self.poster_mock = MagicMock()
        self.poster_mock.post_all.return_value = True

    def test_get_latest_videos_called_once(self):
        self._run_main(
            self.yt_handler, self.extract_mock, self.captions_mock,
            self.branding_mock, self.poster_mock,
        )
        self.yt_handler.get_latest_videos.assert_called_once()

    def test_get_latest_videos_called_with_channel_id(self):
        self._run_main(
            self.yt_handler, self.extract_mock, self.captions_mock,
            self.branding_mock, self.poster_mock,
        )
        args, kwargs = self.yt_handler.get_latest_videos.call_args
        # Channel id is the first positional arg.
        assert args[0] == "your_channel_id"

    def test_download_video_called_with_youtube_url(self):
        self._run_main(
            self.yt_handler, self.extract_mock, self.captions_mock,
            self.branding_mock, self.poster_mock,
        )
        self.yt_handler.download_video.assert_called_once()
        url_arg = self.yt_handler.download_video.call_args[0][0]
        assert "dQw4w9WgXcQ" in url_arg
        assert url_arg.startswith("https://www.youtube.com/watch?v=")

    def test_extract_clips_called_with_downloaded_path(self):
        self._run_main(
            self.yt_handler, self.extract_mock, self.captions_mock,
            self.branding_mock, self.poster_mock,
        )
        self.extract_mock.assert_called_once()
        assert self.extract_mock.call_args[0][0] == "downloads/video.mp4"

    def test_add_captions_called_for_each_clip(self):
        extract_mock, captions_mock, branding_mock = _mock_video_editor(
            clip_paths=["clip1.mp4", "clip2.mp4"]
        )
        self._run_main(
            self.yt_handler, extract_mock, captions_mock,
            branding_mock, self.poster_mock,
        )
        assert captions_mock.call_count == 2

    def test_add_branding_called_for_each_clip(self):
        extract_mock, captions_mock, branding_mock = _mock_video_editor(
            clip_paths=["clip1.mp4", "clip2.mp4"]
        )
        self._run_main(
            self.yt_handler, extract_mock, captions_mock,
            branding_mock, self.poster_mock,
        )
        assert branding_mock.call_count == 2

    def test_post_all_called_for_each_clip(self):
        extract_mock, captions_mock, branding_mock = _mock_video_editor(
            clip_paths=["clip1.mp4", "clip2.mp4"]
        )
        self._run_main(
            self.yt_handler, extract_mock, captions_mock,
            branding_mock, self.poster_mock,
        )
        assert self.poster_mock.post_all.call_count == 2

    def test_post_all_receives_branded_path(self):
        self._run_main(
            self.yt_handler, self.extract_mock, self.captions_mock,
            self.branding_mock, self.poster_mock,
        )
        posted_path = self.poster_mock.post_all.call_args[0][0]
        assert "branded_" in posted_path

    def test_post_all_receives_caption_string(self):
        self._run_main(
            self.yt_handler, self.extract_mock, self.captions_mock,
            self.branding_mock, self.poster_mock,
        )
        _, kwargs = self.poster_mock.post_all.call_args
        caption = self.poster_mock.post_all.call_args[1].get("caption") or \
                  self.poster_mock.post_all.call_args[0][1]
        assert isinstance(caption, str)
        assert len(caption) > 0

    def test_prints_automation_complete(self, capsys):
        self._run_main(
            self.yt_handler, self.extract_mock, self.captions_mock,
            self.branding_mock, self.poster_mock,
        )
        captured = capsys.readouterr()
        assert "Automation complete!" in captured.out

    def test_pipeline_ordering(self):
        """extract_clips must run before add_captions, which runs before add_branding."""
        call_order = []
        extract_mock = MagicMock(side_effect=lambda *a, **kw: call_order.append("extract") or ["clip.mp4"])
        captions_mock = MagicMock(side_effect=lambda *a, **kw: call_order.append("captions") or "cap.mp4")
        branding_mock = MagicMock(side_effect=lambda *a, **kw: call_order.append("branding") or "brand.mp4")

        self._run_main(
            self.yt_handler, extract_mock, captions_mock, branding_mock, self.poster_mock
        )
        assert call_order == ["extract", "captions", "branding"]

    def test_no_clips_does_not_call_add_captions(self):
        extract_mock, captions_mock, branding_mock = _mock_video_editor(clip_paths=[])
        self._run_main(
            self.yt_handler, extract_mock, captions_mock,
            branding_mock, self.poster_mock,
        )
        captions_mock.assert_not_called()

    def test_no_clips_does_not_call_add_branding(self):
        extract_mock, captions_mock, branding_mock = _mock_video_editor(clip_paths=[])
        self._run_main(
            self.yt_handler, extract_mock, captions_mock,
            branding_mock, self.poster_mock,
        )
        branding_mock.assert_not_called()

    def test_no_clips_does_not_call_post_all(self):
        extract_mock, captions_mock, branding_mock = _mock_video_editor(clip_paths=[])
        self._run_main(
            self.yt_handler, extract_mock, captions_mock,
            branding_mock, self.poster_mock,
        )
        self.poster_mock.post_all.assert_not_called()
