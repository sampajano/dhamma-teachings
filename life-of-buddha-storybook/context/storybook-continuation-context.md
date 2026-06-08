# Continuation Context: 佛陀的一生图像故事书

> Archived source context from the original Obsidian-vault workflow.
> Some paths and scene counts below describe earlier working states before the storybook was extracted into this standalone repository.

Created: 2026-06-06

This note is meant to be pasted into a new Codex conversation so it can continue improving the same project with enough context.

## One-Sentence Goal

We are creating and refining a Chinese Obsidian picture storybook of the Buddha's life, using a sequence of AI-generated / curated images, with flowing beginner-friendly storytelling that feels like a real illustrated storybook rather than captions, lecture notes, or doctrinal bullet points.

## Where The Work Lives

Obsidian vault:

`<original-obsidian-vault>`

Main Chinese storybook note:

`<original-obsidian-vault>/Dhamma/Blog/(2026-06-05) 佛陀的一生 - 图像故事书.md`

English reference storybook note:

`<original-obsidian-vault>/Dhamma/Blog/(2026-05-30) The Life of the Buddha - A Picture Storybook.md`

Image attachment folder:

`<original-obsidian-vault>/Dhamma/Attachments/(2026) Buddha's life/`

There are currently 38 official image files named like:

`Buddha (May) - 001 - ...png`

The Chinese note currently embeds all 38 images using vault-relative Obsidian embeds, for example:

`![[Dhamma/Attachments/(2026) Buddha's life/Buddha (May) - 001 - The Vow Before Dīpaṅkara Buddha.png]]`

## Local Vault Instructions

The vault has `<original-obsidian-vault>/AGENTS.MD`.

Important rules from that file:

- Treat this as an Obsidian vault.
- Prefer Obsidian wiki-links and embeds over raw Markdown links.
- Keep agent temporary files under `Agents/tmp/`.
- Preserve naming consistency and update links if moving/renaming notes.
- The local instruction says to end responses with `Namo Buddhaya 🙏`.

There is also a broader user preference from `<home>/Downloads/AGENTS.md`:

- User-facing replies should start with `Hi Eryu, Please be mindful :)`.
- Default language should be Chinese unless there is a reason otherwise.
- The user appreciates thoughtful critique and does not want blindly executed bad assumptions.

## Current Shape Of The Chinese Note

The Chinese note has this structure:

```md
---
created-at: 2026-06-05 00:00
tags:
  - dhamma/buddha-life
  - buddhism/story
  - 中文
---
图像由法友May理想化构思并使用 ChatGPT 生成 😊🙏

# 佛陀的一生 - 图像故事书
Tags:: [[Buddha]], [[Dhamma]]

## 第01幕 - ...
![[...png]]

叙事段落 1

叙事段落 2

叙事段落 3
```

Important structural decision:

- We removed the separate `故事与因缘：` section.
- We removed the separate `意义：` section.
- We removed the separate `**事件：...**` line because it duplicated the scene title and made the story feel more like captioned notes.
- Each scene now has only:
  - heading
  - image embed
  - 3-ish paragraphs of flowing story.

This was deliberate. The user felt the separate `意义` section sounded too much like a moral lesson / lecture. Meaning should now be woven naturally into the story, usually in the final sentence or final paragraph, and only when it helps.

## Desired Writing Style

The user wants this to read like a warm, clear, detailed illustrated storybook for beginners.

Good style:

- Tell the event directly.
- Add setting, mood, people present, emotional texture, and narrative transition.
- Explain significance gently through the story itself.
- Keep beginners in mind without saying "对初学者来说".
- Use simple but dignified Chinese.
- Let the scene breathe.
- Use 3 to 4 paragraphs per scene if helpful.
- For key scenes, longer is okay.
- The user wants it "quite a bit longer" than captions, but not bloated.

Avoid:

