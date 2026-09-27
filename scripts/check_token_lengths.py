import json
from pathlib import Path
from transformers import AutoTokenizer


MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"
DATA_DIR = Path("data")


print("Loading Qwen tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME,
    local_files_only=True
)

print("Tokenizer loaded successfully.")


def check_file(path):
    lengths = []

    with open(path, "r", encoding="utf-8") as f:

        for line_number, line in enumerate(f, start=1):

            if not line.strip():
                continue

            item = json.loads(line)

            messages = item["messages"]

            text = tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=False
            )

            tokens = tokenizer(
                text,
                add_special_tokens=False
            )["input_ids"]

            lengths.append(len(tokens))

    print()
    print("=" * 60)
    print(path)
    print("=" * 60)

    print(f"Examples: {len(lengths)}")
    print(f"Minimum tokens: {min(lengths)}")
    print(f"Maximum tokens: {max(lengths)}")
    print(f"Average tokens: {sum(lengths) / len(lengths):.2f}")

    over_512 = sum(x > 512 for x in lengths)

    print(f"Over 512 tokens: {over_512}")


for filename in [
    "train.jsonl",
    "validation.jsonl",
    "test.jsonl"
]:

    file_path = DATA_DIR / filename

    if not file_path.exists():
        print(f"ERROR: File not found: {file_path}")
        continue

    check_file(file_path)


print()
print("=" * 60)
print("TOKEN LENGTH CHECK COMPLETE")
print("=" * 60)