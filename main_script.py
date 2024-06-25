# .\main_script.py - the main script.

import os
from scripts.utility_script import (
    load_config, check_model_paths, load_models, unload_models, VulkanModel, run_llama_cli
)

def main():
    config_path = './data/config_general.json'
    if not os.path.exists(config_path):
        print("Configuration file not found. Please run main_config.py first.")
        return

    config = load_config(config_path)
    chat_model = config.get("chat_model_used")
    instruct_model = config.get("instruct_model_used")
    code_model = config.get("code_model_used")
    max_memory_usage = config.get("maximum_memory_usage")

    if not check_model_paths([chat_model, instruct_model, code_model]):
        print("Check Modelfile Locations Are Correct!")
        return

    models = load_models(chat_model, instruct_model, code_model)
    print("Models Loaded To System RAM.")

    vulkan_model_instance = VulkanModel(model_path=chat_model)

    if not vulkan_model_instance.load_model_to_gpu():
        print("Failed to load chat model to GPU.")
        return

    print("Chat Model Loaded On GPU.")

    response = run_llama_cli(
        "./libraries/llama-bin-win-vulkan-x64/llama-cli.exe", chat_model, max_memory_usage=max_memory_usage, use_gpu=True
    )
    if response:
        print(response)
    else:
        print("Failed to get response from the model.")

    unload_models(models)

    vulkan_model_instance.unload_model_from_gpu()

if __name__ == "__main__":
    main()