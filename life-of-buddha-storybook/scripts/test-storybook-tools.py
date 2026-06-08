#!/usr/bin/env python3
"""Smoke tests for storybook generation helpers."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile


PROJECT = Path(__file__).resolve().parents[1]
TOOLS_PATH = PROJECT / "scripts/storybook_tools.py"
GENERATE_AUDIO_PATH = PROJECT / "scripts/generate-audio.py"


def load_tools():
    spec = importlib.util.spec_from_file_location("storybook_tools", TOOLS_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_generate_audio():
    spec = importlib.util.spec_from_file_location("generate_audio", GENERATE_AUDIO_PATH)
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
    assert "Kusāvatī" in english[40]["paragraphs"][2]
    assert "he himself had been that king" in english[40]["paragraphs"][2]
    assert "six times before" in english[40]["paragraphs"][2]
    assert "the seventh time was as that wheel-turning monarch" in english[40]["paragraphs"][2]
    assert "no further laying down would follow" in english[40]["paragraphs"][2]
    assert "wheel-turning monarch" in english[5]["paragraphs"][1]
    assert "Taṇhā (craving or thirst)" in english[24]["paragraphs"][0]
    assert "Aratī (discontent or aversion)" in english[24]["paragraphs"][0]
    assert "Rāgā (passion or lust)" in english[24]["paragraphs"][0]
    assert "resolved not to teach" in english[27]["paragraphs"][0]
    assert "Brahmā Sahampati" in english[27]["paragraphs"][1]
    assert "world would be lost" in english[27]["paragraphs"][1]
    assert "eye of a Buddha" in english[27]["paragraphs"][2]
    assert "lotuses in a pond" in english[27]["paragraphs"][2]
    assert "拘舍婆提" in chinese[40]["paragraphs"][2]
    assert "转轮圣王大善见王" in chinese[40]["paragraphs"][2]
    assert "自己正是那位转轮圣王" in chinese[40]["paragraphs"][2]
    assert "舍身六次" in chinese[40]["paragraphs"][2]
    assert "第七次，正是以那位转轮圣王的身份在此舍身" in chinese[40]["paragraphs"][2]
    assert "此后不会再有下一次" in chinese[40]["paragraphs"][2]
    assert "Taṇhā（渴爱、贪求）" in chinese[24]["paragraphs"][0]
    assert "Aratī（不乐、不满）" in chinese[24]["paragraphs"][0]
    assert "Rāgā（贪染、欲爱）" in chinese[24]["paragraphs"][0]
    assert "决定不说法" in chinese[27]["paragraphs"][0]
    assert "梵天娑婆主" in chinese[27]["paragraphs"][1]
    assert "世间将失去机会" in chinese[27]["paragraphs"][1]
    assert "以佛眼观察世间" in chinese[27]["paragraphs"][2]
    assert "池中的莲花" in chinese[27]["paragraphs"][2]


def test_english_audio_filenames_keep_existing_ascii_style():
    tools = load_tools()
    generate_audio = load_generate_audio()
    english = tools.parse_scenes(
        PROJECT / "content/the-life-of-the-buddha-picture-storybook.en.md",
        "en",
    )
    chinese = tools.parse_scenes(
        PROJECT / "content/the-life-of-the-buddha-picture-storybook.zh.md",
        "zh",
    )

    english_target = generate_audio.output_path(english[40], Path("audio"), "en")
    chinese_target = generate_audio.output_path(chinese[40], Path("audio/zh"), "zh")

    assert english_target.name == "Buddha (May) - 041 - The Final Journey to Kusinara - cedar.mp3"
    assert chinese_target.name == "Buddha (May) - 041 - 病中前往拘尸那罗 - cedar.mp3"


def test_audio_narration_simplifies_mara_daughters_pali_names():
    tools = load_tools()
    generate_audio = load_generate_audio()
    english = tools.parse_scenes(
        PROJECT / "content/the-life-of-the-buddha-picture-storybook.en.md",
        "en",
    )
    chinese = tools.parse_scenes(
        PROJECT / "content/the-life-of-the-buddha-picture-storybook.zh.md",
        "zh",
    )

    english_audio_text = "\n\n".join(generate_audio.narration_paragraphs(english[24], "en"))
    chinese_audio_text = "\n\n".join(generate_audio.narration_paragraphs(chinese[24], "zh"))

    assert "Taṇhā" not in english_audio_text
    assert "Aratī" not in english_audio_text
    assert "Rāgā" not in english_audio_text
    assert "craving, discontent, and passion" in english_audio_text
    assert "Taṇhā" not in chinese_audio_text
    assert "Aratī" not in chinese_audio_text
    assert "Rāgā" not in chinese_audio_text
    assert "渴爱、不乐与贪染" in chinese_audio_text


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
    assert '<h1><a class="title-link" href="https://github.com/sampajano/dhamma-teachings" aria-label="Open source repository on GitHub">佛陀的一生</a></h1>' in html
    assert "source-link" not in html
    assert ">source</a>" not in html
    assert "第01幕 / 42" in html
    assert "../assets/images/Buddha%20%28May%29%20-%20001" in html
    assert "../assets/audio/zh/Buddha%20%28May%29%20-%20001" in html
    assert "%E7%87%83%E7%81%AF%E4%BD%9B%E5%89%8D%E7%94%9F%E8%B5%B7%E5%A4%A7%E6%84%BF%20-%20cedar.mp3" in html


def test_mobile_reader_controls_can_yield_to_story_text():
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

    assert "controls-collapsed" in html
    assert "controlsPeek" in html
    assert "showControls" in html
    assert "setControlsCollapsed" in html
    assert "controlsPeek.textContent = collapsed ? '⌃' : '⌄';" in html
    assert "隐藏控制条" in html
    assert ".reader {\n        height: auto;" in html
    assert "padding-bottom: calc(168px + env(safe-area-inset-bottom));" in html
    assert ".jump {\n        display: grid;\n        grid-template-columns: auto minmax(0, 1fr);" in html
    assert "width: 100%;\n        min-width: 0;" in html
    assert "padding: 24px 20px 36px" in html
    assert ".spread {\n        grid-template-columns: 1fr;\n        grid-template-rows: minmax(340px, 56svh) auto;\n        overflow: visible;" in html
    assert ".story-page {\n        min-height: 360px;\n        overflow: visible;" in html
    assert ".controls {\n        position: fixed;" in html
    assert ".controls button {\n        touch-action: manipulation;" in html
    assert "user-scalable=no" not in html
    assert "transform: translateY(calc(100% - 16px));" in html
    assert "isNearPageBottom" in html
    assert "if (isNearPageBottom()) return;" in html
    assert "currentY < 40 || isNearPageBottom()" in html
    assert "scheduleControlsAutoHide" in html


def test_rendered_html_can_open_to_page_from_query_or_hash():
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

    assert "function pageNumberFromUrl()" in html
    assert "new URLSearchParams(window.location.search).get('page')" in html
    assert "window.location.hash.match(/^#(\\d+)$/)" in html
    assert "function initialSceneIndex()" in html
    assert "return Math.max(0, Math.min(scenes.length - 1, pageNumber - 1));" in html
    assert "render(initialSceneIndex());" in html


def test_write_html_creates_parent_directory():
    tools = load_tools()
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "cn/index.html"
        tools.write_html(target, "<!doctype html>")
        assert target.read_text(encoding="utf-8") == "<!doctype html>"


if __name__ == "__main__":
    tests = [
        test_parse_english_and_chinese_scenes,
        test_english_audio_filenames_keep_existing_ascii_style,
        test_audio_narration_simplifies_mara_daughters_pali_names,
        test_build_chinese_html_uses_local_audio_and_page_copy,
        test_mobile_reader_controls_can_yield_to_story_text,
        test_rendered_html_can_open_to_page_from_query_or_hash,
        test_write_html_creates_parent_directory,
    ]
    for test in tests:
        test()
