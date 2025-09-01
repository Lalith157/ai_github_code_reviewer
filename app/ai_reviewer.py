# app/ai_reviewer.py
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoModelForCausalLM, pipeline
import torch

# Vulnerability detection model
vuln_model_id = "mrm8488/codebert-base-finetuned-detect-insecure-code"
vuln_tokenizer = AutoTokenizer.from_pretrained(vuln_model_id)
vuln_model = AutoModelForSequenceClassification.from_pretrained(vuln_model_id)
vuln_pipeline = pipeline("text-classification", model=vuln_model, tokenizer=vuln_tokenizer)

# Syntax + optimization model
opt_model_id = "bigcode/starcoderbase-1b"
opt_tokenizer = AutoTokenizer.from_pretrained(opt_model_id)
opt_model = AutoModelForCausalLM.from_pretrained(
    opt_model_id,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    device_map="auto"
)

def review_pull_request(code: str, mode: str = "auto") -> str:
    """
    Reviews code for vulnerabilities, syntax errors, and optimizations.

    Args:
        code (str): The code to analyze.
        mode (str): "auto", "vulnerability", or "optimization".
            - auto: picks based on code content.
            - vulnerability: checks for security issues.
            - optimization: checks syntax errors + optimizations.

    Returns:
        str: Review feedback.
    """

    # Auto mode: simple heuristic
    if mode == "auto":
        if "SELECT" in code or "exec" in code or "input" in code:
            mode = "vulnerability"
        else:
            mode = "optimization"

    if mode == "vulnerability":
        result = vuln_pipeline(code)
        return f"🔍 Vulnerability Analysis:\n{result}"

    elif mode == "optimization":
        prompt = (
            "Review the following code. Identify any syntax errors, "
            "suggest improvements, and provide optimization tips:\n\n"
            f"{code}\n\n### Review:"
        )
        inputs = opt_tokenizer(prompt, return_tensors="pt").to(opt_model.device)
        outputs = opt_model.generate(
            **inputs,
            max_length=512,
            temperature=0.3,
            top_p=0.9,
            do_sample=True
        )
        review = opt_tokenizer.decode(outputs[0], skip_special_tokens=True)
        return f"🛠️ Syntax & Optimization Review:\n{review}"

    else:
        return "❌ Invalid mode. Use 'auto', 'vulnerability', or 'optimization'."
