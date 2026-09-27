import torch

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig,
)

from peft import (
    LoraConfig,
    get_peft_model,
    prepare_model_for_kbit_training,
)


MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"


print("=" * 60)
print("LoRA SETUP TEST")
print("=" * 60)


# GPU
if not torch.cuda.is_available():
    raise RuntimeError("CUDA GPU is not available.")

print("GPU:", torch.cuda.get_device_name(0))


# Tokenizer
print()
print("Loading tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME,
    local_files_only=True,
)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

print("Tokenizer loaded.")


# 4-bit configuration
print()
print("Configuring 4-bit NF4...")

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
)

print("4-bit configuration ready.")


# Model
print()
print("Loading Qwen model...")

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    quantization_config=bnb_config,
    device_map="auto",
    local_files_only=True,
)

print("Model loaded successfully.")


# Prepare model
print()
print("Preparing model for k-bit training...")

model = prepare_model_for_kbit_training(model)

model.config.use_cache = False

print("Model prepared.")


# LoRA
print()
print("Applying LoRA...")

lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
    target_modules=[
        "q_proj",
        "k_proj",
        "v_proj",
        "o_proj",
    ],
)

model = get_peft_model(model, lora_config)

print("LoRA applied successfully.")


# Parameters
print()
print("=" * 60)
print("TRAINABLE PARAMETERS")
print("=" * 60)

model.print_trainable_parameters()


# GPU memory
allocated = torch.cuda.memory_allocated() / 1024**3
reserved = torch.cuda.memory_reserved() / 1024**3

print()
print("=" * 60)
print("GPU MEMORY")
print("=" * 60)

print(f"Allocated: {allocated:.2f} GB")
print(f"Reserved:  {reserved:.2f} GB")


print()
print("=" * 60)
print("LoRA SETUP TEST PASSED")
print("=" * 60)