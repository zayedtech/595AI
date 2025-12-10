import os, csv, requests

BASE_URL = "http://localhost:11434/v1/chat/completions"
HEADERS = {
    "Authorization": "Bearer ollama",
    "Content-Type": "application/json",
}
MODEL_NAME = "llama3.2:3b"              


attributes = ["rdiscr_rgroup", "rdiscr_nonsen_group", "nonsen_discr_rgroup"]
num_runs = 1

for attribute in attributes:
    csv_filename = f"{attribute}_questions.csv"   

  
    prompts = []
    with open(csv_filename, "r", encoding="utf-8", newline="") as f:
        rdr = csv.DictReader(f)
        assert {"id", "prompt"} <= set(rdr.fieldnames), f"{csv_filename} must have headers: id,prompt"
        for row in rdr:
            prompts.append((row["id"].strip(), row["prompt"].strip()))


    os.makedirs("answers", exist_ok=True)
    for run in range(1, num_runs + 1):
        output_filename = f"{attribute}_answers_llama{run}.csv"
        with open(output_filename, "w", encoding="utf-8", newline="") as out:
            w = csv.writer(out)
            w.writerow(["attribute", "run", "id", "prompt", "answer"])

            for pid, prompt in prompts:
                print(prompt)
                try:
                    fmt = (
                            "Answer in exactly 3 short bullet points. "
                            "Your answer should not exceed 37 words!"
                            
)
                    payload = {
                        "model": MODEL_NAME,
                        "messages": [{"role": "user", "content": f"{prompt}\n\n{fmt}"}],
                        "stream": False
                    }
                    r = requests.post(BASE_URL, headers=HEADERS, json=payload, timeout=60)
                    if r.status_code != 200:
                        raise Exception(f"HTTP {r.status_code}: {r.text[:300]}")
                    data = r.json()
                    answer = data["choices"][0]["message"]["content"].strip()
                except Exception as e:
                    answer = f"Error: {e}"

                w.writerow([attribute, run, pid, prompt, answer])









