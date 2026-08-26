# 旁白生成：VoxCPM2

VoxCPM2 可根据文本和参考 WAV 生成旁白。本项目的模板负责逐段生成、保存音频并输出时长，供后续动画定时与视频合成使用。

## 前置条件

- 已安装可导入的 `voxcpm` 包，或在 `.env` 中设置 `VOXCPM_PATH` 指向本地源码目录。
- CUDA 环境可用时设置 `DEVICE=cuda` 或 `cuda:0`；没有 GPU 时可尝试 `cpu`，速度会明显下降。
- `.env` 中的 `REFERENCE_AUDIO` 指向本地 WAV 文件。
- 仅将有权使用的音频用作参考素材。

## 配置

```dotenv
DEVICE=cuda
VOXCPM_PATH=
REFERENCE_AUDIO=assets/voices/narrator.wav
```

当 VoxCPM2 已安装在当前 Python 环境时，`VOXCPM_PATH` 保持为空。相对路径以运行命令时所在目录解析，因此推荐从仓库根目录执行章节脚本。

## 生成规则

- 每个 `SEGMENTS` 元素少于 280 个中文字符。
- 在句号、逗号或完整短语后分段，避免破坏韵律。
- 默认 `cfg_value=2.5`、`inference_timesteps=15`，可基于质量与速度需求调整。
- 保留分段数组后一次性合并为 `voiceover.wav`，避免反复编解码引入噪声。

## 运行

```powershell
python chapters/chNN_topic/gen_voice.py
```

输出包括 `seg_NN.wav`、`voiceover.wav` 和终端中的累计时间表。时间表可用于检查动画镜头是否与旁白段落对应。

## 常见问题

单段过长会显著增加显存占用，遇到显存不足时先缩短单段，再降低并发和推理步数。导入错误通常说明环境未激活或 `VOXCPM_PATH` 设置不正确；先在同一环境执行 `python -c "from voxcpm import VoxCPM"` 验证。
