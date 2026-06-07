#!/usr/bin/env python3
"""Generate per-scene MP3 narration for the Buddha storybook."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
import sys
import time
import unicodedata
import urllib.error
import urllib.request
from pathlib import Path

from storybook_tools import parse_scenes

PROJECT = Path(__file__).resolve().parents[1]
DEFAULT_EN_SOURCE = PROJECT / "content/the-life-of-the-buddha-picture-storybook.en.md"
DEFAULT_ZH_SOURCE = PROJECT / "content/the-life-of-the-buddha-picture-storybook.zh.md"
DEFAULT_EN_OUT_DIR = PROJECT / "assets/audio"
DEFAULT_ZH_OUT_DIR = PROJECT / "assets/audio/zh"
MODEL = "gpt-4o-mini-tts"
VOICE = "cedar"
RESPONSE_FORMAT = "mp3"
EN_INSTRUCTIONS = (
    "Read as a calm, mature male narrator with warmth, depth, and reverence. "
    "The pacing should be unhurried and clear, suitable for a contemplative "
    "storybook about the life of the Buddha. Avoid theatrical drama; keep the "
    "tone gentle, grounded, and spacious."
)
ZH_INSTRUCTIONS = (
    "Read in clear, natural Mandarin Chinese as a calm, mature male narrator "
    "with warmth, depth, and reverence. The pacing should be unhurried and "
    "suitable for a contemplative storybook about the life of the Buddha. "
    "Avoid theatrical drama; keep the tone gentle, grounded, and spacious."
)


def ascii_title(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    return "".join(char for char in normalized if not unicodedata.combining(char))


def output_path(scene: dict[str, object], out_dir: Path, language: str) -> Path:
    number = f"{int(scene['number']):03d}"
    title = ascii_title(str(scene["title"])) if language == "en" else str(scene["title"])
    return out_dir / f"Buddha (May) - {number} - {title} - cedar.mp3"


def narration_paragraphs(scene: dict[str, object], language: str) -> list[str]:
    paragraphs = [str(paragraph) for paragraph in scene["paragraphs"]]
    if scene["number"] == "25":
        if language == "en":
            paragraphs = [
                paragraph.replace(
                    "Tradition names them Taṇhā (craving or thirst), Aratī (discontent or aversion), and Rāgā (passion or lust).",
                    "Tradition remembers these daughters as craving, discontent, and passion.",
                )
                for paragraph in paragraphs
            ]
        elif language == "zh":
            paragraphs = [
                paragraph.replace(
                    "传统中称她们为 Taṇhā（渴爱、贪求）、Aratī（不乐、不满）与 Rāgā（贪染、欲爱）。",
                    "传统中称她们象征渴爱、不乐与贪染。",
                )
                for paragraph in paragraphs
            ]
    return paragraphs


def request_speech(scene: dict[str, object], api_key: str, language: str) -> bytes:
    scene_number = int(scene["number"])
    body = "\n\n".join(narration_paragraphs(scene, language))
    if language == "zh":
        input_text = f"第{scene_number}幕。{scene['title']}。\n\n{body}"
        instructions = ZH_INSTRUCTIONS
    else:
        input_text = f"Scene {scene_number}. {scene['title']}.\n\n{body}"
        instructions = EN_INSTRUCTIONS
    payload = {
        "model": MODEL,
        "voice": VOICE,
        "input": input_text,
        "instructions": instructions,
        "response_format": RESPONSE_FORMAT,
    }
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        "https://api.openai.com/v1/audio/speech",
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    for attempt in range(1, 4):
        try:
            with urllib.request.urlopen(request, timeout=180) as response:
                return response.read()
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            if attempt == 3:
                raise RuntimeError(f"OpenAI API error for scene {scene['number']}: {detail}") from exc
        except (TimeoutError, urllib.error.URLError) as exc:
            if attempt == 3:
                raise RuntimeError(f"Network error for scene {scene['number']}: {exc}") from exc
        time.sleep(1.5 * attempt)
    raise RuntimeError(f"Failed to generate scene {scene['number']}")


def generate_one(
    scene: dict[str, object],
    api_key: str,
    overwrite: bool,
    out_dir: Path,
    language: str,
) -> str:
    target = output_path(scene, out_dir, language)
    if target.exists() and not overwrite:
        return f"skip {scene['number']} {target.name}"
    audio = request_speech(scene, api_key, language)
    target.write_bytes(audio)
    return f"wrote {scene['number']} {target.name} ({len(audio):,} bytes)"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--scene",
        action="append",
        help="Generate only a specific scene number, such as 01. May be repeated.",
    )
    parser.add_argument("--language", choices=["en", "zh"], default="en")
    parser.add_argument("--source", type=Path, help="Markdown source file.")
    parser.add_argument("--out-dir", type=Path, help="Output directory for MP3 files.")
    parser.add_argument("--overwrite", action="store_true", help="Regenerate existing MP3 files.")
    parser.add_argument("--concurrency", type=int, default=1, help="Number of parallel API requests.")
    parser.add_argument("--sleep", type=float, default=0.25, help="Pause between API requests.")
    args = parser.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEY is not set", file=sys.stderr)
        return 2

    source = args.source or (DEFAULT_ZH_SOURCE if args.language == "zh" else DEFAULT_EN_SOURCE)
    out_dir = args.out_dir or (DEFAULT_ZH_OUT_DIR if args.language == "zh" else DEFAULT_EN_OUT_DIR)
    requested = {f"{int(scene):02d}" for scene in args.scene or []}
    scenes = [
        scene
        for scene in parse_scenes(source, args.language)
        if not requested or scene["number"] in requested
    ]
    out_dir.mkdir(parents=True, exist_ok=True)

    concurrency = max(1, args.concurrency)
    if concurrency == 1:
        for scene in scenes:
            print(f"start {scene['number']} {scene['title']}", flush=True)
            print(generate_one(scene, api_key, args.overwrite, out_dir, args.language), flush=True)
            time.sleep(args.sleep)
        return 0

    failures = []
    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = {
            executor.submit(generate_one, scene, api_key, args.overwrite, out_dir, args.language): scene
            for scene in scenes
        }
        for future in as_completed(futures):
            scene = futures[future]
            try:
                print(future.result(), flush=True)
            except Exception as exc:
                failures.append((scene["number"], str(exc)))
                print(f"failed {scene['number']} {scene['title']}: {exc}", file=sys.stderr, flush=True)

    if failures:
        print("Failures:", file=sys.stderr)
        for number, reason in failures:
            print(f"- {number}: {reason}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
