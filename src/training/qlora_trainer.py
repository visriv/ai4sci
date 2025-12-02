from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig, get_peft_model
from datasets import load_dataset
from trl import SFTTrainer

def train_qlora(model_name, dataset_path, output_dir):
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        load_in_4bit=True,
        device_map="auto"
    )

    lora_cfg = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )

    model = get_peft_model(model, lora_cfg)

    dataset = load_dataset("json", data_files=dataset_path)

    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=dataset["train"],
        dataset_text_field="text",
        output_dir=output_dir
    )

    trainer.train()
    model.save_pretrained(output_dir)
