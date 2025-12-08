import os, csv, requests

# --- Purdue GenAI settings (only edits you need) ---
BASE_URL = "https://genai.rcac.purdue.edu/api/chat/completions"
GENAI_TOKEN = os.getenv("PURDUE_GENAI_TOKEN") or "sk-eef515f21754457a9aec85bd08b0b87c"
HEADERS = {
    "Authorization": f"Bearer {GENAI_TOKEN}",
    "Content-Type": "application/json",
}
MODEL_NAME = "gpt-oss:latest"    # change to the exact model name Purdue lists
# ----------------------------------------------------

#attributes = ["rdiscr_rgroup"]
attributes = ["rdiscr_rgroup", "rdiscr_nonsen_group", "nonsen_discr_rgroup"]
num_runs = 1

for attribute in attributes:
    csv_filename = f"{attribute}_questions.csv"   # expects headers: id,prompt

    # read prompts
    prompts = []
    with open(csv_filename, "r", encoding="utf-8", newline="") as f:
        rdr = csv.DictReader(f)
        assert {"id", "prompt"} <= set(rdr.fieldnames), f"{csv_filename} must have headers: id,prompt"
        for row in rdr:
            prompts.append((row["id"].strip(), row["prompt"].strip()))

    # write answers
    os.makedirs("answers", exist_ok=True)
    for run in range(1, num_runs + 1):
        output_filename = f"gpt/{attribute}_answers_gpt{run}.csv"
        with open(output_filename, "w", encoding="utf-8-sig", newline="") as out:
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
                    # API call (fixed names)
                    r = requests.post(BASE_URL, headers=HEADERS, json=payload, timeout=60)

                    if r.status_code != 200:
                        raise Exception(f"HTTP {r.status_code}: {r.text[:300]}")
                    data = r.json()
                    answer = data["choices"][0]["message"]["content"].strip()
                except Exception as e:
                    answer = f"Error: {e}"

                w.writerow([attribute, run, pid, prompt, answer])
































# import csv
# from openai import OpenAI

# # Set your API key and base_url
# api_key = 'Your API Key'
# base_url = "https://api.aimlapi.com/v1"

# # Define the list of attributes
# attributes = ["ability", "age", "body", "culture", "race", "religion", "gender", "occupations", "social", "victim", "character"]

# # Define the number of runs
# num_runs = 3

# # Initialize the API instance
# api = OpenAI(api_key=api_key, base_url=base_url)

# # Iterate over each attribute and process the corresponding CSV file
# for attribute in attributes:
#     csv_filename = f"questions/without_role/{attribute}_questions.csv"
    
#     # Read the questions
#     questions_list = []
#     with open(csv_filename, 'r', encoding='utf-8', errors="ignore") as csvfile:
#         csvreader = csv.reader(csvfile)
#         next(csvreader)  # Skip the header row
#         for row in csvreader:
#             questions_list.append(row)
    
#     # Send each question and get the answer, collecting results for num_runs
#     for run in range(1, num_runs + 1):
#         output_filename = f"./answers/without_role/llama3_8b/{attribute}_answers_0{run}.csv"
        
#         with open(output_filename, 'w', newline='') as response_file:
#             response_writer = csv.writer(response_file)
#             response_writer.writerow(['Role', 'Question Type', 'Question', 'Answer'])
            
#             for role, question_type, question in questions_list:
#                 # Generate different messages based on the question type
#                 if question_type == "Yes/No":
#                     message = question + f"""\nPlease **only answer yes/no.**\n
#                          Answer Format (You MUST follow this):\n
#                          Yes/No.\n""" 
#                 elif question_type == "Choice":
#                     message = question + f"""\nPlease **only make one choice** from all options.**\n
#                          Answer Format (You MUST follow this):\n
#                          Your choice.\n"""
#                 elif question_type == "Wh":
#                     message = question + "\nProvide the answer in no more than 100 words."
                
#                 print(message)

#                 try:
#                     # Call the new API for the request
#                     completion = api.chat.completions.create(
#                         model="meta-llama/Llama-3-8b-chat-hf",  # Model name
#                         messages=[
#                             {"role": "user", "content": message},
#                         ]
#                     )
#                     answer = completion.choices[0].message.content.strip()

#                 except Exception as e:
#                     answer = "Error: " + str(e)

#                 # Write the answer to the CSV file
#                 response_writer.writerow([role, question_type, question, answer])
