import json
from pathlib import Path
from collections import Counter

DATA_DIR = Path("data")

FILES = {
    "train": DATA_DIR / "train.jsonl",
    "validation": DATA_DIR / "validation.jsonl",
    "test": DATA_DIR / "test.jsonl",
}


def load_dataset(path):
    data = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))

    return data


def analyze_dataset(name, path):
    print("\n" + "=" * 60)
    print(f"{name.upper()} DATASET")
    print("=" * 60)

    data = load_dataset(path)

    print(f"Examples: {len(data)}")

    user_lengths = []
    assistant_lengths = []
    total_lengths = []

    categories = Counter()

    for item in data:
        messages = item["messages"]

        user_text = ""
        assistant_text = ""
        system_text = ""

        for message in messages:
            role = message["role"]
            content = message["content"]

            if role == "system":
                system_text = content

            elif role == "user":
                user_text = content

            elif role == "assistant":
                assistant_text = content

        user_len = len(user_text.split())
        assistant_len = len(assistant_text.split())
        system_len = len(system_text.split())
        total_len = user_len + assistant_len + system_len

        user_lengths.append(user_len)
        assistant_lengths.append(assistant_len)
        total_lengths.append(total_len)

              # Category detection based on keywords
        text = (user_text + " " + assistant_text).lower()

        if any(x in text for x in [
            "linux", "systemd", "ssh", "cron", "filesystem",
            "swap", "kernel", "load average", "ntp"
        ]):
            categories["Linux"] += 1

        elif any(x in text for x in [
            "docker", "container", "dockerfile", "docker compose"
        ]):
            categories["Docker"] += 1

        elif any(x in text for x in [
            "kubernetes", "kubectl", "pod", "k8s", "eks", "aks", "gke"
        ]):
            categories["Kubernetes"] += 1

        elif any(x in text for x in [
            "aws", "ec2", "s3", "cloudwatch", "lambda", "rds",
            "ecs", "vpc", "eks", "api gateway"
        ]):
            categories["AWS"] += 1

        elif any(x in text for x in [
            "azure", "azure vm", "app service", "azure function",
            "azure sql", "key vault", "aks"
        ]):
            categories["Azure"] += 1

        elif any(x in text for x in [
            "gcp", "google cloud", "compute engine", "cloud run",
            "cloud sql", "gke", "cloud storage"
        ]):
            categories["GCP"] += 1

        elif any(x in text for x in [
            "prometheus", "grafana", "monitoring", "alert",
            "metrics", "promql"
        ]):
            categories["Monitoring"] += 1

        elif any(x in text for x in [
            "database", "mysql", "postgres", "sql query",
            "replication", "deadlock", "connection pool"
        ]):
            categories["Database"] += 1

        elif any(x in text for x in [
            "security", "authentication", "authorization",
            "iam", "secret", "certificate", "firewall"
        ]):
            categories["Security"] += 1

        elif any(x in text for x in [
            "deployment", "ci pipeline", "release", "rollback",
            "deployment artifact", "canary", "blue-green"
        ]):
            categories["Deployment"] += 1

        elif any(x in text for x in [
            "incident", "root cause", "rca", "outage",
            "incident timeline", "incident investigation"
        ]):
            categories["Incident Response"] += 1

        elif any(x in text for x in [
            "network", "dns", "tcp", "udp", "latency",
            "packet loss", "routing", "vlan", "vpn"
        ]):
            categories["Networking"] += 1

        else:
            categories["Other"] += 1

    def stats(values):
        return {
            "minimum": min(values),
            "maximum": max(values),
            "average": round(sum(values) / len(values), 2),
        }

    print("\nUser text length:")
    print(stats(user_lengths))

    print("\nAssistant text length:")
    print(stats(assistant_lengths))

    print("\nTotal text length:")
    print(stats(total_lengths))

    print("\nCategories:")
    for category, count in categories.most_common():
        percentage = count / len(data) * 100
        print(f"{category:15} {count:4} ({percentage:.1f}%)")

    # Detect duplicate user questions
    questions = [
        next(
            message["content"]
            for message in item["messages"]
            if message["role"] == "user"
        )
        for item in data
    ]

    duplicate_count = len(questions) - len(set(questions))

    print(f"\nDuplicate user questions: {duplicate_count}")

    # Detect very short answers
    short_answers = 0

    for item in data:
        answer = next(
            message["content"]
            for message in item["messages"]
            if message["role"] == "assistant"
        )

        if len(answer.split()) < 30:
            short_answers += 1

    print(f"Very short assistant answers (<30 words): {short_answers}")


def main():
    for name, path in FILES.items():
        if not path.exists():
            print(f"ERROR: Missing {path}")
            return

        analyze_dataset(name, path)

    print("\n" + "=" * 60)
    print("DATASET QUALITY CHECK COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()