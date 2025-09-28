import os
from openai import OpenAI
from tqdm import tqdm
import json
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root_dir', type=str, required=True, help='Root directory')
    return parser.parse_args()

args = parse_args()

prompt_template = "Task Instructions: Given a caption that summarizes the events in the video, generate three multiple choice question-answer pairs that relate directly to the temporal information provided in the events. Make sure to ground the question to temporal understanding of the video content by including the words like 'beginning or end of the video', 'after', 'before' etc.\n\nGuidelines for QA Generation:\n\n1. Answer choices: For each question, produce four choices that can only be answered using the information from the video.\n\n2. Helpfulness: Answers should provide sufficient detail and depth to fully address the question. They should include relevant explanations, or context where appropriate to enhance temporal understanding.\n\n3. Faithfulness: The answers must accurately reflect the information presented in the video caption. Avoid speculation or the inclusion of the information not contained or implied by the caption to maintain the integrity of the content.\n\n4. Diversity: Craft questions that cover different temporal aspects of the video captions to provide a comprehensive understanding of the temporal context.\n\n5. Lastly, make sure that the options can not be ruled out based on just the options provided.\n\nInput Video Caption: {}\n\nOutput Format:\nQ1: <question1>\n1. <option1>\n2. <option2>\n3. <option3>\n4. <option4>\nA1: 2. <option2>\nQ2: <question2>\n1. <option1>\n2. <option2>\n3. <option3>\n4. <option4>\nA2: 1. <option1>\nQ3: <question3>\n1. <option1>\n2. <option2>\n3. <option3>\n4. <option4>\nA3: 4. <option4>"

qa_dicts_all = []

for filename in tqdm(sorted(os.listdir(os.path.join(args.root_dir, "normal_annotations")))):
    annotation_file_path = os.path.join(args.root_dir, "normal_annotations", filename)

    with open(annotation_file_path, 'r') as f:
        annotation_data = json.load(f)

    prompt = prompt_template.format(annotation_data['combined_captions'])

    client = OpenAI()

    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": prompt,
            }
        ],
        }
    ],
    # max_tokens=1024,
    )

    response_text = response.choices[0].message.content
    
    # Extract id from the filename
    id = filename.replace(".json", ".mp4")

    q1 = response_text.split("Q1:")[1].split("A1:")[0].strip().strip("\n")
    a1 = response_text.split("A1:")[1].split("Q2:")[0].strip().strip("\n")
    q2 = response_text.split("Q2:")[1].split("A2:")[0].strip().strip("\n")
    a2 = response_text.split("A2:")[1].split("Q3:")[0].strip().strip("\n")
    q3 = response_text.split("Q3:")[1].split("A3:")[0].strip().strip("\n")
    a3 = response_text.split("A3:")[1].strip().strip("\n")

    # Extract Q1, A1, Q2, A2, Q3, A3 from the response_text
    questions_answers = response_text.split("\n")
    qa_dicts = [
        {
            "id": id,
            "question": q1,
            "answer": a1
        },
        {
            "id": id,
            "question": q2,
            "answer": a2
        },
        {
            "id": id,
            "question": q3,
            "answer": a3
        },
    ]

    qa_dicts_all.extend(qa_dicts)

# Save the list of dictionaries as a json file
with open(os.path.join(args.root_dir, "timewar_normal_benchmark_15k.json"), "w") as file:
    json.dump(qa_dicts_all, file)