[**中文**](./README.md) | [**English**](./README_EN.md)

# Open-Chinese-LLaMA-7B-Patch

This project is a **Chinese large language model base** generated from the [LLaMA](https://github.com/facebookresearch/llama)-7B model after **secondary pre-training** on Chinese datasets.

This project's code depends on [OpenLMLab/collie](https://github.com/OpenLMLab/collie). Please install it using the following command:

```bash

pip install git+https://github.com/OpenLMLab/collie.git

```

## Download Links

| Source      | Link         |
| ----------- | -----------  |
| 🤗Huggingface             | [openlmlab/open-chinese-llama-7b-patch](https://huggingface.co/openlmlab/open-chinese-llama-7b-patch)       |
| Baidu Cloud Disk          | [Extraction code gk34](https://pan.baidu.com/s/14E7iZKcH-5SHMDu97k70cg?pwd=gk34) |
| Google Driver             | [further-train-7B](https://drive.google.com/drive/folders/1THvuFzq_wojVfMLYV1qsSE_ddSjG0Ypv?usp=sharing)        |
| SHA256 Verification File  | [SHA256.txt](./SHA256.txt) |

## Evaluation

See [Benchmark.md](./benchmark/Benchmark.md)。

## Usage

Since the official weights for [LLaMA](https://github.com/facebookresearch/llama)-7B have not been open-sourced, the model released this time is of the **patch** type, which needs to be used in combination with the original official weights.

You can install the **patch** using `tools/patch_model.py`, for example:

```bash

python tools/patch_model.py --base_model <path_or_name_to_original_model>
                            --patch_model openlmlab/open-chinese-llama-7b-patch
                            --base_model_format <hf_or_raw>

```

The **patch** is installed in place, which means that the installed **patch** is the complete `hf` format weight. You can use `transformers` to load the model.

## Quick Experience via Command Line

The **patched** model can be easily loaded by `transformers`. For a quick experience, we provide a console Demo:

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

The result is shown in the image below:

![Cli Demo](/pics/cli_demo.png "命令行 Demo")

## Model Format Conversion

The `patch_model.py` tool in **Open-Chinese-LLaMA-7B-Patch** generates this model in the **hf** format, which can be loaded by `transformers`. For convenience, we also provide a conversion tool between the official version model (**raw**) and **hf**:

Note that when converting to the **raw** format model, you need to specify the tensor parallel size and corresponding devices, and the conversion can only be performed on a machine with the corresponding number of graphics cards.

```bash

python convert_model.py --model_path <path_or_name_to_your_hf_or_raw_model>
                        --source_format hf
                        --target_format raw
                        --target_path <path_you_want_to_save_the_converted_model>
                        --raw_parallel_degree 2
                        --raw_parallel_devices 0,1

```
