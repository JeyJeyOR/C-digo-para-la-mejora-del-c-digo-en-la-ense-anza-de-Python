import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import time

def build_prompt(reference_code: str, code_to_evaluate: str, topic_level: int) -> str:
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

reference_code = """

def pedir_numero(msg, min):
    num = int(input(f"{msg}(>{min}): "))
    while num <= min:
        num = int(input(f"Error. {msg} (>{min}): "))
    return num

def add_edad_a_rango(rangos, edad):
    if 0 <= edad <= 9:
        rangos[0] = rangos[0] + 1
    elif 10 <= edad <= 19:
        rangos[1] = rangos[1] + 1
    elif 20 <= edad <= 29:
        rangos[2] = rangos[2] + 1
    elif 30 <= edad <= 39:
        rangos[3] = rangos[3] + 1
    elif 40 <= edad <= 49:
        rangos[4] = rangos[4] + 1
    elif 50 <= edad <= 59:
        rangos[5] = rangos[5] + 1
    elif 60 <= edad <= 69:
        rangos[6] = rangos[6] + 1
    elif 70 <= edad <= 79:
        rangos[7] = rangos[7] + 1
    elif 80 <= edad <= 89:
        rangos[8] = rangos[8] + 1
    elif 90 <= edad <= 99:
        rangos[9] = rangos[9] + 1
    else:
        rangos[10] = rangos[10] + 1


def pedir_edad_persona(dim, rangos):
    lista = []
    for i in range(dim):
        n = int(input(f"Introduce la edad de la persona {i+1}: "))
        while n < 0:
            print("Error: la edad debe ser positiva. Vuelve a introducirla.")
            n = int(input(f"Introduce la edad de la persona {i+1}: "))
        add_edad_a_rango(rangos, n)
        lista.append(n)

    return lista


def inicializar_listas_rangos():
    rangos_str = [
        " 0 -  9 :",
        "10 - 19 :",
        "20 - 29 :",
        "30 - 39 :",
        "40 - 49 :",
        "50 - 59 :",
        "60 - 69 :",
        "70 - 79 :",
        "80 - 89 :",
        "90 - 99 :",
        "100 -   :",
    ]
    rangos_edades = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    return rangos_edades, rangos_str


def mostrar_rangos_edades(lista, lista_str):
    for i in range(len(lista)):
        print(f"{lista_str[i]} {lista[i]}")


def main():
    dimension = pedir_numero("Introduce el número de personas", 2)
    rangos_edades, rangos_str = inicializar_listas_rangos()
    pedir_edad_persona(dimension, rangos_edades)
    print("Número de personas por intervalo:: ")
    mostrar_rangos_edades(rangos_edades, rangos_str)


if __name__ == "__main__":
    main()


"""

