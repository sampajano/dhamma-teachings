# Buddha Storybook Audio Generation

Source storybook:
`life-of-buddha-storybook/content/the-life-of-the-buddha-picture-storybook.en.md`

Output directory:
`life-of-buddha-storybook/assets/audio/`

Generation script:
`life-of-buddha-storybook/scripts/generate-audio.py`

Recommended command:

```bash
python3 life-of-buddha-storybook/scripts/generate-audio.py --concurrency 4
```

The script skips existing MP3 files unless `--overwrite` is passed. A moderate concurrency such as `4` makes the full book much faster while still keeping API requests reasonably gentle.

Early audition samples, when preserved, live in:
`life-of-buddha-storybook/context/audio-samples/`

## Chosen Voice

- Model: `gpt-4o-mini-tts`
- Voice: `cedar`
- Format: `mp3`
- Rationale: `cedar` gave the best sample for this project: calm, warm, mature, and less theatrical than the lower but heavier `onyx` sample.

Voice instruction:

```text
Read as a calm, mature male narrator with warmth, depth, and reverence. The pacing should be unhurried and clear, suitable for a contemplative storybook about the life of the Buddha. Avoid theatrical drama; keep the tone gentle, grounded, and spacious.
```

## Naming

Formal per-scene files use:

```text
Buddha (May) - 001 - The Great Aspiration Before Dīpaṅkara Buddha - cedar.mp3
```

The scene number and English title match the storybook and image sequence.

## Cost Estimate

The English book has 42 scenes and about 7,497 words including scene titles. Based on the first-page `cedar` sample, the full narration should be about 46 to 50 minutes.

At the checked OpenAI TTS pricing, the expected full-book generation cost is roughly `$0.70-$0.76`, plus a very small text input cost. Actual cost should be verified in the OpenAI usage dashboard after generation.

## HTML Playback

Browsers usually block audio autoplay until the reader clicks a playback control. The flip book should therefore use a user-initiated play button, then allow continuous playback and automatic scene advancement after that gesture.
