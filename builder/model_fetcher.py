'''
RunPod | serverless-ckpt-template | model_fetcher.py

Downloads the model from the URL passed in.
'''

import datetime
import shutil
import requests
import argparse
import torch

from pathlib import Path
from urllib.parse import urlparse

from diffusers import StableDiffusionPipeline
from diffusers.pipelines.stable_diffusion.safety_checker import (
    StableDiffusionSafetyChecker,
)

SAFETY_MODEL_ID = "CompVis/stable-diffusion-safety-checker"
MODEL_CACHE_DIR = "diffusers-cache"
MODEL_DIR = "epicrealism_naturalSinRC1VAE"


def download_model(model_url: str):
    '''
    Downloads the model from the URL passed in.
    '''
    model_cache_path = Path(MODEL_CACHE_DIR)
    # if model_cache_path.exists():
    #     shutil.rmtree(model_cache_path)
    # model_cache_path.mkdir(parents=True, exist_ok=True)

    # # Check if the URL is from huggingface.co, if so, grab the model repo id.
    # parsed_url = urlparse(model_url)
    # if parsed_url.netloc == "huggingface.co":
    #     model_id = f"{parsed_url.path.strip('/')}"
    # else:
    #     downloaded_model = requests.get(model_url, stream=True, timeout=600)
    #     model_id = "./" + MODEL_CACHE_DIR + '/model.safetensors'
    #     with open(model_cache_path / "model.safetensors", "wb") as f:
    #         for chunk in downloaded_model.iter_content(chunk_size=1024):
    #             if chunk:
    #                 f.write(chunk)

    StableDiffusionSafetyChecker.from_pretrained(
        SAFETY_MODEL_ID,
        cache_dir=model_cache_path,
    )

    # 40s
    # print(datetime.datetime.now())
    StableDiffusionPipeline.from_pretrained(
        MODEL_DIR,
        local_files_only=True,
        use_safetensors=True,
        torch_dtype=torch.float16
    )
    # print(datetime.datetime.now())

    # WARNING: cost 1 minute, slow implementation
    # print(datetime.datetime.now())
    # StableDiffusionPipeline.from_single_file(
    #     model_path,
    #     cache_dir=model_cache_path,
    #     use_safetensors=True,
    #     torch_dtype=torch.float16
    # )
    # print(datetime.datetime.now())


    # StableDiffusionPipeline.from_pretrained(
    #     model_id,
    #     cache_dir=model_cache_path,
    #     use_safetensors=True,
    # )


# ---------------------------------------------------------------------------- #
#                                Parse Arguments                               #
# ---------------------------------------------------------------------------- #
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    "--model_url", type=str,
    default="https://huggingface.co/stabilityai/stable-diffusion-2-1",
    help="URL of the model to download."
)

if __name__ == "__main__":
    args = parser.parse_args()
    download_model(args.model_url)
    # download_model("https://civitai-delivery-worker-prod-2023-10-01.5ac0637cfd0766c97916cefa3764fbdf.r2.cloudflarestorage.com/81744/model/epicrealism.XNId.safetensors?X-Amz-Expires=86400&response-content-disposition=attachment%3B%20filename%3D%22epicrealism_naturalSinRC1VAE.safetensors%22&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=2fea663d76bd24a496545da373d610fc/20231021/us-east-1/s3/aws4_request&X-Amz-Date=20231021T215043Z&X-Amz-SignedHeaders=host&X-Amz-Signature=413d0ffba8fc459f57f37dba57229cd65f291d2aa5f64d0b9c69afd63890e5df")
