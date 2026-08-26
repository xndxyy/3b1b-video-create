# 模板使用说明

每个章节目录保存自己的脚本、动画和生成媒体。开始新章节时，将本目录的 `gen_voice.py` 和 `assemble.py` 复制过去，再按章节内容修改配置区。

| 文件 | 修改位置 | 作用 |
| --- | --- | --- |
| `gen_voice.py` | `SEGMENTS` | 生成分段 WAV 和完整旁白 WAV |
| `assemble.py` | `SCENE_SEGMENTS` | 将场景时长校准到对应旁白并合成视频 |

推荐目录结构：

```text
chapters/chNN_topic/
├── script.md
├── gen_voice.py
├── scenes.py
├── assemble.py
├── seg_00.wav             # 自动生成，已忽略
├── voiceover.wav          # 自动生成，已忽略
└── media/                 # Manim 渲染结果，已忽略
```

在仓库根目录执行命令时，模板会把输出写入其所在的章节目录：

```powershell
python chapters/chNN_topic/gen_voice.py
manim render -qm --media_dir chapters/chNN_topic/media chapters/chNN_topic/scenes.py SceneName
python chapters/chNN_topic/assemble.py
```

旁白段落请按语义切分，每段不得超过 280 个中文字符。场景类名必须与 `SCENE_SEGMENTS` 的键一致；渲染文件默认位于该章节的 `media/videos/scenes/1080p30/`。
