#!/usr/bin/env python3
"""Shared helpers for the Buddha storybook pages and audio scripts."""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import quote


PROJECT = Path(__file__).resolve().parents[1]
ENGLISH_INDEX = PROJECT / "index.html"


def _scene_pattern(language: str) -> re.Pattern[str]:
    if language == "en":
        heading = r"Scene (?P<number>\d{2}) - (?P<title>.+?)"
    elif language == "zh":
        heading = r"第(?P<number>\d{2})幕 - (?P<title>.+?)"
    else:
        raise ValueError(f"Unsupported language: {language}")

    return re.compile(
        rf"^## {heading}\n"
        r"!\[(?P<alt>.*?)\]\((?P<image>.*?)\)\n\n"
        r"(?P<body>.*?)(?=^## (?:Scene \d{2} - |第\d{2}幕 - )|\Z)",
        re.M | re.S,
    )


def parse_scenes(source: Path, language: str) -> list[dict[str, object]]:
    text = source.read_text(encoding="utf-8")
    scenes: list[dict[str, object]] = []
    for match in _scene_pattern(language).finditer(text):
        body = match.group("body").strip()
        paragraphs = [part.strip() for part in re.split(r"\n\s*\n", body) if part.strip()]
        image = match.group("image").strip()
        scenes.append(
            {
                "number": match.group("number"),
                "title": match.group("title").strip(),
                "image": image.removeprefix("../"),
                "paragraphs": paragraphs,
            }
        )

    if len(scenes) != 42:
        raise RuntimeError(f"Expected 42 scenes in {source}, found {len(scenes)}")
    return scenes


def _read_style() -> str:
    html = ENGLISH_INDEX.read_text(encoding="utf-8")
    match = re.search(r"<style>(.*?)</style>", html, re.S)
    if not match:
        raise RuntimeError(f"Could not find <style> block in {ENGLISH_INDEX}")
    return match.group(1)


def _audio_filename(scene: dict[str, object]) -> str:
    number = f"{int(str(scene['number'])):03d}"
    title = str(scene["title"])
    return f"Buddha (May) - {number} - {title} - cedar.mp3"


def _url(path: str) -> str:
    return quote(path, safe="/%")


def _scene_data(
    scenes: list[dict[str, object]],
    *,
    asset_prefix: str,
    audio_dir: str,
) -> list[dict[str, object]]:
    data: list[dict[str, object]] = []
    for scene in scenes:
        image = f"{asset_prefix}{scene['image']}"
        audio = f"{audio_dir.rstrip('/')}/{_audio_filename(scene)}"
        data.append(
            {
                "number": scene["number"],
                "title": scene["title"],
                "image": _url(image),
                "paragraphs": scene["paragraphs"],
                "audio": _url(audio),
            }
        )
    return data


