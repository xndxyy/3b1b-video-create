# 章节制作流程

以下流程适用于每个章节。目标是让文字、旁白和动画围绕同一组概念推进，而不是把现成讲义逐页搬到视频里。

## 1. 准备环境

在仓库根目录创建 `.env`：

```powershell
Copy-Item .env.example .env
```

安装 Manim、ffmpeg 和旁白生成所需依赖。教材 PDF、参考音频和生成媒体均保留在本地；其位置由 `.env` 管理，默认采用相对路径。

## 2. 拆解教材

逐节记录定义、公式推导、Python 实现、图表和练习。为每项内容补充三个问题：观众已有的前置知识是什么，最容易产生的误解是什么，最适合用什么画面说明。先完成内容清单，再确定删减与强调的边界。

## 3. 编写旁白

从一个具体问题或现象进入主题，按概念之间的因果关系组织段落。正文使用完整的散文段落，不使用提纲式列表。每段同时记录简短的动画提示，例如公式变形、点集移动或代码执行轨迹。

章节脚本应覆盖本章所有小节、公式、实现和练习。交付前检查术语一致性、推导前提和数值示例；不要只给结论而省略中间步骤。

## 4. 切分与生成旁白

将脚本按自然停顿切成 `SEGMENTS`。每段小于 280 个中文字符，避免在公式、专有名词和句子中间切断。将 `templates/gen_voice.py` 复制到章节目录，填入文本后从仓库根目录运行：

```powershell
python chapters/chNN_topic/gen_voice.py
```

脚本会在同一章节目录生成 `seg_00.wav`、`seg_01.wav` 等分段文件和 `voiceover.wav`，并打印累计时长。参考音频由 `.env` 的 `REFERENCE_AUDIO` 指定。

## 5. 制作动画

优先用画面表达数学关系：让权重改变直线，让坐标点映射到真值表，让网络结构随变量增长。一个镜头只解决一个问题，关键结论出现后至少停留半秒。

Manim 场景类名应和合成配置一致。示例命令：

```powershell
manim render -qm --media_dir chapters/chNN_topic/media chapters/chNN_topic/scenes.py S1_ColdOpen
```

渲染前检查字体可用性，并遵循 [视觉规范](3b1b-style-guide.md)：深色背景、克制配色、动画服务于推理。

## 6. 合成成片

在 `assemble.py` 的 `SCENE_SEGMENTS` 中建立场景到旁白段落索引的映射。例如 `"S1_ColdOpen": [0, 1]` 表示该场景对应前两段旁白。然后运行：

```powershell
python chapters/chNN_topic/assemble.py
```

合成器会读取音频时长，将较短的视频片段停帧补齐，将较长片段裁到目标时长，再拼接视频并混入完整旁白。命令细节见 [ffmpeg 参考](ffmpeg-cookbook.md)。

## 7. 验收

```powershell
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 chapters/chNN_topic/chapter_3b1b.mp4
```

至少抽查开头、中段和结尾，并逐一检查场景边界的口型、停帧、字幕和公式显示。确认 `.env`、PDF、音频、`media/` 和最终视频未进入 Git 暂存区后再提交。
