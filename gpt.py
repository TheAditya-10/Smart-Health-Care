from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import gc

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_name = 'microsoft/BioGPT-Large'
#model_name = 'ContactDoctor/Bio-Medical-Llama-3-8B'
tokenizer = AutoTokenizer.from_pretrained(model_name )
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32).to(device)

def predict_disease(symptoms, weight, height):
    prompt = f"""
    Here are the details of the patient:
    Symptoms: {symptoms}
    Weight: {weight} kg
    Height: {height} cm
    Q1. What is the probable disease that could be to this person and which type of disease is this?
    Q2. What should he/she should do now ? First hand precations.
    """
    
    try:
        input_ids = tokenizer.encode(prompt, return_tensors='pt').to(device)
        output = model.generate(
            input_ids, 
            max_length=150, 
            attention_mask=torch.ones_like(input_ids),
            temperature = 0.7, 
            do_sample=True,
            top_p=0.9,
            pad_token_id=tokenizer.eos_token_id,
            no_repeat_ngram_size=2)
        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
        result = generated_text.replace(prompt, '').strip()
        
        # Clean up GPU memory
        del input_ids, output
        torch.cuda.empty_cache()
        gc.collect()
        
        return result if result else "Error: No meaningful response generated."
    except torch.cuda.OutOfMemoryError:
        torch.cuda.empty_cache()
        return "Error: CUDA Out of Memory. Try reducing input size or model complexity."

    except Exception as e:
        return "Error", str(e)
    
print(predict_disease("fever", 60, 170))