#!/usr/bin/env python3
"""
LoRA Training Script for Mistral 7B
Trains a LoRA adapter on constitution data with sentence-based chunking
"""

import os
import re
import torch
from pathlib import Path
from typing import List
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer
from datasets import Dataset
from peft import get_peft_model, LoraConfig, TaskType
import warnings
warnings.filterwarnings('ignore')

# Configuration
CONFIG = {
    "model_name": "mistralai/Mistral-7B-v0.1",
    "max_seq_length": 2048,
    "dtype": torch.float16,
    "lora_rank": 16,
    "lora_alpha": 32,
    "lora_dropout": 0.05,
    "learning_rate": 3e-4,
    "batch_size": 4,
    "epochs": 1,
    "output_dir": "unsloth_model",
}


def load_data_files(data_dir: str) -> str:
    """Load all text files from data directory."""
    data_path = Path(data_dir)
    if not data_path.exists():
        raise ValueError(f"Data directory not found: {data_dir}")

    text_content = ""
    for pattern in ["*.md", "*.txt", "*.json"]:
        for file_path in data_path.glob(pattern):
            print(f"Loading {file_path.name}...")
            with open(file_path, "r", encoding="utf-8") as f:
                text_content += f.read() + "\n\n"

    return text_content


def split_into_sentences(text: str) -> List[str]:
    """Split text into sentences using regex."""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences


def chunk_text_by_tokens(
    text: str,
    tokenizer,
    max_tokens: int = 2048,
) -> List[str]:
    """Chunk text into maximum token size, splitting by sentences."""
    sentences = split_into_sentences(text)
    chunks = []
    current_chunk = ""
    current_tokens = 0

    for sentence in sentences:
        sentence_tokens = len(tokenizer.encode(sentence, add_special_tokens=False))

        if current_tokens + sentence_tokens > max_tokens and current_chunk:
            chunks.append(current_chunk.strip())
            current_chunk = ""
            current_tokens = 0

        current_chunk += " " + sentence
        current_tokens += sentence_tokens

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks


def prepare_training_data(chunks: List[str]) -> Dataset:
    """Prepare dataset for training."""
    dataset = Dataset.from_dict({
        "text": chunks
    })
    return dataset


def tokenize_function(examples, tokenizer, max_length=2048):
    """Tokenize function for dataset."""
    return tokenizer(
        examples["text"],
        truncation=True,
        max_length=max_length,
        padding="max_length",
    )


def main():
    print("=" * 60)
    print("LoRA Training for Mistral 7B")
    print("=" * 60)

    os.makedirs(CONFIG["output_dir"], exist_ok=True)

    # Step 1: Load data
    print("\n[1/5] Loading training data...")
    text_data = load_data_files("data")
    print(f"Loaded {len(text_data):,} characters of text")

    # Step 2: Initialize tokenizer
    print("\n[2/5] Initializing tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(CONFIG["model_name"])
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # Step 3: Chunk text
    print("\n[3/5] Chunking text by tokens (max {})...".format(CONFIG["max_seq_length"]))
    chunks = chunk_text_by_tokens(
        text_data,
        tokenizer,
        max_tokens=CONFIG["max_seq_length"]
    )
    print(f"Created {len(chunks)} chunks")
    for i, chunk in enumerate(chunks[:3]):
        tokens = len(tokenizer.encode(chunk, add_special_tokens=False))
        print(f"  Chunk {i+1}: {tokens} tokens, {len(chunk)} characters")

    # Step 4: Load model
    print("\n[4/5] Loading Mistral 7B model...")
    print("Note: First download may take several minutes (~15GB)")

    try:
        model = AutoModelForCausalLM.from_pretrained(
            CONFIG["model_name"],
            device_map="auto",
            torch_dtype=CONFIG["dtype"],
            trust_remote_code=True,
        )
    except Exception as e:
        print(f"Error loading model: {e}")
        print("Make sure you have sufficient disk space and GPU memory")
        return

    # Add LoRA adapters
    peft_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=CONFIG["lora_rank"],
        lora_alpha=CONFIG["lora_alpha"],
        lora_dropout=CONFIG["lora_dropout"],
        bias="none",
        target_modules=["q_proj", "v_proj"],
    )

    model = get_peft_model(model, peft_config)
    print(f"Added LoRA adapters (rank={CONFIG['lora_rank']}, alpha={CONFIG['lora_alpha']})")

    # Step 5: Prepare data and train
    print("\n[5/5] Preparing data and starting training...")

    dataset = prepare_training_data(chunks)
    print(f"Dataset size: {len(dataset)} samples")

    tokenized_dataset = dataset.map(
        lambda x: tokenize_function(x, tokenizer, CONFIG["max_seq_length"]),
        batched=True,
    )

    training_args = TrainingArguments(
        output_dir=CONFIG["output_dir"],
        learning_rate=CONFIG["learning_rate"],
        per_device_train_batch_size=CONFIG["batch_size"],
        num_train_epochs=CONFIG["epochs"],
        save_strategy="epoch",
        logging_steps=5,
        gradient_accumulation_steps=4,
        fp16=True,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
    )

    print("Starting training...")
    trainer.train()

    # Save the trained model
    print(f"\nSaving model to {CONFIG['output_dir']}...")
    model.save_pretrained(CONFIG["output_dir"])
    tokenizer.save_pretrained(CONFIG["output_dir"])

    print("\n" + "=" * 60)
    print("Training completed successfully!")
    print(f"Model saved to: {CONFIG['output_dir']}")
    print("=" * 60)


if __name__ == "__main__":
    main()
