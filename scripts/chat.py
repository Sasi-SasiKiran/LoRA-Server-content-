import torch

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig,
)

from peft import PeftModel


# ============================================================
# CONFIGURATION
# ============================================================

BASE_MODEL = "Qwen/Qwen2.5-1.5B-Instruct"

ADAPTER_PATH = "outputs/cloud-operations-lora"


# ============================================================
# GPU CHECK
# ============================================================

if not torch.cuda.is_available():
    raise RuntimeError("CUDA GPU is not available.")

print("=" * 60)
print("CLOUD OPERATIONS AI")
print("=" * 60)

print("GPU:", torch.cuda.get_device_name(0))


# ============================================================
# TOKENIZER
# ============================================================

print()
print("Loading tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(
    ADAPTER_PATH,
    local_files_only=True,
)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token


# ============================================================
# 4-BIT CONFIGURATION
# ============================================================

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
)


# ============================================================
# LOAD BASE MODEL
# ============================================================

print("Loading Qwen model...")

base_model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    quantization_config=bnb_config,
    device_map="auto",
    local_files_only=True,
)

base_model.config.use_cache = True


# ============================================================
# LOAD LoRA
# ============================================================

print("Loading LoRA adapter...")

model = PeftModel.from_pretrained(
    base_model,
    ADAPTER_PATH,
)

model.eval()

print()
print("Model loaded successfully.")
print("Type 'exit' to stop.")
print("=" * 60)


# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are a Cloud and Server Operations Specialist.

Analyze infrastructure incidents using evidence, metrics, logs,
events and configuration.

Do not invent live system information.

Do not guess when evidence is insufficient.

Clearly separate:

INCIDENT
OBSERVED
EVIDENCE / EVIDENCE NEEDED
POSSIBLE CAUSES
NEEDS VERIFICATION
LIKELY CAUSE
CONFIDENCE
RECOMMENDED ACTION

When current system information is unavailable, explicitly state
what evidence should be collected.
"""


# ============================================================
# CHAT LOOP
# ============================================================

while True:

    print()

    user_input = input("You: ").strip()

    if not user_input:
        continue

    if user_input.lower() in ["exit", "quit"]:
        print("Exiting...")
        break

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": user_input,
        },
    ]

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
    )

    inputs = {
        key: value.to(model.device)
        for key, value in inputs.items()
    }

    with torch.no_grad():

        outputs = model.generate(
            **inputs,

            max_new_tokens=350,

            do_sample=True,

            temperature=0.3,

            top_p=0.9,

            pad_token_id=tokenizer.pad_token_id,

            eos_token_id=tokenizer.eos_token_id,
        )

    generated_tokens = outputs[
        0
    ][
        inputs["input_ids"].shape[1]:
    ]

    response = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True,
    )

    print()
    print("Model:")
    print(response.strip())