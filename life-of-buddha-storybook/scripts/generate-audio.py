#!/usr/bin/env python3
"""Generate per-scene MP3 narration for the English Buddha storybook."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
SOURCE = PROJECT / "content/the-life-of-the-buddha-picture-storybook.en.md"
OUT_DIR = PROJECT / "assets/audio"
MODEL = "gpt-4o-mini-tts"
VOICE = "cedar"
RESPONSE_FORMAT = "mp3"
INSTRUCTIONS = (
    "Read as a calm, mature male narrator with warmth, depth, and reverence. "
    "The pacing should be unhurried and clear, suitable for a contemplative "
    "storybook about the life of the Buddha. Avoid theatrical drama; keep the "
    "tone gentle, grounded, and spacious."
)


def parse_scenes() -> list[dict[str, str]]:
    text = SOURCE.read_text(encoding="utf-8")
    pattern = re.compile(
        r"^## Scene (\d{2}) - (.+?)\n!\[.*?\]\(.+?\)\n\n(.*?)(?=\n## Scene \d{2} - |\Z)",
        re.S | re.M,
    )
    scenes = []
    for number, title, body in pattern.findall(text):
        scenes.append(
            {
                "number": number,
                "title": title.strip(),
                "body": body.strip(),
            }
        )
    if len(scenes) != 42:
        raise RuntimeError(f"Expected 42 scenes, found {len(scenes)}")
    return scenes


def output_path(scene: dict[str, str]) -> Path:
    number = f"{int(scene['number']):03d}"
    return OUT_DIR / f"Buddha (May) - {number} - {scene['title']} - cedar.mp3"


def request_speech(scene: dict[str, str], api_key: str) -> bytes:
    scene_number = int(scene["number"])
    input_text = f"Scene {scene_number}. {scene['title']}.\n\n{scene['body']}"
    payload = {
        "model": MODEL,
        "voice": VOICE,
        "input": input_text,
        "instructions": INSTRUCTIONS,
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


def generate_one(scene: dict[str, str], api_key: str, overwrite: bool) -> str:
    target = output_path(scene)
    if target.exists() and not overwrite:
        return f"skip {scene['number']} {target.name}"
    audio = request_speech(scene, api_key)
    target.write_bytes(audio)
    return f"wrote {scene['number']} {target.name} ({len(audio):,} bytes)"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--scene",
        action="append",
        help="Generate only a specific scene number, such as 01. May be repeated.",
    )
    parser.add_argument("--overwrite", action="store_true", help="Regenerate existing MP3 files.")
    parser.add_argument("--concurrency", type=int, default=1, help="Number of parallel API requests.")
    parser.add_argument("--sleep", type=float, default=0.25, help="Pause between API requests.")
    args = parser.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEY is not set", file=sys.stderr)
        return 2

    requested = {f"{int(scene):02d}" for scene in args.scene or []}
    scenes = [scene for scene in parse_scenes() if not requested or scene["number"] in requested]
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    concurrency = max(1, args.concurrency)
    if concurrency == 1:
        for scene in scenes:
            print(f"start {scene['number']} {scene['title']}", flush=True)
            print(generate_one(scene, api_key, args.overwrite), flush=True)
            time.sleep(args.sleep)
        return 0

    failures = []
    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = {
            executor.submit(generate_one, scene, api_key, args.overwrite): scene
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
