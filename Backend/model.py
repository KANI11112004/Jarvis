from transformers import BertTokenizer, BertForSequenceClassification
import torch

# Load the saved model
model = BertForSequenceClassification.from_pretrained('Backend/Models/bert_base_intent_classifier')
tokenizer = BertTokenizer.from_pretrained('Backend/Models/bert_base_intent_classifier')
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
def classify_query(text):
    encoding = tokenizer.encode_plus(
        text,
        add_special_tokens=True,
        max_length=64,
        return_token_type_ids=False,
        padding='max_length',
        truncation=True,
        return_attention_mask=True,
        return_tensors='pt',
    )
    
    input_ids = encoding['input_ids'].to(device)
    attention_mask = encoding['attention_mask'].to(device)
    
    with torch.no_grad():
        outputs = model(
            input_ids=input_ids,
            attention_mask=attention_mask
        )
    
    _, preds = torch.max(outputs.logits, dim=1)
    predicted_label = model.config.id2label[preds.item()]
    
    return predicted_label

print(classify_query("Hi"))