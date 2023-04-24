[**中文**](./README.md) | [**English**](./README_EN.md)

# Open-Chinese-LLaMA-7B-Patch

本项目为基于 [LLaMA](https://github.com/facebookresearch/llama)-7B 经过 **中文数据集二次预训练** 产生的 **中文大语言模型基座**。

## 使用

由于 [LLaMA](https://github.com/facebookresearch/llama)-7B 未开源官方权重，本次发布的模型为 **补丁** 类型，需配合原始官方权重才可以使用。

您可以通过 `tools/patch_model.py` 来安装 **补丁**，例如：

```bash

python tools/patch_model.py --base_model <path_or_name_to_original_model>
                            --patch_model openlmlab/open-chinese-llama-7b-patch
                            --base_model_format <hf_or_raw>

```

**补丁** 安装为原地安装，即安装后的 `patch` 即为完整版 `hf` 格式的权重，您可以使用 `transformers` 加载模型。

## 下载地址

| 来源      | 地址 |
| ----------- | ----------- |
| 🤗Huggingface   | [openlmlab/open-chinese-llama-7b-patch](https://huggingface.co/openlmlab/open-chinese-llama-7b-patch)       |
| 百度网盘       | Text        |
| Google Driver | Text        |

