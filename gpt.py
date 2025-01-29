from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
device = 'cuda'
model = AutoModelForCausalLM.from_pretrained("gpt2", torch_dtype=torch.bfloat16, attn_implimentation='flash_attention_2')
tokenizer = AutoTokenizer.from_pretrained('gpt2')

prompt = "Hello I'm Aditya. How are you"

input_ids = tokenizer(prompt, return_tensors='pt').input_ids

gen_token = model.generate(input_ids, max_length=100, temperature=0.9, do_sample=True)

gen_text = tokenizer.batch_decode(gen_token, skip_special_tokens=True)[0]

print(gen_text)