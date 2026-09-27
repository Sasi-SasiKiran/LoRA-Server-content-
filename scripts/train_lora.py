import torch
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig,
)
from peft import (
    LoraConfig,
    prepare_model_for_kbit_training,
)
from trl import SFTTrainer, SFTConfig


# ============================================================
# CONFIGURATION
# ============================================================

MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"

TRAIN_FILE = "data/train.jsonl"
VALIDATION_FILE = "data/validation.jsonl"

OUTPUT_DIR = "outputs/cloud-operations-lora"


# ============================================================
# GPU CHECK
# ============================================================

if not torch.cuda.is_available():
    raise RuntimeError(
        "CUDA GPU is not available. "
        "Please check your PyTorch/CUDA installation."
    )

print("=" * 60)
print("GPU INFORMATION")
print("=" * 60)

print("GPU:", torch.cuda.get_device_name(0))

print(
    "GPU Memory:",
    round(
        torch.cuda.get_device_properties(0).total_memory
        / 1024**3,
        2
    ),
    "GB"
)


# ============================================================
# TOKENIZER
# ============================================================

print()
print("=" * 60)
print("LOADING TOKENIZER")
print("=" * 60)

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME,
    local_files_only=True,
)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

print("Tokenizer loaded.")
print("Pad token:", tokenizer.pad_token)


# ============================================================
# 4-BIT QUANTIZATION
# ============================================================

print()
print("=" * 60)
print("CONFIGURING 4-BIT QUANTIZATION")
print("=" * 60)

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
)

print("4-bit NF4 enabled.")
print("Compute dtype: float16")


# ============================================================
# LOAD MODEL
# ============================================================

print()
print("=" * 60)
print("LOADING QWEN MODEL")
print("=" * 60)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    quantization_config=bnb_config,
    device_map="auto",
    local_files_only=True,
)

print("Model loaded.")


# ============================================================
# PREPARE MODEL FOR LoRA
# ============================================================

print()
print("=" * 60)
print("PREPARING MODEL FOR LoRA")
print("=" * 60)

model = prepare_model_for_kbit_training(model)

# Required for gradient checkpointing
model.config.use_cache = False

print("Base model prepared.")
print("Base model will remain frozen.")


# ============================================================
# LoRA CONFIGURATION
# ============================================================

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

print()
print("=" * 60)
print("LoRA CONFIGURATION")
print("=" * 60)

print("Rank:", lora_config.r)
print("Alpha:", lora_config.lora_alpha)
print("Dropout:", lora_config.lora_dropout)
print("Target modules:", lora_config.target_modules)


# ============================================================
# LOAD DATASET
# ============================================================

print()
print("=" * 60)
print("LOADING DATASET")
print("=" * 60)

dataset = load_dataset(
    "json",
    data_files={
        "train": TRAIN_FILE,
        "validation": VALIDATION_FILE,
    },
)

print("Training examples:", len(dataset["train"]))
print("Validation examples:", len(dataset["validation"]))


# ============================================================
# TRAINING CONFIGURATION
# ============================================================

training_args = SFTConfig(
    output_dir=OUTPUT_DIR,

    # --------------------------------------------------------
    # Training
    # --------------------------------------------------------

    num_train_epochs=2,

    per_device_train_batch_size=1,

    gradient_accumulation_steps=8,

    # --------------------------------------------------------
    # Learning rate
    # --------------------------------------------------------

    learning_rate=2e-4,

    lr_scheduler_type="cosine",

    warmup_steps=20,

    # --------------------------------------------------------
    # Precision
    # --------------------------------------------------------
    #
    # IMPORTANT:
    # Previous training failed because GradScaler attempted
    # to unscale BF16 gradients.
    #
    # Disable AMP for the LoRA optimizer.
    # The base model is STILL loaded in 4-bit.
    #

    fp16=False,

    bf16=False,

    # --------------------------------------------------------
    # Memory optimization
    # --------------------------------------------------------

    gradient_checkpointing=True,

    # --------------------------------------------------------
    # Optimizer
    # --------------------------------------------------------

    optim="paged_adamw_8bit",

    # --------------------------------------------------------
    # Sequence length
    # --------------------------------------------------------

    max_length=512,

    # --------------------------------------------------------
    # Evaluation
    # --------------------------------------------------------

    eval_strategy="epoch",

    per_device_eval_batch_size=1,

    # --------------------------------------------------------
    # Saving
    # --------------------------------------------------------

    save_strategy="epoch",

    save_total_limit=2,

    # --------------------------------------------------------
    # Logging
    # --------------------------------------------------------

    logging_strategy="steps",

    logging_steps=10,

    # --------------------------------------------------------
    # Reproducibility
    # --------------------------------------------------------

    seed=42,

    # --------------------------------------------------------
    # Disable external logging
    # --------------------------------------------------------

    report_to="none",

    # --------------------------------------------------------
    # Dataset handling
    # --------------------------------------------------------

    packing=False,

    # --------------------------------------------------------
    # Padding
    # --------------------------------------------------------

    pad_token=tokenizer.pad_token,
)


# ============================================================
# CREATE TRAINER
# ============================================================

print()
print("=" * 60)
print("CREATING SFT TRAINER")
print("=" * 60)

trainer = SFTTrainer(
    model=model,
    args=training_args,

    train_dataset=dataset["train"],

    eval_dataset=dataset["validation"],

    processing_class=tokenizer,

    peft_config=lora_config,
)

print("Trainer created successfully.")


# ============================================================
# SHOW TRAINABLE PARAMETERS
# ============================================================

print()
print("=" * 60)
print("TRAINABLE PARAMETERS")
print("=" * 60)

trainer.model.print_trainable_parameters()


# ============================================================
# TRAIN
# ============================================================

print()
print("=" * 60)
print("STARTING LoRA TRAINING")
print("=" * 60)

print()
print("Base model: Qwen2.5-1.5B-Instruct")
print("Quantization: 4-bit NF4")
print("Fine-tuning: LoRA")
print("Base model: FROZEN")
print("Trainable parameters: LoRA adapters only")
print("AMP: DISABLED")
print()

trainer.train()


# ============================================================
# SAVE LoRA ADAPTER
# ============================================================

print()
print("=" * 60)
print("SAVING LoRA ADAPTER")
print("=" * 60)

trainer.save_model(OUTPUT_DIR)

tokenizer.save_pretrained(OUTPUT_DIR)

print()
print("LoRA adapter saved to:")
print(OUTPUT_DIR)


# ============================================================
# FINAL GPU MEMORY
# ============================================================

print()
print("=" * 60)
print("FINAL GPU MEMORY")
print("=" * 60)

allocated = torch.cuda.memory_allocated() / 1024**3
reserved = torch.cuda.memory_reserved() / 1024**3

print(f"Allocated: {allocated:.2f} GB")
print(f"Reserved:  {reserved:.2f} GB")


# ============================================================
# COMPLETE
# ============================================================

print()
print("=" * 60)
print("TRAINING COMPLETE")
print("=" * 60)

print()
print("LoRA adapter location:")
print(OUTPUT_DIR)