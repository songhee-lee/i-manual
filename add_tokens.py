from transformers import AutoTokenizer, AutoModelForQuestionAnswering, AutoConfig
import argparse
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model_name_or_path",
        default=None,
        type=str,
        required=True
    )
    parser.add_argument(
        "--data_path",
        default=None,
        type=str,
        required=True
    )
    parser.add_argument(
        "--output_dir",
        default=None,
        type=str,
        required=True
    )
    args = parser.parse_args() 
    
    # Load model and tokenizer
    config = AutoConfig.from_pretrained(args.model_name_or_path)
    tokenizer = AutoTokenizer.from_pretrained(args.model_name_or_path)
    model = AutoModelForQuestionAnswering.from_pretrained(args.model_name_or_path, config=config)

    # Load data
    f = open("add_tokens.txt", "r")
    data = f.read().split()

    # Add tokens 
    tokenizer.add_tokens(data)
    model.resize_token_embeddings(len(tokenizer))
    
    # Save model and tokenizer
    os.makedirs(args.output_dir, exist_ok=True)    

    model.save_pretrained(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)

if __name__ == "__main__":
    main()