- `传统故事说...`
- `传说...`
- `佛传中...`
- `对初学者来说...`
- `这一幕说明...`
- `这个故事象征...`
- `这提醒我们...`
- `可以理解为...`
- lecture-style moralizing
- meta-writing like "这里不应..."
- prematurely explaining later doctrinal insights before the story timeline reaches them

The user specifically disliked this kind of tone:

> 对初学者来说，这一幕很重要，因为它说明...

They also disliked a standalone `意义` section sounding like a teacher giving a conclusion.

## Timeline And Doctrinal Accuracy Notes

Be careful about timeline. The user catches chronological issues.

Critical example already fixed:

- In the marriage scene with Yasodharā, do not say Siddhartha already understands aging/death deeply, because he has not yet seen the Four Sights.
- Before Scene 11, avoid using the later Four Sights insight as if Siddhartha already has it.
- A validation check was run so scenes before Scene 11 no longer contain old/sick/death terms such as `老、病、死`, `老人`, `病人`, `死人`, `死亡`, `衰老`, `疾病`.

Scene 16 and 18 terminology:

- Scene 16: Ālāra Kālāma / 阿罗逻迦蓝 teaches `无所有处`.
- In this storybook we call it `第七禅（无所有处）的深定`.
- Current wording says: `若以色界四禅加上四无色定来计算，这就是第七禅`.
- Scene 18: Uddaka Rāmaputta / 郁陀迦罗摩子 teaches `非想非非想处`.
- In this storybook we call it `第八禅（非想非非想处）的微细境界`.
- Current wording says this is the highest level in that meditation system.
- Do not say "几乎最高". The user corrected this: it is already the highest.

Scene 36:

- This is Devadatta injuring the Buddha's foot with a rock fragment, and the doctor Jīvaka Komārabhacca / 耆婆童子 treating the Buddha's foot.
- The user previously corrected this scene.

Scene 31 and 32:

- Scene 31 is Yasodharā seeing the Buddha again after his awakening and return to Kapilavatthu.
- Scene 32 is the Buddha instructing Rāhula.
- Earlier there was confusion about scenes 22-24; ignore older assumptions. The current order places Yasodharā/Rāhula after the establishment of the Saṅgha and before later teaching scenes.

Scene 24/25/26:

- Māra's army, Māra's daughters, earth-witness/awakening are separate sequential scenes.

Scene 1 wording:

- The current title is `燃灯佛前生起大愿`.
- Avoid wording such as `初见燃灯佛`, because it may sound as if Sumedha met Dīpaṅkara Buddha multiple times in that life.
- The first two scenes should feel like one continuous Dīpaṅkara-Buddha occasion: Scene 1 shows reverent offering and the arising of the vow; Scene 2 shows the stronger embodied action of lying in the mud and receiving the prophecy.

## Current Scene List

As of 2026-06-06, the Chinese note validates as:

- 38 scenes
- 38 embeds
- 0 `事件` labels
- 0 `故事与因缘` labels
- 0 `意义` labels
- 0 "traditional framing" terms such as `传统`, `传说`, `佛传`, etc.
- 0 `几乎最高`
- 0 pre-Scene-11 old/sick/death terms in scene bodies

Current scene headings and image embeds:

