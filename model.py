import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModel

class CodeReviewBot(nn.Module):
    def __init__(self):
        super ().__init__()
        self.encoder = AutoModel.from_pretrained("microsoft/codebert-base")
        self.classifier = nn.Linear(768, 4)  

    def forward(self, input_ids, attention_mask):
        outputs = self.encoder(input_ids=input_ids, attention_mask=attention_mask)
        cls_token = outputs.last_hidden_state[:, 0, :]
        return self.classifier(cls_token)



model = CodeReviewBot()
input_ids = torch.randint(0, 1000, (2, 10))
attention_mask = torch.ones(2, 10, dtype=torch.long)

raw_output = model(input_ids, attention_mask)
scores = torch.sigmoid(raw_output) * 10

print("Raw output:", raw_output)
print("Scores (0-10):", scores)