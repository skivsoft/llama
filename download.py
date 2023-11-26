import os
import subprocess


def mkdir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


def download_file(route, filename):
    url = presigned_url.replace("*", route)
    try:
        subprocess.run(["wget", "--continue", "-O", filename, url], check=True)
        print(f"File downloaded successfully: {filename}")
    except subprocess.CalledProcessError as e:
        print("An error occured:", e)


def check_md5(filepath):
    folder, filename = os.path.split(filepath)
    os.chdir(folder)
    try:
        subprocess.run(["md5sum", "-c", filename], check=True)
    except subprocess.CalledProcessError as e:
        print("An error occured:", e)


presigned_url = input("Enter the URL from email: ")
model_size = input("Enter the list of models to download without spaces (7B,13B,70B,7B-chat,13B-chat,70B-chat), or press Enter for all: ")

target_folder = "/Users/skiv/LLM/meta_models"
mkdir(target_folder)

if not model_size:
    model_size = "7B,13B,70B,7B-chat,13B-chat,70B-chat"

print("Downloading LICENSE and Acceptable Usage Policy")
download_file("LICENSE", f"{target_folder}/LICENSE")
download_file("USE_POLICY.md", f"{target_folder}/USE_POLICY.md")

print("Downloading tokenizer")
download_file("tokenizer.model", f"{target_folder}/tokenizer.model")
download_file("tokenizer_checklist.chk", f"{target_folder}/tokenizer_checklist.chk")
check_md5(f"{target_folder}/tokenizer_checklist.chk")

for m in model_size.split(","):
    if m == "7B":
        SHARD = 0
        MODEL_PATH = "llama-2-7b"
    elif m == "7B-chat":
        SHARD = 0
        MODEL_PATH = "llama-2-7b-chat"
    elif m == "13B":
        SHARD = 1
        MODEL_PATH = "llama-2-13b"
    elif m == "13B-chat":
        SHARD = 1
        MODEL_PATH = "llama-2-13b-chat"
    elif m == "70B":
        SHARD = 7
        MODEL_PATH = "llama-2-70b"
    elif m == "70B-chat":
        SHARD = 7
        MODEL_PATH = "llama-2-70b-chat"

    print(f"Downloading {MODEL_PATH}")
    mkdir(f"{target_folder}/{MODEL_PATH}")

    for i in range(SHARD + 1):
        s = f"{i:02d}"
        download_file(f"{MODEL_PATH}/consolidated.{s}.pth", f"{target_folder}/{MODEL_PATH}/consolidated.{s}.pth")

    download_file(f"{MODEL_PATH}/params.json", f"{target_folder}/{MODEL_PATH}/params.json")
    download_file(f"{MODEL_PATH}/checklist.chk", f"{target_folder}/{MODEL_PATH}/checklist.chk")

    print("Checking checksums")
    check_md5(f"{target_folder}/{MODEL_PATH}/checklist.chk")

