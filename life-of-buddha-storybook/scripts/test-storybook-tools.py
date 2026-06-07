#!/usr/bin/env python3
"""Smoke tests for storybook generation helpers."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile


PROJECT = Path(__file__).resolve().parents[1]
TOOLS_PATH = PROJECT / "scripts/storybook_tools.py"


def load_tools():
    spec = importlib.util.spec_from_file_location("storybook_tools", TOOLS_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_parse_english_and_chinese_scenes():
    tools = load_tools()
    english = tools.parse_scenes(
        PROJECT / "content/the-life-of-the-buddha-picture-storybook.en.md",
        "en",
    )
    chinese = tools.parse_scenes(
        PROJECT / "content/the-life-of-the-buddha-picture-storybook.zh.md",
        "zh",
    )

    assert len(english) == 42
    assert len(chinese) == 42
    assert english[0]["number"] == "01"
    assert chinese[0]["number"] == "01"
    assert chinese[0]["title"] == "燃灯佛前生起大愿"


def test_build_chinese_html_uses_local_audio_and_page_copy():
    tools = load_tools()
    scenes = tools.parse_scenes(
        PROJECT / "content/the-life-of-the-buddha-picture-storybook.zh.md",
        "zh",
    )

    html = tools.render_html(
        scenes=scenes,
        language="zh-Hans",
        book_title="佛陀的一生",
        page_title="佛陀的一生 - 图像故事书",
        scene_label="第",
        scene_suffix="幕",
        scene_select_label="场景",
        previous_label="← 上一幕",
        next_label="下一幕 →",
        play_label="▶ 播放",
        pause_label="⏸ 暂停",
        continuous_label="连续播放",
        beginning_label="开始",
        progress_end_label="觉悟之路展开",
        asset_prefix="../",
        audio_dir="../assets/audio/zh",
    )

    assert '<html lang="zh-Hans">' in html
    assert "<h1>佛陀的一生</h1>" in html
    assert "第01幕 / 42" in html
    assert "../assets/images/Buddha%20%28May%29%20-%20001" in html
    assert "../assets/audio/zh/Buddha%20%28May%29%20-%20001" in html
    assert "%E7%87%83%E7%81%AF%E4%BD%9B%E5%89%8D%E7%94%9F%E8%B5%B7%E5%A4%A7%E6%84%BF%20-%20cedar.mp3" in html


def test_write_html_creates_parent_directory():
    tools = load_tools()
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "cn/index.html"
        tools.write_html(target, "<!doctype html>")
        assert target.read_text(encoding="utf-8") == "<!doctype html>"


if __name__ == "__main__":
    tests = [
        test_parse_english_and_chinese_scenes,
        test_build_chinese_html_uses_local_audio_and_page_copy,
        test_write_html_creates_parent_directory,
    ]
    for test in tests:
        test()
