import os
from openai import OpenAI
from tqdm import tqdm
import json
import argparse
from pprint import pprint
import tiktoken

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root_dir', type=str, required=True, help='Root directory')
    return parser.parse_args()

args = parse_args()

prompt_template = "Task Instructions: Given a caption that summarizes the events in the video and a question along with multiple choices, select the option based on the given caption that mostly relate to the temporal information provided in the events.\n\nGuidelines for answer Generation:\n\n1. Helpfulness: Answers should provide sufficient detail and depth to fully address the  question.\n\n2. Faithfulness: The answers must accurately reflect the information presented in the video caption. Avoid speculation or the inclusion of the information not contained or implied by the caption to maintain the integrity of the content.\n\nInput Video Caption: {}\n\nInput Question: {}\n\nOutput Format:\nAnswer: 4. <option4>"

benchmark = os.path.join(args.root_dir, "timewar_normal_benchmark_15k.json")
qa_dicts_all = []

with open(benchmark, "r") as f:
    benchmark_data = json.load(f)

for index, data in enumerate(tqdm(benchmark_data)):
    id = data['id'].replace(".mp4", "")

    try:
        json_filename = id + ".json"
        with open(os.path.join(args.root_dir, "shuffled_annotations", json_filename), "r") as f:
            json_data = json.load(f)

        prompt = prompt_template.format(json_data['shuffled_combined_captions'], data['question'])

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
        answers = response_text.split("Answer: ")[-1].strip().strip("\n")

        qa_dict = {
            "id": id + ".mp4",
            "question": data['question'],
            'answer': answers,
        }

        qa_dicts_all.append(qa_dict)
    
    except Exception as err:
        print(err)
        with open('benchmark_shuffled_error_log.txt', "a") as log_file:
            log_file.write(json_filename + "\n")
        
# Save qa_dicts_all
print(len(qa_dicts_all))
with open(os.path.join(args.root_dir, "temporal_shuffled_benchmark.json"), 'w') as f:
    json.dump(qa_dicts_all, f)