| #   | Heading      | Image                                                                                                          |
| --- | ------------ | -------------------------------------------------------------------------------------------------------------- |
| 01  | 燃灯佛前生起大愿     | `Dhamma/Attachments/(2026) Buddha's life/Buddha (May) - 001 - The Vow Before Dīpaṅkara Buddha.png`             |
| 02  | 铺发泥中与未来成佛的授记 | `Dhamma/Attachments/(2026) Buddha's life/Buddha (May) - 002 - The Prophecy of Future Buddhahood.png`           |
| 03  | 摩耶夫人的白象梦     | `Dhamma/Attachments/(2026) Buddha's life/Buddha (May) - 003 - Queen Māyā's Dream.png`                          |
| 04  | 蓝毗尼园中的摩耶夫人   | `Dhamma/Attachments/(2026) Buddha's life/Buddha (May) - 004 - Queen Māyā in Lumbinī Grove.png`                 |
| 05  | 悉达多太子的诞生     | `Dhamma/Attachments/(2026) Buddha's life/Buddha (May) - 005 - The Birth of Prince Siddhartha.png`              |
| 06  | 阿私陀仙人的预言     | `Dhamma/Attachments/(2026) Buddha's life/Buddha (May) - 006 - The Sage Asita's Prediction.png`                 |
| 07  | 少年太子的树下禅定    | `Dhamma/Attachments/(2026) Buddha's life/Buddha (May) - 007 - The Young Prince Enters Meditation.png`          |
| 08  | 悉达多救护受伤的天鹅   | `Dhamma/Attachments/(2026) Buddha's life/Buddha (May) - 008 - Siddhartha Saves the Wounded Swan.png`           |
| 09  | 太子的技艺与力量     | `Dhamma/Attachments/(2026) Buddha's life/Buddha (May) - 009 - The Prince's Skill and Strength.png`             |
| 10  | 悉达多与耶输陀罗成婚   | `Dhamma/Attachments/(2026) Buddha's life/Buddha (May) - 010 - The Marriage of Siddhartha and Yasodharā.png`    |
| 11  | 四门出游与四种相     | `Dhamma/Attachments/(2026) Buddha's life/Buddha (May) - 011 - The Four Sights.png`                             |
| 12  | 宫中欲乐失去魅力     | `Dhamma/Attachments/(2026) Buddha's life/Buddha (May) - 012 - The Palace Pleasures Lose Their Charm.png`       |
| 13  | 静默的告别        | `Dhamma/Attachments/(2026) Buddha's life/Buddha (May) - 013 - The Silent Farewell.png`                         |
| 14  | 伟大的出离        | `Dhamma/Attachments/(2026) Buddha's life/Buddha (May) - 014 - The Great Renunciation.png`                      |
| 15  | 削发舍弃王相       | `Dhamma/Attachments/(2026) Buddha's life/Buddha (May) - 015 - Cutting the Hair.png`                            |
| 16  | 跟随阿罗逻迦蓝学习   | `Dhamma/Attachments/(2026) Buddha's life/Buddha (May) - 016 - Learning from Āḷāra Kālāma.png`                  |
| 17  | 离开阿罗逻迦蓝     | `Dhamma/Attachments/(2026) Buddha's life/Buddha (May) - 017 - Leaving Āḷāra Kālāma.png`                        |
| 18  | 跟随郁陀迦罗摩子学习   | `Dhamma/Attachments/(2026) Buddha's life/Buddha (May) - 018 - Learning from Uddaka Rāmaputta.png`              |
| 19  | 离开郁陀迦罗摩子     | `Dhamma/Attachments/(2026) Buddha's life/Buddha (May) - 019 - Leaving Uddaka Rāmaputta.png`                    |
| 20  | 与五位苦行者同修     | `Dhamma/Attachments/(2026) Buddha's life/Buddha (May) - 020 - Siddhartha Practices with the Five Ascetics.png` |
| 21  | 苦行的极限        | `Dhamma/Attachments/(2026) Buddha's life/Buddha (May) - 021 - The Limits of Austerity.png`                     |
| 22  | 善生女供养乳糜      | `Dhamma/Attachments/(2026) Buddha's life/Buddha (May) - 022 - Sujātā's Offering.png`                           |
| 23  | 金钵顺流与逆流      | `Dhamma/Attachments/(2026) Buddha's life/Buddha (May) - 023 - The Golden Bowl and the River.png`               |
| 24  | 魔军来袭         | `Dhamma/Attachments/(2026) Buddha's life/Buddha (May) - 024 - Māra's Army Attacks.png`                         |
| 25  | 魔女的诱惑        | `Dhamma/Attachments/(2026) Buddha's life/Buddha (May) - 025 - The Temptations of Māra's Daughters.png`         |
| 26  | 触地降魔与觉悟      | `Dhamma/Attachments/(2026) Buddha's life/Buddha (May) - 026 - The Earth-Witness and Awakening.png`             |
| 27  | 目支邻陀龙王护佛     | `Dhamma/Attachments/(2026) Buddha's life/Buddha (May) - 027 - Mucalinda Protects the Buddha.png`               |
| 28  | 梵天劝请说法       | `Dhamma/Attachments/(2026) Buddha's life/Buddha (May) - 028 - Brahmā Requests the Teaching.png`                |
| 29  | 初转法轮         | `Dhamma/Attachments/(2026) Buddha's life/Buddha (May) - 029 - The First Turning of the Wheel.png`              |
| 30  | 僧团围绕正法建立     | `Dhamma/Attachments/(2026) Buddha's life/Buddha (May) - 030 - The Saṅgha Gathers Around the Teaching.png`      |
| 31  | 耶输陀罗再见佛陀     | `Dhamma/Attachments/(2026) Buddha's life/Buddha (May) - 031 - Yasodharā Meets the Buddha Again.png`            |
| 32  | 佛陀教导罗睺罗      | `Dhamma/Attachments/(2026) Buddha's life/Buddha (May) - 032 - The Buddha Instructs Rāhula.png`                 |
| 33  | 忉利天为母说法      | `Dhamma/Attachments/(2026) Buddha's life/Buddha (May) - 033 - Teaching in Tāvatiṃsa Heaven.png`                |
| 34  | 从天界降下        | `Dhamma/Attachments/(2026) Buddha's life/Buddha (May) - 034 - The Descent from Heaven.png`                     |
| 35  | 央掘魔罗的转化      | `Dhamma/Attachments/(2026) Buddha's life/Buddha (May) - 035 - Aṅgulimāla Is Transformed.png`                   |
| 36  | 耆婆为佛陀疗足      | `Dhamma/Attachments/(2026) Buddha's life/Buddha (May) - 036 - Jīvaka Treats the Buddha's Foot.png`             |
| 37  | 调伏那罗祇利象      | `Dhamma/Attachments/(2026) Buddha's life/Buddha (May) - 037 - The Taming of Nāḷāgiri.png`                      |
| 38  | 般涅槃          | `Dhamma/Attachments/(2026) Buddha's life/Buddha (May) - 038 - The Parinibbāna.png`                             |

