"""Tests for src/video_editor.py"""
import pytest

from src.video_editor import extract_clips, add_captions, add_branding


# ---------------------------------------------------------------------------
# extract_clips
# ---------------------------------------------------------------------------

class TestExtractClips:
    def test_callable(self):
        assert callable(extract_clips)

    def test_returns_none_stub(self):
        # Current implementation is a stub (pass); confirm it returns None.
        result = extract_clips("video.mp4", start_time=0, end_time=60)
        assert result is None

    def test_accepts_zero_start_time(self):
        result = extract_clips("video.mp4", start_time=0, end_time=30)
        assert result is None

    def test_accepts_large_end_time(self):
        result = extract_clips("video.mp4", start_time=0, end_time=3600)
        assert result is None

    def test_accepts_non_zero_start_time(self):
        result = extract_clips("video.mp4", start_time=30, end_time=90)
        assert result is None

    def test_accepts_float_times(self):
        result = extract_clips("video.mp4", start_time=1.5, end_time=61.5)
        assert result is None

    def test_does_not_raise_on_nonexistent_path(self):
        # Stub must not perform I/O; it should not raise for missing files.
        try:
            extract_clips("/nonexistent/path.mp4", start_time=0, end_time=10)
        except Exception as exc:
            pytest.fail(f"extract_clips raised unexpectedly: {exc}")

    def test_accepts_keyword_arguments(self):
        result = extract_clips(video_path="clip.mp4", start_time=5, end_time=15)
        assert result is None


# ---------------------------------------------------------------------------
# add_captions
# ---------------------------------------------------------------------------

class TestAddCaptions:
    def test_callable(self):
        assert callable(add_captions)

    def test_returns_none_stub(self):
        result = add_captions("video.mp4", captions="Follow @roshmusik 🎵")
        assert result is None

    def test_accepts_empty_caption_string(self):
        result = add_captions("video.mp4", captions="")
        assert result is None

    def test_accepts_unicode_captions(self):
        result = add_captions("video.mp4", captions="🎵🎶🎸")
        assert result is None

    def test_accepts_long_caption_string(self):
        long_caption = "A" * 500
        result = add_captions("video.mp4", captions=long_caption)
        assert result is None

    def test_does_not_raise_on_nonexistent_path(self):
        try:
            add_captions("/nonexistent/path.mp4", captions="test")
        except Exception as exc:
            pytest.fail(f"add_captions raised unexpectedly: {exc}")

    def test_accepts_keyword_arguments(self):
        result = add_captions(video_path="clip.mp4", captions="hello")
        assert result is None

    def test_accepts_multiline_captions(self):
        result = add_captions("video.mp4", captions="Line 1\nLine 2\nLine 3")
        assert result is None


# ---------------------------------------------------------------------------
# add_branding
# ---------------------------------------------------------------------------

class TestAddBranding:
    def test_callable(self):
        assert callable(add_branding)

    def test_returns_none_stub(self):
        result = add_branding("video.mp4", branding_image_path=None)
        assert result is None

    def test_accepts_none_branding_image(self):
        result = add_branding("video.mp4", branding_image_path=None)
        assert result is None

    def test_accepts_string_branding_image_path(self):
        result = add_branding("video.mp4", branding_image_path="logo.png")
        assert result is None

    def test_accepts_absolute_branding_image_path(self):
        result = add_branding("video.mp4", branding_image_path="/assets/watermark.png")
        assert result is None

    def test_does_not_raise_on_nonexistent_paths(self):
        try:
            add_branding("/no/video.mp4", branding_image_path="/no/brand.png")
        except Exception as exc:
            pytest.fail(f"add_branding raised unexpectedly: {exc}")

    def test_accepts_keyword_arguments(self):
        result = add_branding(video_path="clip.mp4", branding_image_path=None)
        assert result is None
