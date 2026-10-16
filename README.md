# 深度学习可视化课程制作工具箱

把《深度学习入门：基于 Python 的理论与实现》的章节内容，逐步制作成中文讲解视频：**脚本 → 分段旁白 → Manim 数学动画 → ffmpeg 合成 → 人工验收**。

仓库提供可复用的制作模板、规范和第二章感知机示例，适合教师、课程作者和 AI 辅助制作流程。视觉参考 3Blue1Brown 的暗色画布、几何推演和逐步揭示；这不代表 3Blue1Brown 官方项目或授权背书。

**当前是需要人工改写与联调的工具箱，不是一键生成整本教材课程的产品。** 仓库不包含教材 PDF、参考音频、字体、背景音乐、模型权重或成品视频。

## 能做什么

| 环节 | 仓库内容 | 仍需你完成 |
| --- | --- | --- |
| 讲稿与镜头 | 感知机旁白、12 个 Manim 场景类、脚本写作方法 | 知识点取舍、数学/史实核对、章节脚本与镜头设计 |
| 旁白 | VoxCPM2 生成模板，逐段保存 WAV，合并完整旁白并打印时长 | 提供有授权的参考 WAV、安装模型环境、填写 `SEGMENTS` |
| 数学动画 | Manim Community 场景示例、配色与构图规范 | 适配本机字体、制作新场景、逐镜头渲染 |
| 合成 | 场景与音频段落映射、短片段停帧补齐、长片段裁切、拼接与混音 | 配置 `SCENE_SEGMENTS`、核对媒体路径与成片同步 |
| 验收 | 工作流程、ffmpeg / ffprobe 参考 | 逐场景检查公式、旁白、停帧、画面和授权 |

**不是已实现能力：** 自动读取整本 PDF、自动生成完整章节、自动事实核查、自动字幕/Whisper 对齐、网页动画渲染集成。文档提及的 HyperFrames 等属于可选扩展，当前没有相应工程实现。

## 环境与依赖

| 用途 | 依赖或外部工具 |
| --- | --- |
| Python 脚本 | 建议 Python 3.10+；NumPy、soundfile、python-dotenv |
| 数学动画 | Manim Community 及其本机系统依赖 |
| 旁白生成 | 可导入的 `voxcpm` 包、`openbmb/VoxCPM2` 模型及兼容运行环境 |
| 媒体合成 | 可从命令行调用的 `ffmpeg`、`ffprobe` |
| 字体 | 示例使用 `Microsoft YaHei` 与 `Consolas`；缺少时需改为已安装且有授权的字体 |

仓库没有锁定的 `requirements.txt`、环境文件或自动安装脚本；需要分别准备动画、语音模型与系统媒体工具。VoxCPM2 模板默认 `DEVICE=cuda`，文档也允许尝试 `cpu`，但本仓库不承诺固定显存、速度或跨设备效果。

## 快速开始：先渲染一个场景

以下为 Windows PowerShell 示例，所有命令从仓库根目录运行。**这一步不需要教材 PDF、参考音频或 TTS 模型。**

~~~powershell
git clone https://github.com/xndxyy/3b1b-video-create.git
cd 3b1b-video-create

python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install manim python-dotenv numpy soundfile

ffmpeg -version
ffprobe -version
manim render -qm samples/ch02_perceptron_scenes.py S1_ColdOpen
~~~

前两条媒体工具命令用于确认外部程序已加入 `PATH`，不负责安装它们。渲染前检查示例中的字体名称；安装 Python 包本身不保证字体和系统依赖齐备。

这一命令只渲染一个示例场景，**不会生成旁白或完整课程成片**。示例源码设置 1920×1080、30 fps；具体输出位置以 Manim 当次日志为准。仓库未附本轮新生成的截图、视频或渲染测试结果。

## 新建章节：从最小片段到完整章节

### 1. 建立章节工作区

~~~powershell
New-Item -ItemType Directory -Force chapters/ch03_neural_network
Copy-Item templates/gen_voice.py chapters/ch03_neural_network/gen_voice.py
Copy-Item templates/assemble.py chapters/ch03_neural_network/assemble.py
Copy-Item samples/ch02_perceptron_scenes.py chapters/ch03_neural_network/scenes.py
Copy-Item .env.example .env
~~~

这里复制感知机场景只是建立起点，**不会自动变成第三章内容**。先阅读 [制作规范](AGENTS.md)与[完整流程](docs/workflow.md)，写自己的 `script.md`，再按本章改写动画。

~~~text
chapters/ch03_neural_network/
├── script.md          自行编写的讲稿与动画提示
├── gen_voice.py       填写本章 SEGMENTS
├── scenes.py          编写本章场景
├── assemble.py        填写 SCENE_SEGMENTS
├── seg_00.wav         本地生成，不提交
├── voiceover.wav      本地生成，不提交
└── media/             本地渲染，不提交
~~~

### 2. 准备授权输入与旁白环境

编辑 `.env`，示例字段与当前模板一致：

~~~dotenv
DEVICE=cuda
VOXCPM_PATH=
REFERENCE_AUDIO=assets/voices/narrator.wav
TEXTBOOK_PDF=sources/deep-learning-from-scratch.pdf
FFMPEG=ffmpeg
FFPROBE=ffprobe
~~~