## Current Validation Command

Use this after edits to make sure the note still has the right structure and that image embeds exist:

```bash
python3 - <<'PY'
from pathlib import Path
import re
note=Path('<original-obsidian-vault>/Dhamma/Blog/(2026-06-05) 佛陀的一生 - 图像故事书.md')
root=Path('<original-obsidian-vault>')
text=note.read_text()
pat=re.compile(r'^## 第(\d{2})幕 - (.*?)\n(!\[\[(.*?)\]\])\n\n(.*?)(?=\n## 第\d{2}幕 - |\Z)', re.M|re.S)
scenes=pat.findall(text)
nums=[int(s[0]) for s in scenes]
embeds=re.findall(r'!\[\[(.*?)\]\]', text)
missing=[e for e in embeds if not (root/e).exists()]
pre11='\n'.join([s[4] for s in scenes if int(s[0])<11])
print('scene_count', len(scenes))
print('heading_sequence_ok', nums == list(range(1,39)))
print('embed_count', len(embeds))
print('missing_files', len(missing))
print('event_count', text.count('**事件：'))
print('story_label_count', text.count('**故事与因缘：**'))
print('meaning_label_count', text.count('**意义：**'))
print('traditional_terms', len(re.findall(r'传统|传说|佛传|通常被说成|据说|故事说|常说|被说成|图像常|相传', text)))
print('almost_highest_count', text.count('几乎最高'))
print('pre_scene11_old_sick_death_terms', len(re.findall(r'老、病、死|老病|老人|病人|死人|死亡|衰老|疾病', pre11)))
PY
```

Expected current output:

