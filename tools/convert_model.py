import sys
sys.path.append("/mnt/lustre/zhangshuo/projects/collie/")

import argparse

from collie.models.llama_colossalai import load_state_dict, ModelArgs, save_state_dict

parser = argparse.ArgumentParser()
parser.add_argument("--model_path", type=str, default="decapoda-research/llama-7b-hf", help="Path or name to the model to convert. (e.g. decapoda-research/llama-7b-hf)")
parser.add_argument("--source_format", type=str, default="hf", help="Format of the source model. (e.g. `hf` or `raw`)")
parser.add_argument("--target_format", type=str, default="raw", help="Format of the target model. (e.g. `hf` or `raw`)")
parser.add_argument("--target_path", type=str, default="./converted_model", help="Path to save the converted model. (e.g. `./converted_model`)")
parser.add_argument("--raw_parallel_degree", type=int, default=2, help="Parallel degree of the raw format model. (e.g. 1)")
parser.add_argument("--raw_parallel_devices", type=str, default='0,1', help="Parallel devices of the raw format model. (e.g. `0,1`)")
args = parser.parse_known_args()[0]

def convert_model(model_path: str = args.model_path,
                  source_format: str = args.source_format,
                  target_format: str = args.target_format,
                  target_path: str = args.target_path,
                  raw_parallel_degree: int = args.raw_parallel_degree,
                  raw_parallel_devices: str = args.raw_parallel_devices):
    assert args.source_format in ["hf", "raw"], "source_format must be either hf or raw"
    assert args.target_format in ["hf", "raw"], "target_format must be either hf or raw"
    assert args.source_format != args.target_format, "source_format and target_format must be different"
    model_args = ModelArgs()
    state_dict = load_state_dict(
        protocol="file",
        format=source_format,
        file_folder=model_path,
        model_args=model_args
    )
    assert len(raw_parallel_devices.split(",")) == raw_parallel_degree, "raw_parallel_devices must be the same length as raw_parallel_degree"
    raw_tp_device_map = {i: int(raw_parallel_devices.split(",")[i]) for i in range(raw_parallel_degree)}
    save_state_dict(
        state_dict, 
        protocol="file",
        format=target_format,
        file_folder=target_path,
        save_to_buffer=False,
        model_args=model_args,
        raw_tp_size=raw_parallel_degree,
        raw_tp_device_map=raw_tp_device_map
    )
    
if __name__ == "__main__":
    convert_model()