code_to_evaluate = """
def numero_personas():
    personas=int(input("Introduce el numero de personas: "))
    while personas<0:
        print("Error en el rango")
        personas=int(input("Introduce de nuevo el numero de personas: "))
    return personas

def pedir_edad(cantidad_personas):
    numero_edades_introducidas=1
    lista=[]
    while numero_edades_introducidas<cantidad_personas+1:
        edad=int(input(f"Introduce la edad de la persona {numero_edades_introducidas}: "))
        while edad<0:
            print("Error: la edad debe ser positiva. Vuelve a introducirla.")
            edad=int(input(f"Introduce la edad de la persona {numero_edades_introducidas}: "))
        lista.append(edad)
        numero_edades_introducidas=numero_edades_introducidas+1
    return lista

def clasificacion(lista_edades):
    lista_cantidades=[]
    edad_0_9=0
    edad_10_19=0
    edad_20_29=0
    edad_30_39=0
    edad_40_49=0
    edad_50_59=0
    edad_60_69=0
    edad_70_79=0
    edad_80_89=0
    edad_90_99=0
    edad_100=0
    for i in range(len(lista_edades)):
        if 0<=lista_edades[i]<=9:
            edad_0_9=edad_0_9+1
        if 10<=lista_edades[i]<=19:
            edad_10_19=edad_10_19+1
        if 20<=lista_edades[i]<=29:
            edad_20_29=edad_20_29+1
        if 30<=lista_edades[i]<=39:
            edad_30_39=edad_30_39+1
        if 40<=lista_edades[i]<=49:
            edad_40_49=edad_40_49+1
        if 50<=lista_edades[i]<=59:
            edad_50_59=edad_50_59+1
        if 60<=lista_edades[i]<=69:
            edad_60_69=edad_60_69+1
        if 70<=lista_edades[i]<=79:
            edad_70_79=edad_70_79+1
        if 80<=lista_edades[i]<=89:
            edad_80_89=edad_80_89+1
        if 90<=lista_edades[i]<=99:
            edad_90_99=edad_90_99+1
        if lista_edades[i]>=100:
            edad_100=edad_100+1
    lista_cantidades.append(edad_0_9)
    lista_cantidades.append(edad_10_19)
    lista_cantidades.append(edad_20_29)
    lista_cantidades.append(edad_30_39)
    lista_cantidades.append(edad_40_49)
    lista_cantidades.append(edad_50_59)
    lista_cantidades.append(edad_60_69)
    lista_cantidades.append(edad_70_79)
    lista_cantidades.append(edad_80_89)
    lista_cantidades.append(edad_90_99)
    lista_cantidades.append(edad_100)
    return lista_cantidades

def main():
    cantidad_personas=numero_personas()
    lista_edades=pedir_edad(cantidad_personas)
    lista_nueva=clasificacion(lista_edades)
    for j in range(len(lista_nueva)):
        
        if j==0:
            print(f"0-9:   {lista_nueva[j]}")
        if j==1:
            print(f"10-19: {lista_nueva[j]}")
        if j==2:
            print(f"20-29: {lista_nueva[j]}")
        if j==3:
            print(f"30-39: {lista_nueva[j]}")
        if j==4:
            print(f"40-49: {lista_nueva[j]}")
        if j==5:
            print(f"50-59: {lista_nueva[j]}")
        if j==6:
            print(f"60-69: {lista_nueva[j]}")
        if j==7:
            print(f"70-79: {lista_nueva[j]}")
        if j==8:
            print(f"80-89: {lista_nueva[j]}")
        if j==9:
            print(f"90-99: {lista_nueva[j]}")
        if j==10:
            print(f"100- : {lista_nueva[j]}")
    

if __name__=="__main__":
    main()

"""

model_id = "mistralai/Mistral-7B-Instruct-v0.3"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    trust_remote_code=True,
    device_map="auto",
    load_in_4bit=True,
    torch_dtype=torch.bfloat16,
    bnb_4bit_quant_type="nf4"
)

prompt = build_prompt(reference_code, code_to_evaluate, topic_level=2)

start_time = time.time()
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
outputs = model.generate(
    **inputs,
    do_sample=True,
    temperature=0.4,
    top_p=0.95,
    max_new_tokens=1500,
    repetition_penalty=1.2,
    eos_token_id=tokenizer.eos_token_id,
    pad_token_id=tokenizer.eos_token_id
)
response = tokenizer.decode(outputs[0], skip_special_tokens=True)
elapsed_time = time.time() - start_time

print("\n=== Output ===\n")
print(response)

with open("resultado_llama.txt", "w", encoding="utf-8") as f:
    f.write(f"Tiempo de ejecución: {elapsed_time:.2f} segundos\n\n")
    f.write("Prompt utilizado:\n")
    f.write(prompt)
    f.write("\n\nRespuesta generada:\n")
    f.write(response)

tokens = tokenizer(prompt, return_tensors="pt")["input_ids"]
print(f"Número de tokens: {tokens.shape[1]}")


