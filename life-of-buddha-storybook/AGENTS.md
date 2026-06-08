# Life of the Buddha Storybook Agent Notes

## Generated Assets

- When changing story text in this project, update the generated page and audio assets in the same commit.
- Regenerate the English and Chinese MP3 narration for every scene whose text changed.
- Regenerate the full English and Chinese MP3 narration sets only when the user explicitly asks for a full audio refresh.
- Use the existing scripts from the repository root:
  - `python3 life-of-buddha-storybook/scripts/build-storybook-html.py`
  - `python3 life-of-buddha-storybook/scripts/generate-audio.py --language en --overwrite`
  - `python3 life-of-buddha-storybook/scripts/generate-audio.py --language zh --overwrite`
- After regenerating audio, verify at least the scenes whose text changed by transcription or another direct content check.
