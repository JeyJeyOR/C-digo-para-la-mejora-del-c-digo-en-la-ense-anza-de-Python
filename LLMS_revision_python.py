import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import time

def load_code_from_file(filename: str) -> str:  
    """Carga el código desde un archivo .py proporcionado."""
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()
    

def build_prompt(reference_code: str, code_to_evaluate: str, topic_level: int) -> str: 
    """Construye el prompt en función del nivel de dificultad escogido."""
    topic_coverage = {
        1: "1. Introduction: Data types (bool, int, float, complex), values and variables, operators and operands, expressions and statements, basic I/O and comments.",
        2: "2. Control flow: Logical expressions, conditional statements and loops.",
        3: "3. Functions.",
        4: "4. Data containers: Sequences (lists, tuples, ranges, strings), iterators, list comprehensions, generators, sets, docstrings and dictionaries.",
        5: "5. Object-oriented programming: Classes and objects, attributes and methods, inheritance and exceptions.",
        6: "6. Files: Open and close, reading and writing."
    }

    if topic_level not in topic_coverage:
        raise ValueError("Topic level must be between 1 and 6.")

    known_topics = "\n".join(topic_coverage[i] for i in range(1, topic_level + 1))

    prompt = f"""

You will be given two Python code snippets: a reference solution and a student's version.
Your task is to provide suggestions to improve the student's code based on: naming, clarity, validation, modularity, logical structure and readability.
The student has only learned the following topics:
{known_topics}
Your response must only include improvements that the student can understand given the topics listed above.
Only include improvements of the known topics.
For each suggestion, include what could be improved, why is it important and what should be done.
Do not include any revised or rewritten code.

### Reference solution:
{reference_code}

### Student's code:
{code_to_evaluate}

### Response:
"""
    return prompt.strip()

reference_code = load_code_from_file("reference_code.py")   ##Codigo del profesor
code_to_evaluate = load_code_from_file("student_code.py")   ##Codigo del alumno

model_id = "mistralai/Mistral-7B-Instruct-v0.3" ##Modelo a utilizar

tokenizer = AutoTokenizer.from_pretrained(model_id) ##Tokenizador
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    trust_remote_code=True,
    device_map="auto",
    load_in_4bit=True,  ##Cuantización  4 bits
    torch_dtype=torch.bfloat16, 
    bnb_4bit_quant_type="nf4"
)

prompt = build_prompt(reference_code, code_to_evaluate, topic_level=2)    ##Nivel de dificultad

start_time = time.time()    ##Comprobar cuanto tarda en ejecutarse
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
outputs = model.generate(
    **inputs,
    do_sample=True,
    temperature=0.4,    ##Creatividad escogida
    top_p=0.95, ##Limitacion del diccionario
    max_new_tokens=1500,    ##Numero de tokens máximos a la salida
    repetition_penalty=1.2, ##Penalización de repetición para evitar que entre en bucle
    eos_token_id=tokenizer.eos_token_id,
    pad_token_id=tokenizer.eos_token_id
)
response = tokenizer.decode(outputs[0], skip_special_tokens=True)
elapsed_time = time.time() - start_time

print("\n=== Output ===\n")
print(response)

with open("resultado_llama.txt", "w", encoding="utf-8") as f:
    """Funcion para guardar los resultados en un archivo de texto."""
    f.write(f"Tiempo de ejecución: {elapsed_time:.2f} segundos\n\n")
    f.write("Prompt utilizado:\n")
    f.write(prompt)
    f.write("\n\nRespuesta generada:\n")
    f.write(response)

tokens = tokenizer(prompt, return_tensors="pt")["input_ids"]
print(f"Número de tokens: {tokens.shape[1]}")




