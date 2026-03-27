"""Tests for src/youtube_handler.py"""
import logging
from unittest.mock import MagicMock, patch, call

import pytest

from src.youtube_handler import YouTubeAPIHandler


# ---------------------------------------------------------------------------
# get_latest_videos
# ---------------------------------------------------------------------------

class TestGetLatestVideos:
    def setup_method(self):
        self.handler = YouTubeAPIHandler()

    def test_returns_list(self):
        result = self.handler.get_latest_videos("UCtest", max_results=1)
        assert isinstance(result, list)

    def test_returns_non_empty_list(self):
        result = self.handler.get_latest_videos("UCtest", max_results=1)
        assert len(result) > 0

    def test_each_item_has_video_id_structure(self):
        result = self.handler.get_latest_videos("UCtest", max_results=1)
        for item in result:
            assert "id" in item
            assert "videoId" in item["id"]

    def test_video_id_is_string(self):
        result = self.handler.get_latest_videos("UCtest", max_results=1)
        assert isinstance(result[0]["id"]["videoId"], str)

    def test_stub_returns_known_video_id(self):
        # The current stub always returns the same hard-coded video ID.
        result = self.handler.get_latest_videos("UCtest", max_results=1)
        assert result[0]["id"]["videoId"] == "dQw4w9WgXcQ"

    def test_default_max_results_is_one(self):
        result = self.handler.get_latest_videos("UCtest")
        assert isinstance(result, list)

    def test_accepts_different_channel_ids(self):
        for channel_id in ("UCabc", "UCxyz", "UC123"):
            result = self.handler.get_latest_videos(channel_id, max_results=1)
            assert isinstance(result, list)

    def test_logs_info_message(self, caplog):
        with caplog.at_level(logging.INFO, logger="src.youtube_handler"):
            self.handler.get_latest_videos("UCtest", max_results=3)
        assert any("Fetching latest" in m for m in caplog.messages)

    def test_returns_empty_list_on_exception(self):
        """If the internals raise, the method catches and returns []."""
        handler = YouTubeAPIHandler()
        # Patch logger.info to raise so we can exercise the except branch.
        with patch("src.youtube_handler.logger") as mock_log:
            mock_log.info.side_effect = RuntimeError("boom")
            result = handler.get_latest_videos("UCtest", max_results=1)
        assert result == []

    def test_logs_error_on_exception(self, caplog):
        with patch("src.youtube_handler.logger") as mock_log:
            mock_log.info.side_effect = ValueError("network error")
            handler = YouTubeAPIHandler()
            handler.get_latest_videos("UCtest", max_results=1)
        mock_log.error.assert_called_once()
        error_msg = mock_log.error.call_args[0][0]
        assert "Error fetching videos" in error_msg


# ---------------------------------------------------------------------------
# download_video
# ---------------------------------------------------------------------------

class TestDownloadVideo:
    def setup_method(self):
        self.handler = YouTubeAPIHandler()
        self.sample_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

    def _make_ydl_mock(self, filename="downloads/test_video.mp4"):
        """Helper: returns a configured yt_dlp.YoutubeDL context-manager mock."""
        ydl_instance = MagicMock()
        ydl_instance.extract_info.return_value = {"title": "test_video", "ext": "mp4"}
        ydl_instance.prepare_filename.return_value = filename
        ydl_instance.__enter__ = MagicMock(return_value=ydl_instance)
        ydl_instance.__exit__ = MagicMock(return_value=False)
        return ydl_instance

    def test_returns_filename_on_success(self):
        ydl_mock = self._make_ydl_mock("downloads/test_video.mp4")
        with patch("yt_dlp.YoutubeDL", return_value=ydl_mock):
            result = self.handler.download_video(self.sample_url)
        assert result == "downloads/test_video.mp4"

    def test_calls_extract_info_with_url(self):
        ydl_mock = self._make_ydl_mock()
        with patch("yt_dlp.YoutubeDL", return_value=ydl_mock):
            self.handler.download_video(self.sample_url)
        ydl_mock.extract_info.assert_called_once_with(self.sample_url, download=True)

    def test_calls_prepare_filename_with_info(self):
        info = {"title": "test_video", "ext": "mp4"}
        ydl_mock = self._make_ydl_mock()
        ydl_mock.extract_info.return_value = info
        with patch("yt_dlp.YoutubeDL", return_value=ydl_mock):
            self.handler.download_video(self.sample_url)
        ydl_mock.prepare_filename.assert_called_once_with(info)

    def test_passes_correct_ydl_opts(self):
        ydl_mock = self._make_ydl_mock()
        with patch("yt_dlp.YoutubeDL", return_value=ydl_mock) as ydl_cls:
            self.handler.download_video(self.sample_url)
        ydl_cls.assert_called_once_with({"outtmpl": "downloads/%(title)s.%(ext)s"})

    def test_returns_none_on_exception(self):
        ydl_mock = self._make_ydl_mock()
        ydl_mock.extract_info.side_effect = Exception("network error")
        with patch("yt_dlp.YoutubeDL", return_value=ydl_mock):
            result = self.handler.download_video(self.sample_url)
        assert result is None

    def test_logs_error_on_exception(self):
        ydl_mock = self._make_ydl_mock()
        ydl_mock.extract_info.side_effect = Exception("some error")
        with patch("yt_dlp.YoutubeDL", return_value=ydl_mock), \
             patch("src.youtube_handler.logger") as mock_log:
            self.handler.download_video(self.sample_url)
        mock_log.error.assert_called_once()
        assert "Error downloading video" in mock_log.error.call_args[0][0]

    def test_returns_none_when_ydl_constructor_raises(self):
        with patch("yt_dlp.YoutubeDL", side_effect=RuntimeError("init fail")):
            result = self.handler.download_video(self.sample_url)
        assert result is None

    def test_handles_empty_url(self):
        ydl_mock = self._make_ydl_mock()
        ydl_mock.extract_info.side_effect = Exception("invalid url")
        with patch("yt_dlp.YoutubeDL", return_value=ydl_mock):
            result = self.handler.download_video("")
        assert result is None
