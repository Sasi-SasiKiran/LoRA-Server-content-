import json
from pathlib import Path

DATA_DIR = Path("data")

FILES = [
    DATA_DIR / "train.jsonl",
    DATA_DIR / "validation.jsonl",
    DATA_DIR / "test.jsonl",
]


def validate_file(path):
    print(f"\nChecking: {path}")

    if not path.exists():
        print("ERROR: File does not exist.")
        return 0

    count = 0

    with open(path, "r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):

            if not line.strip():
                continue

            try:
                item = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"ERROR line {line_number}: Invalid JSON")
                print(e)
                continue

            if "messages" not in item:
                print(f"ERROR line {line_number}: Missing 'messages'")
                continue

            messages = item["messages"]

            if not isinstance(messages, list):
                print(f"ERROR line {line_number}: messages must be a list")
                continue

            roles = [message.get("role") for message in messages]

            if "user" not in roles:
                print(f"ERROR line {line_number}: Missing user message")
                continue

            if "assistant" not in roles:
                print(f"ERROR line {line_number}: Missing assistant message")
                continue

            valid_messages = True

            for message in messages:
                if "role" not in message or "content" not in message:
                    print(
                        f"ERROR line {line_number}: "
                        "Every message needs role and content"
                    )
                    valid_messages = False
                    break

            if not valid_messages:
                continue

            count += 1

    print(f"Valid examples: {count}")
    return count


def main():
    total = 0

    for file in FILES:
        total += validate_file(file)

    print("\n==============================")
    print(f"Total valid examples: {total}")
    print("==============================")


if __name__ == "__main__":
    main()