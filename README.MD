[**中文**](./README.md) | [**English**](./README_EN.md)

# Open-Chinese-LLaMA-7B-Patch

本项目为基于 [LLaMA](https://github.com/facebookresearch/llama)-7B 经过 **中文数据集二次预训练** 产生的 **中文大语言模型基座**。

本项目代码依赖于 [OpenLMLab/collie](https://github.com/OpenLMLab/collie)，请通过如下命令安装：

```bash

pip install git+https://github.com/OpenLMLab/collie.git

```

## 使用

由于 [LLaMA](https://github.com/facebookresearch/llama)-7B 未开源官方权重，本次发布的模型为 **补丁** 类型，需配合原始官方权重才可以使用。

您可以通过 `tools/patch_model.py` 来安装 **补丁**，例如：

```bash

python tools/patch_model.py --base_model <path_or_name_to_original_model>
                            --patch_model openlmlab/open-chinese-llama-7b-patch
                            --base_model_format <hf_or_raw>

```

**补丁** 安装为原地安装，即安装后的 `patch` 即为完整版 `hf` 格式的权重，您可以使用 `transformers` 加载模型。

## 通过命令行快速体验

经过 **patch** 的模型可以被 `transformers` 轻松加载。为了方便快速体验效果，我们提供了控制台的 Demo：

```bash

python cli_demo.py --model openlmlab/open-chinese-llama-7b-patch
                   --devices 0
                   --max_length 1024
                   --do_sample true
                   --top_k 40
                   --top_p 0.8
                   --temperature 0.7
                   --penalty 1.02

```

效果如图所示：

![Cli Demo](/pics/cli_demo.png "命令行 Demo")

## 下载地址

| 来源      | 地址 |
| ----------- | ----------- |
| 🤗Huggingface   | [openlmlab/open-chinese-llama-7b-patch](https://huggingface.co/openlmlab/open-chinese-llama-7b-patch)       |
| 百度网盘       | -        |
| Google Driver | -        |

## 模型格式转换

**Open-Chinese-LLaMA-7B-Patch** 中的 `patch_model.py` 工具尽可转换为 `transformers` 可加载的 **hf** 格式。为了方便，我们同时提供了官方版本模型（`raw`）到 `hf` 的转换工具：

提示，当转换成 `raw` 格式的模型时，需要指定张量并行的大小和对应设备，并且只能在拥有对应数量的显卡的机器上转换。

```bash

python convert_model.py --model_path <path_or_name_to_your_hf_or_raw_model>
                        --source_format hf
                        --target_format raw
                        --target_path <path_you_want_to_save_the_converted_model>
                        --raw_parallel_degree 2
                        --raw_parallel_devices 0,1

```
