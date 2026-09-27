import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"

print("Loading tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

print("Loading model in 4-bit...")

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True
)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    quantization_config=bnb_config,
    device_map="auto"
)

print("\nModel loaded successfully!")
print("GPU:", torch.cuda.get_device_name(0))
print(
    "VRAM allocated:",
    round(torch.cuda.memory_allocated() / 1024**2, 2),
    "MB"
)

messages = [
    {
        "role": "system",
        "content": "You are a Cloud and Server Operations Specialist."
    },
    {
        "role": "user",
        "content": "A Linux server has very high CPU usage. What should I check first?"
    }
]

text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)

inputs = tokenizer(text, return_tensors="pt").to(model.device)

print("\nGenerating response...")

with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_new_tokens=150,
        temperature=0.7,
        do_sample=True
    )

response = tokenizer.decode(
    outputs[0][inputs["input_ids"].shape[1]:],
    skip_special_tokens=True
)

print("\n========== MODEL RESPONSE ==========\n")
print(response)

print("\n====================================")
print(
    "VRAM allocated:",
    round(torch.cuda.memory_allocated() / 1024**2, 2),
    "MB"
)