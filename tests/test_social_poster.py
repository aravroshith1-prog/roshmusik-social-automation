"""Tests for src/social_poster.py"""
import pytest

from src.social_poster import SocialMediaPoster


class TestSocialMediaPosterPostAll:
    def setup_method(self):
        self.poster = SocialMediaPoster()

    # --- return value ---

    def test_returns_true(self):
        result = self.poster.post_all("clip.mp4", caption="Check this out!")
        assert result is True

    def test_returns_true_with_empty_caption(self):
        result = self.poster.post_all("clip.mp4", caption="")
        assert result is True

    def test_returns_true_with_unicode_caption(self):
        result = self.poster.post_all("clip.mp4", caption="🎵 #music #shorts")
        assert result is True

    def test_returns_true_with_none_video_path(self):
        result = self.poster.post_all(None, caption="test")
        assert result is True

    # --- printed output ---

    def test_prints_video_path(self, capsys):
        self.poster.post_all("my_video.mp4", caption="hello")
        captured = capsys.readouterr()
        assert "my_video.mp4" in captured.out

    def test_prints_caption(self, capsys):
        self.poster.post_all("clip.mp4", caption="Check out the latest music!")
        captured = capsys.readouterr()
        assert "Check out the latest music!" in captured.out

    def test_prints_both_path_and_caption(self, capsys):
        self.poster.post_all("path/to/video.mp4", caption="My caption")
        captured = capsys.readouterr()
        assert "path/to/video.mp4" in captured.out
        assert "My caption" in captured.out

    def test_output_goes_to_stdout_not_stderr(self, capsys):
        self.poster.post_all("clip.mp4", caption="hello")
        captured = capsys.readouterr()
        assert captured.out != ""
        assert captured.err == ""

    # --- multiple calls ---

    def test_can_be_called_multiple_times(self):
        for i in range(5):
            result = self.poster.post_all(f"clip_{i}.mp4", caption=f"caption {i}")
            assert result is True

    def test_multiple_calls_produce_separate_output(self, capsys):
        self.poster.post_all("clip_a.mp4", caption="first")
        self.poster.post_all("clip_b.mp4", caption="second")
        captured = capsys.readouterr()
        assert "clip_a.mp4" in captured.out
        assert "clip_b.mp4" in captured.out

    # --- instantiation ---

    def test_instantiation_creates_object(self):
        poster = SocialMediaPoster()
        assert poster is not None

    def test_post_all_method_exists(self):
        assert hasattr(SocialMediaPoster(), "post_all")
        assert callable(SocialMediaPoster().post_all)
