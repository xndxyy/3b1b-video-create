# 深度学习可视化课程制作工具箱

将《深度学习入门：基于 Python 的理论与实现》的章节内容制作成中文讲解视频。项目提供从脚本、旁白、Manim 动画到 ffmpeg 合成的一套可复用模板，视觉语言参考数学可视化视频的暗色画布、几何推演和逐步揭示。

仓库只包含代码、文档和示例脚本；教材、生成音频、渲染视频及本地运行配置均不纳入版本控制。

## 项目内容

```text
.
├── assets/                 # 字体、音乐等本地素材的说明
├── docs/                   # 制作流程、视觉规范和命令参考
├── samples/                # 第二章的脚本与 Manim 场景示例
├── templates/              # 新章节可复制的旁白与合成模板
├── .env.example            # 运行配置示例
└── AGENTS.md               # 供 AI 编程助手读取的制作规范
```

## 依赖

| 用途 | 工具 |
| --- | --- |
| 数学动画 | [Manim Community](https://www.manim.community/) |
| 旁白生成 | [VoxCPM2](https://github.com/OpenBMB/VoxCPM) 与 CUDA GPU |
| 视频合成 | ffmpeg / ffprobe |
| 可选的时间轴对齐 | Whisper 或 faster-whisper |

建议使用 Python 3.10 或更高版本，并确保 `ffmpeg` 与 `ffprobe` 已加入 `PATH`。

## 快速开始

1. 克隆仓库并创建 Python 环境。
2. 安装 Manim、`python-dotenv`、`numpy`、`soundfile` 以及旁白模型所需依赖。
3. 将 `.env.example` 复制为 `.env`，按注释填写设备、教材和音频配置。示例中的文件位置均相对于仓库根目录。
4. 阅读 [制作流程](docs/workflow.md)，在 `chapters/` 下创建一个章节目录。
5. 参考 [第二章脚本](samples/ch02_perceptron_script.md) 和 [第二章场景](samples/ch02_perceptron_scenes.py)，完成脚本与动画。

```powershell
Copy-Item .env.example .env
pip install manim python-dotenv numpy soundfile
manim render -qm samples/ch02_perceptron_scenes.py S1_ColdOpen
```

VoxCPM2 的安装方式和显存要求以其上游仓库为准。若使用参考音频进行语音生成，请仅使用已获得使用许可的音频。

## 新建章节

```text
chapters/
└── ch03_neural_network/
    ├── script.md
    ├── gen_voice.py
    ├── scenes.py
    ├── assemble.py
    └── media/
```

将 `templates/gen_voice.py` 与 `templates/assemble.py` 复制到章节目录。旁白文本写入 `SEGMENTS`，每段控制在 280 个中文字符以内；将场景名和旁白段落索引写入 `SCENE_SEGMENTS`。详细步骤见 [制作流程](docs/workflow.md)。

## 制作顺序

1. 从教材提取章节的定义、公式、代码、图表和习题。
2. 写成连贯的中文旁白，并在段落间标注动画意图。
3. 按句意切分旁白，生成每段音频与完整旁白。
4. 使用 Manim 或网页动画实现每个讲解节拍。
5. 用 ffmpeg 按旁白时长校准片段并合成成片。
6. 使用 `ffprobe` 检查时长和音视频流，在场景交界处抽查同步。

## 文档索引

- [制作流程](docs/workflow.md)
- [视觉规范](docs/3b1b-style-guide.md)
- [旁白生成](docs/voice-cloning.md)
- [模板说明](templates/README.md)
- [ffmpeg 命令参考](docs/ffmpeg-cookbook.md)
- [脚本写作方法](docs/skill-recipes.md)

## 版本控制约定

`.env`、教材 PDF、参考音频、分段音频、渲染缓存与最终视频均已被 `.gitignore` 排除。提交前运行 `git status --ignored`，确认此类本地文件没有进入暂存区。

## 许可

本仓库采用 [MIT License](LICENSE)。教材原文及相关图像的著作权归原权利人所有；发布成片前请自行确认所使用的教材内容、字体、音乐和音频的授权范围。