def render_html(
    *,
    scenes: list[dict[str, object]],
    language: str,
    book_title: str,
    page_title: str,
    scene_label: str,
    scene_suffix: str,
    scene_select_label: str,
    previous_label: str,
    next_label: str,
    play_label: str,
    pause_label: str,
    continuous_label: str,
    beginning_label: str,
    progress_end_label: str,
    audio_dir: str,
    asset_prefix: str = "",
) -> str:
    data = _scene_data(scenes, asset_prefix=asset_prefix, audio_dir=audio_dir)
    scenes_json = json.dumps(data, ensure_ascii=False, indent=2)
    labels_json = json.dumps(
        {
            "bookTitle": book_title,
            "scene": scene_label,
            "sceneSuffix": scene_suffix,
            "sceneSelect": scene_select_label,
            "previous": previous_label,
            "next": next_label,
            "play": play_label,
            "pause": pause_label,
            "playAria": "播放旁白" if language.startswith("zh") else "Play narration",
            "pauseAria": "暂停旁白" if language.startswith("zh") else "Pause narration",
            "continuous": continuous_label,
            "beginning": beginning_label,
            "complete": "圆满" if language.startswith("zh") else "Complete",
            "awakening": "觉悟" if language.startswith("zh") else "Awakening",
            "teachingUnfolds": "教法展开" if language.startswith("zh") else "Teaching unfolds",
            "afterAwakening": "成道之后" if language.startswith("zh") else "After awakening",
            "progressEnd": progress_end_label,
        },
        ensure_ascii=False,
        indent=2,
    )
    total = f"{len(scenes):02d}"
    first_scene = f"{scene_label}{scenes[0]['number']}{scene_suffix}"
    controls_aria = "显示控制条" if language.startswith("zh") else "Show controls"
    style = _read_style()
    return f"""<!doctype html>
<html lang="{language}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{page_title}</title>
  <style>{style}</style>
</head>
<body>
  <main class="reader" aria-live="polite">
    <header class="topbar">
      <div class="book-title">
        <h1>{book_title}</h1>
        <div class="counter" id="counter">{first_scene} / {total}</div>
      </div>
      <div class="jump">
        <label for="sceneSelect">{scene_select_label}</label>
        <select id="sceneSelect" aria-label="{scene_select_label}"></select>
      </div>
    </header>

    <section class="spread">
      <figure class="image-page" aria-label="{scene_select_label}">
        <img id="sceneImage" alt="">
      </figure>
      <article class="story-page">
        <p class="kicker" id="kicker">{first_scene}</p>
        <h2 class="scene-title" id="sceneTitle"></h2>
        <div class="story-text" id="storyText"></div>
      </article>
    </section>

    <footer class="controls controls-collapsed">
      <button class="controls-peek" id="controlsPeek" type="button" aria-label="{controls_aria}">⌃</button>
      <button class="nav-button" id="prevButton" type="button" aria-label="{previous_label}">{previous_label}</button>
      <div class="audio-tools">
        <button class="audio-button" id="playButton" type="button" aria-label="{play_label}">{play_label}</button>
        <label class="auto-toggle">
          <input id="autoAdvance" type="checkbox">
          {continuous_label}
        </label>
        <span class="audio-time" id="audioTime">0:00 / 0:00</span>
      </div>
      <div class="progress-wrap" aria-hidden="true">
        <div class="progress-label">
          <span id="progressStart">{beginning_label}</span>
          <span id="progressEnd">{progress_end_label}</span>
        </div>
        <div class="progress-track"><div class="progress-bar" id="progressBar"></div></div>
      </div>
      <button class="nav-button" id="nextButton" type="button" aria-label="{next_label}">{next_label}</button>
      <audio id="sceneAudio" preload="metadata"></audio>
    </footer>
  </main>

  <script>
    const scenes = {scenes_json};
    const labels = {labels_json};

    const state = {{
      index: 0,
      shouldPlayAudio: false
    }};
    const $ = (selector) => document.querySelector(selector);
    const sceneSelect = $('#sceneSelect');
    const sceneImage = $('#sceneImage');
    const sceneAudio = $('#sceneAudio');
    const storyText = $('#storyText');
    const storyPage = $('.story-page');
    const controls = $('.controls');
    const controlsPeek = $('#controlsPeek');
    const playButton = $('#playButton');
    const autoAdvance = $('#autoAdvance');
    const audioTime = $('#audioTime');
    let controlsAutoHideTimer = 0;

    function escapeHtml(value) {{
      return value.replace(/[&<>"]/g, (char) => ({{
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;'
      }}[char]));
    }}

    function sceneName(scene) {{
      return `${{labels.scene}}${{scene.number}}${{labels.sceneSuffix}}`;
    }}

    function renderOptions() {{
      sceneSelect.innerHTML = scenes.map((scene, index) => (
        `<option value="${{index}}">${{sceneName(scene)}} - ${{escapeHtml(scene.title)}}</option>`
      )).join('');
    }}

    function formatTime(value) {{
      if (!Number.isFinite(value) || value < 0) return '0:00';
      const minutes = Math.floor(value / 60);
      const seconds = Math.floor(value % 60);
      return `${{minutes}}:${{String(seconds).padStart(2, '0')}}`;
    }}

    function updateAudioTime() {{
      audioTime.textContent = `${{formatTime(sceneAudio.currentTime)}} / ${{formatTime(sceneAudio.duration)}}`;
    }}

    function updatePlayButton() {{
      const isPlaying = !sceneAudio.paused && !sceneAudio.ended;
      playButton.textContent = isPlaying ? labels.pause : labels.play;
      playButton.setAttribute('aria-label', isPlaying ? labels.pauseAria : labels.playAria);
    }}

    function progressEndLabel(scene) {{
      const sceneNumber = Number(scene.number);
      if (sceneNumber === scenes.length) return labels.complete;
      if (sceneNumber === 26) return labels.awakening;
      if (sceneNumber >= 29) return labels.teachingUnfolds;
      if (sceneNumber > 26) return labels.afterAwakening;
      return labels.progressEnd;
    }}

    function isMobileLayout() {{
      return window.matchMedia('(max-width: 900px)').matches;
    }}

    function showControls() {{
      controls.classList.remove('controls-collapsed');
      scheduleControlsAutoHide();
    }}

    function scheduleControlsAutoHide() {{
      window.clearTimeout(controlsAutoHideTimer);
      if (!isMobileLayout()) return;
      controlsAutoHideTimer = window.setTimeout(hideControls, 4200);
    }}

    function hideControls() {{
      if (!isMobileLayout() || document.activeElement.closest?.('.controls')) return;
      controls.classList.add('controls-collapsed');
    }}

    function playCurrentAudio() {{
      state.shouldPlayAudio = true;
      showControls();
      sceneAudio.play().then(updatePlayButton).catch(() => {{
        state.shouldPlayAudio = false;
        updatePlayButton();
      }});
    }}

    function pauseAudio() {{
      state.shouldPlayAudio = false;
      sceneAudio.pause();
      updatePlayButton();
    }}

    function render(index, options = {{}}) {{
      const wasPlaying = state.shouldPlayAudio && !sceneAudio.paused;
      state.index = Math.max(0, Math.min(scenes.length - 1, index));
      const scene = scenes[state.index];
      sceneImage.classList.add('fade-out');
      window.setTimeout(() => {{
        sceneImage.src = scene.image;
        sceneImage.alt = `${{sceneName(scene)}} - ${{scene.title}}`;
        sceneImage.classList.remove('fade-out');
      }}, 90);

      $('#counter').textContent = `${{sceneName(scene)}} / ${{String(scenes.length).padStart(2, '0')}}`;
      $('#kicker').textContent = sceneName(scene);
      $('#sceneTitle').textContent = scene.title;
      storyText.innerHTML = scene.paragraphs.map((paragraph) => `<p>${{escapeHtml(paragraph)}}</p>`).join('');
      storyPage.scrollTop = 0;
      sceneSelect.value = String(state.index);
      $('#prevButton').disabled = state.index === 0;
      $('#nextButton').disabled = state.index === scenes.length - 1;
      $('#progressBar').style.width = `${{((state.index + 1) / scenes.length) * 100}}%`;
      $('#progressStart').textContent = state.index === 0 ? labels.beginning : sceneName(scene);
      $('#progressEnd').textContent = progressEndLabel(scene);
      document.title = `${{sceneName(scene)}} - ${{scene.title}} | ${{labels.bookTitle}}`;
      sceneAudio.src = scene.audio;
      sceneAudio.load();
      updateAudioTime();
      updatePlayButton();
      if (options.play || wasPlaying) {{
        playCurrentAudio();
      }} else if (options.keepControls) {{
        showControls();
      }} else {{
        hideControls();
      }}
    }}

    $('#prevButton').addEventListener('click', () => {{
      showControls();
      render(state.index - 1, {{ keepControls: true }});
    }});
    $('#nextButton').addEventListener('click', () => {{
      showControls();
      render(state.index + 1, {{ keepControls: true }});
    }});
    controlsPeek.addEventListener('click', showControls);
    sceneSelect.addEventListener('change', (event) => {{
      showControls();
      render(Number(event.target.value), {{ keepControls: true }});
    }});
    playButton.addEventListener('click', () => {{
      showControls();
      if (sceneAudio.paused || sceneAudio.ended) {{
        playCurrentAudio();
      }} else {{
        pauseAudio();
      }}
    }});

    let lastScrollY = window.scrollY;
    let scrollTimer = 0;
    window.addEventListener('scroll', () => {{
      if (!isMobileLayout()) return;
      window.clearTimeout(scrollTimer);
      const currentY = window.scrollY;
      const scrollingDown = currentY > lastScrollY + 8;
      if (currentY < 40) {{
        showControls();
      }} else if (scrollingDown) {{
        scrollTimer = window.setTimeout(hideControls, 80);
      }} else {{
        hideControls();
      }}
      lastScrollY = currentY;
    }}, {{ passive: true }});

    sceneAudio.addEventListener('loadedmetadata', updateAudioTime);
    sceneAudio.addEventListener('timeupdate', updateAudioTime);
    sceneAudio.addEventListener('play', updatePlayButton);
    sceneAudio.addEventListener('pause', updatePlayButton);
    sceneAudio.addEventListener('ended', () => {{
      updatePlayButton();
      if (autoAdvance.checked && state.index < scenes.length - 1) {{
        render(state.index + 1, {{ play: true }});
      }} else {{
        state.shouldPlayAudio = false;
      }}
    }});

    window.addEventListener('keydown', (event) => {{
      if (event.defaultPrevented) return;
      if (event.key === 'ArrowLeft') render(state.index - 1);
      if (event.key === 'ArrowRight') render(state.index + 1);
      if (event.key === 'Home') render(0);
      if (event.key === 'End') render(scenes.length - 1);
    }});

    renderOptions();
    render(0);
    window.storybook = {{ render, scenes }};
  </script>
</body>
</html>
"""


def write_html(target: Path, html: str) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html, encoding="utf-8")
