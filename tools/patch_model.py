import io
import os
import json
import tqdm
import torch
import argparse
from huggingface_hub import snapshot_download

from collie.models.llama_colossalai import load_state_dict, save_state_dict, ModelArgs

parser = argparse.ArgumentParser()
parser.add_argument("--base_model", type=str, default="decapoda-research/llama-7b-hf", help="Path or name to the base model to patch. (e.g. decapoda-research/llama-7b-hf)")
parser.add_argument("--base_model_format", type=str, default="hf", help="Format of the base model. (e.g. hf or raw)")
parser.add_argument("--patch_model", type=str, default="openlmlab/further-trained-llama-7b-patch", help="Path or name to the patch model to patch. (e.g. OpenLMLab/yangtuo)")
parser.add_argument("--offload", default=False, action="store_true", help="Whether to offload the base model to the disk. Enable this when meeting CPU RAM shortage.")
parser.add_argument("--offload_path", type=str, default="./offload/", help="Path to offload the base model. (e.g. ./offload/)")
args = parser.parse_known_args()[0]

def patch_model(base_model: str = args.base_model,
                base_model_format: str = args.base_model_format,
                patch_model: str = args.patch_model,
                offload: bool = args.offload,
                offload_path: str = args.offload_path):
    assert args.base_model_format in ["hf", "raw"], "base_model_format must be either hf or raw"
    model_args = ModelArgs()
    if not os.path.exists(base_model):
        base_model = snapshot_download(base_model)
    if not os.path.exists(patch_model):
        patch_model = snapshot_download(patch_model)
    base_state_dict = load_state_dict(protocol="file",
                                      format=base_model_format,
                                      file_folder=base_model,
                                      model_args=model_args)
    buffers = save_state_dict(base_state_dict, 
                              protocol="file",
                              format="hf",
                              file_folder=offload_path,
                              save_to_buffer=not offload,
                              model_args=model_args)
    del base_state_dict
    weights = [weight for weight in list(os.listdir(patch_model)) if weight.endswith(".bin")]
    if not os.path.exists(os.path.join(patch_model, "patch_history.json")):
        # patch_history = {key: False for key in weights}
        # with open(os.path.join(patch_model, "patch_history.json"), mode="w+") as file:
        #     file.write(json.dumps(patch_history, indent=4))
        raise ValueError("patch_history.json not found. Not a normal patch model.")
    else:
        with open(os.path.join(patch_model, "patch_history.json"), mode="r") as file:
            patch_history = json.loads(file.read())
    with tqdm.tqdm(desc=f"Patching state dict", total=len(weights)) as pbar:
        for weight in weights:
            if patch_history[weight]:
                continue
            patch_state_dict = torch.load(os.path.join(patch_model, weight), map_location="cpu")
            if buffers:
                base_state_dict = torch.load(io.BytesIO(buffers[os.path.join(offload_path, weight)]), map_location="cpu")
            else:
                base_state_dict = torch.load(os.path.join(offload_path, weight), map_location="cpu")
            for key in list(patch_state_dict.keys()):
                if not key.endswith("inv_freq"):
                    patch_state_dict[key] = patch_state_dict[key] + base_state_dict[key]
            with open(os.path.join(patch_model, weight), mode="wb+") as file:
                torch.save(patch_state_dict, file)
            del patch_state_dict
            patch_history[weight] = True
            with open(os.path.join(patch_model, "patch_history.json"), mode="w+") as file:
                file.write(json.dumps(patch_history, indent=4))
            pbar.update(1)
    finish()
    
def finish():
    print("Congratulations! You have successfully installed the model patch.")
    print("You can then load the model as follows.")
    print(">>> from transformers import LlamaForCausalLM")
    print(f'>>> model = LlamaForCausalLM.from_pretrained("{args.patch_model}")')
    
if __name__ == "__main__":
    patch_model()