from transformers import AutoTokenizer
import torch

from model import CodeReviewBot

tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
model = CodeReviewBot()
model.eval() 


def tokenize_code(code):
    tokens = tokenizer(
        code,
        return_tensors="pt",     
        max_length=512,          
        padding="max_length",    
        truncation=True         
    )
    return tokens["input_ids"], tokens["attention_mask"]

def review_code(code):
    input_ids, mask = tokenize_code(code)
    
    with torch.no_grad():  
        raw_output = model(input_ids, mask)
        scores = torch.sigmoid(raw_output) * 10
    
    return {
        "quality":      round(scores[0][0].item(), 2),
        "bug_risk":     round(scores[0][1].item(), 2),
        "readability":  round(scores[0][2].item(), 2),
        "complexity":   round(scores[0][3].item(), 2),
    }

code = """
def add(a, b):
    return a + b
"""
print(review_code(code))