- `REFERENCE_AUDIO` 必须指向你有权用于声音生成的本地 WAV。
- `VOXCPM_PATH` 只用于从本地源码目录导入模型包；当前环境已安装时留空。
- `TEXTBOOK_PDF` 是本地素材位置约定，当前脚本**不会自动读取或提取该 PDF**。
- 相对输入路径按命令所在目录解析，因此推荐一直从仓库根目录执行。
- 需另行安装模型及其依赖，并确认 `voxcpm` 能在运行 `gen_voice.py` 的同一环境导入。详见[旁白说明](docs/voice-cloning.md)。

### 3. 对齐旁白与场景配置

在 `gen_voice.py` 中替换 `SEGMENTS`，每项**严格少于 280 个中文字符**，按完整句意切分。脚本负责生成，不会自动替你检查这个长度约束。

在 `assemble.py` 中改写 `SCENE_SEGMENTS`，键必须是实际渲染的场景类名，值为从 0 开始的旁白段落索引。先做一个场景时，可以只保留：

~~~python
SCENE_SEGMENTS = {
    "S1_ColdOpen": [0, 1, 2, 3],
}
~~~

上述示例要求 `SEGMENTS` 恰有与该片段对应的四段旁白。不要直接混用未修改的两个模板：语音模板仅有四段示例文本，而合成模板默认映射引用到了第 20 段，二者**不是开箱配套的完整章节**。

扩展为完整章节后，应按实际讲述顺序覆盖所有旁白段落，避免遗漏、重复或倒序。样例讲稿只是写作参考，仍需根据制作规范补足内容与字数，并做数学与史实复核。

### 4. 生成、渲染与合成

先在已配置好的语音环境生成音频，再渲染每个映射场景：

~~~powershell
python chapters/ch03_neural_network/gen_voice.py
manim render -qm --media_dir chapters/ch03_neural_network/media chapters/ch03_neural_network/scenes.py S1_ColdOpen
~~~

`gen_voice.py` 将 `seg_NN.wav` 与 `voiceover.wav` 写入脚本所在章节目录，并打印累计时长。完整章节需要逐一渲染 `SCENE_SEGMENTS` 中所有场景，不能只渲染开场。

合成模板默认在章节目录下寻找 `media/videos/scenes/1080p30/<SceneName>.mp4`。**检查实际渲染目录后再合成**；若分辨率、文件名或输出路径不同，调整 `MEDIA_DIR`（相对于章节目录）以指向真实片段。

~~~powershell
python chapters/ch03_neural_network/assemble.py
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 chapters/ch03_neural_network/chapter_3b1b.mp4
~~~

模板默认输出 `chapter_3b1b.mp4`，可通过 `FINAL_NAME` 修改。`ffprobe` 时长检查不是内容验收；还应逐场景查看画面、公式、字幕与旁白同步。

## 合成器的重要边界

- 找不到动画时会生成暗色空白片段，而不是证明视频制作已完成。交付前必须排查所有 `MISSING animation`。
- 找不到分段音频时会按 0 秒处理；部分外部命令失败只打印错误，并非所有失败都会立即终止。
- 合成采用停帧/裁切对齐时长，不会自动修复讲解节奏、错误口播或镜头设计。
- 模板会使用并清理章节目录下特定命名的临时文件，保留 `_clip_*.mp4`、`_blank_*.mp4`、`_video_only.mp4` 作为中间产物命名，不要存放唯一原始素材。
- 示例没有配套完整旁白、时间轴或成片，固定停留时间需要根据你实际生成的音频重新调整。

## 文档导航

- [章节制作流程](docs/workflow.md)：从教材拆解到人工验收。
- [模板说明](templates/README.md)：章节目录与可编辑配置区。
- [视觉规范](docs/3b1b-style-guide.md)：配色、构图与动画原则。
- [旁白生成](docs/voice-cloning.md)：参考音频、分段和设备配置。
- [ffmpeg 参考](docs/ffmpeg-cookbook.md)：停帧、裁切、拼接与混音。
- [脚本写作方法](docs/skill-recipes.md)：人工与 AI 辅助写作流程。
- [第二章讲稿](samples/ch02_perceptron_script.md) / [第二章场景](samples/ch02_perceptron_scenes.py)：可读示例，不是经审定的完整课程交付物。
- [本地素材约定](assets/README.md)：字体、声音和音乐目录。

## 版本控制、授权与许可

`.gitignore` 排除 `.env`、PDF、WAV、视频和 Manim 缓存，但忽略规则**不代替授权检查**。字体文件、音乐和其他素材也应逐项确认，不能假定放入 `assets/` 就一定会被忽略。提交前检查 `git status --ignored` 与暂存区，避免上传私有输入和未经许可的素材。

本仓库代码与文档采用 [MIT License](LICENSE)。教材原文和图像、第三方字体、音乐、声音、模型及生成媒体各有独立权利与使用条件；MIT 不授予这些素材的使用许可。仅使用本人或已取得适当授权的参考声音，发布课程前确认教材引用和全部素材的授权范围。

