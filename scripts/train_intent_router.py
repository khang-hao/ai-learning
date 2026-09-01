import argparse
import json
import random
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
BACKEND_DIR = ROOT_DIR / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.ml.intent_classifier import (
    DEFAULT_INTENT_MODEL_NAME,
    DEFAULT_INTENT_TOKENIZER_NAME,
    INTENT_LABELS,
)
from torch.utils.data import DataLoader, Dataset

def main() -> None:
    parser = argparse.ArgumentParser(description="Train the Coursework Copilot intent router.")
    parser.add_argument(
        "--dataset",
        default="data/training/intent_router.sample.jsonl",
        help="Path to a JSONL dataset with fields: text, label",
    )
    parser.add_argument(
        "--output",
        default="data/processed/ml/intent_router",
        help="Directory where the trained model should be saved",
    )
    parser.add_argument(
        "--model-name",
        default=DEFAULT_INTENT_MODEL_NAME,
        help="Hugging Face model name to fine-tune",
    )
    parser.add_argument(
        "--tokenizer-name",
        default=DEFAULT_INTENT_TOKENIZER_NAME,
        help="Tokenizer source to use for training and saving the classifier bundle",
    )
    parser.add_argument("--epochs", type=int, default=4)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--learning-rate", type=float, default=5e-5)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    import torch
    from torch.optim import AdamW
    from transformers import AutoModelForSequenceClassification, AutoTokenizer

    random.seed(args.seed)
    torch.manual_seed(args.seed)

    dataset_path = Path(args.dataset)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    examples = _load_examples(dataset_path)
    if len(examples) < 12:
        raise ValueError("Need at least 12 labeled training examples to train the intent router.")

    random.shuffle(examples)
    split_index = max(1, int(len(examples) * 0.8))
    train_examples = examples[:split_index]
    eval_examples = examples[split_index:]

    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer_name, use_fast=False)
    model = AutoModelForSequenceClassification.from_pretrained(
        args.model_name,
        num_labels=len(INTENT_LABELS),
    )

    train_dataset = IntentDataset(train_examples, tokenizer)
    eval_dataset = IntentDataset(eval_examples, tokenizer)
    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True)
    eval_loader = DataLoader(eval_dataset, batch_size=args.batch_size, shuffle=False)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    optimizer = AdamW(model.parameters(), lr=args.learning_rate)

    for epoch in range(args.epochs):
        model.train()
        for batch in train_loader:
            batch = {key: value.to(device) for key, value in batch.items()}
            outputs = model(**batch)
            loss = outputs.loss
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

    accuracy = evaluate(model, eval_loader, device)

    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    (output_dir / "labels.json").write_text(json.dumps(INTENT_LABELS, indent=2), encoding="utf-8")
    (output_dir / "metrics.json").write_text(
        json.dumps(
            {
                "eval_accuracy": accuracy,
                "epochs": args.epochs,
                "model_name": args.model_name,
                "tokenizer_name": args.tokenizer_name,
                "train_examples": len(train_examples),
                "eval_examples": len(eval_examples),
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"Saved trained model to {output_dir}")
    print(f"Evaluation accuracy: {accuracy:.3f}")


class IntentDataset(Dataset):
    def __init__(self, examples: list[dict[str, str]], tokenizer) -> None:
        self.examples = examples
        self.tokenizer = tokenizer

    def __len__(self) -> int:
        return len(self.examples)

    def __getitem__(self, index: int) -> dict:
        example = self.examples[index]
        encoded = self.tokenizer(
            example["text"],
            truncation=True,
            padding="max_length",
            max_length=96,
            return_tensors="pt",
        )
        item = {key: value.squeeze(0) for key, value in encoded.items()}
        item["labels"] = _label_to_tensor(example["label"])
        return item


def evaluate(model, loader, device) -> float:
    import torch

    if len(loader.dataset) == 0:
        return 0.0

    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for batch in loader:
            labels = batch["labels"].to(device)
            inputs = {key: value.to(device) for key, value in batch.items() if key != "labels"}
            logits = model(**inputs).logits
            predictions = torch.argmax(logits, dim=-1)
            correct += int((predictions == labels).sum().item())
            total += int(labels.size(0))

    return correct / total if total else 0.0


def _label_to_tensor(label: str):
    import torch

    return torch.tensor(INTENT_LABELS.index(label), dtype=torch.long)


def _load_examples(path: Path) -> list[dict[str, str]]:
    examples: list[dict[str, str]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        label = record["label"]
        if label not in INTENT_LABELS:
            raise ValueError(f"Unsupported label in dataset: {label}")
        examples.append({"text": record["text"], "label": label})
    return examples


if __name__ == "__main__":
    main()