```text
scene_count 38
heading_sequence_ok True
embed_count 38
missing_files 0
event_count 0
story_label_count 0
meaning_label_count 0
traditional_terms 0
almost_highest_count 0
pre_scene11_old_sick_death_terms 0
```

## How To Continue Improving

Recommended next pass:

1. Read the Chinese note scene by scene.
2. For each scene, check:
   - Does it match the image content?
   - Is the timeline clean?
   - Does it sound like story, not lecture?
   - Does the final paragraph feel gentle rather than preachy?
   - Is the scene long enough to be useful for beginners?
3. Improve only a few scenes per pass, then validate.

Good next candidates:

- Scene 10: still may need a more elegant way to express "protected palace happiness before the Four Sights" without sounding like a preview.
- Scene 11: can be made very strong because it is the first direct confrontation with old age, sickness, death, and the renunciant.
- Scene 13-14: the silent farewell and great renunciation should be emotionally rich but not sentimental.
- Scene 16-19: the teacher sequence should be doctrinally accurate and respectful. Avoid making the teachers look wrong; Siddhartha learned deeply from them, then saw the limits.
- Scene 26: awakening can probably be expanded later if user wants more detail.
- Scene 31-32: Yasodharā and Rāhula are emotionally important and should be handled with tenderness and accuracy.
- Scene 36: Jīvaka treating the Buddha's foot should avoid making Buddha sound like an invulnerable god.

## Important User Preferences From This Thread

The user repeatedly emphasized:

- Do not rely only on filenames. Understand the image content.
- Sequence should be based on actual Buddha-life timeline and story logic.
- If the user guesses a scene, do not blindly follow the guess. Use best judgement and explain if needed.
- Keep uncertain scenes out until clarified.
- Image 24 was eventually identified as Devadatta injuring the Buddha's foot and Jīvaka treating it.
- Tall images in generated PDFs should use max width with description below, but do not regenerate PDF unless asked.
- The user prefers a natural storybook flow in Chinese.
- The user likes detailed stories for beginners, but does not like "讲道理" / old-sounding moralizing.
- The user is sensitive to doctrinal/timeline details and will correct them.
- When making changes to file structure or image naming, validate all embeds and counts.

## Earlier Workflow History

Earlier in this project:

- Original Buddha-life images were moved into the attachment folder.
- Several new AI-generated scenes were added to match the style:
  - learning from Ālāra Kālāma
  - leaving Ālāra Kālāma
  - learning from Uddaka Rāmaputta
  - leaving Uddaka Rāmaputta
  - Anāthapiṇḍika / Jetavana may have been discussed/generated earlier, but it is not currently in the final 38-scene Chinese list shown above. Do not assume it is included unless you inspect the attachment folder and note.
- Three user-provided images were incorporated:
  - palace pleasures lose their charm
  - five ascetics
  - wounded swan
- The English note exists as a reference, but the current work is on the Chinese note.

## Recommended Response Style In New Conversation

When continuing:

- Start with `Hi Eryu, Please be mindful :)`.
- Reply mainly in Chinese.
- Be warm and thoughtful.
- Challenge questionable requests gently, especially if timeline or doctrine seems off.
- End with `Namo Buddhaya 🙏` if operating under the Obsidian vault instructions.
- Give concise progress updates while editing.
- In final answer, include:
  - which file changed
  - what was improved
  - validation result
  - anything that still needs review

## Suggested First Message For New Codex

The user can paste something like this:

```text
Hi Codex, please continue improving this Buddha-life Chinese picture storybook.

Read this context first:
life-of-buddha-storybook/context/storybook-continuation-context.md

Then inspect the current Chinese note:
<original-obsidian-vault>/Dhamma/Blog/(2026-06-05) 佛陀的一生 - 图像故事书.md

Goal: keep improving the Chinese storybook scene by scene. Make it detailed and beginner-friendly, but not preachy. Keep it as flowing illustrated storytelling. Do not reintroduce separate “意义” sections. Preserve all image embeds and validate after edits.
```
