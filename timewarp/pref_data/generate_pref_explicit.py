import os
from openai import OpenAI
from tqdm import tqdm
import json
import argparse
from pprint import pprint

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root_dir', type=str, required=True, help='Root directory')
    parser.add_argument("--shuffled_dir_name", type=str, required=True, help='Name of the shuffled directory')
    parser.add_argument('--annotation_dir_name', type=str, required=True, help='Name of the annotation directory')
    parser.add_argument('--video_dir_name', type=str, required=True, help='Name of the video directory')
    return parser.parse_args()

args = parse_args()

prompt_template = "Task Instructions: Given a caption that summarizes the events in the video and the question, generate the corresponing answer resulting in question-answer pairs that relate directly to the temporal information provided in the events. \n\nGuidelines for Answer Generation:\n\n1. Helpfulness: Answers should provide sufficient detail and depth to fully address the question. They should include relevant explanations, or context where appropriate to enhance temporal understanding.\n\n2. Faithfulness: The answers must accurately reflect the information presented in the video caption. Avoid speculation or the inclusion of the information not contained or implied by the caption to maintain the integrity of the content.\n\nInput Video Caption: {}\n\nInput Question: {}\n\nOutput Format:\nAnswer: <answer>"
sft_data_path = os.path.join(args.root_dir, "temporal_sft_15k.json")

with open(sft_data_path, "r") as f:
    sft_data = json.load(f)

for data in tqdm(sft_data):
    id = data['id'].replace(".mp4", "")
    
    # Read the json file with same id
    try:
        json_filename = id + ".json"
        with open(os.path.join(args.root_dir, "shuffled", args.annotation_dir_name, json_filename), "r") as f:
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
        data['rejected'] = answers
    except Exception as err:
        print(err)
        with open("preference_error_log.txt", "a") as log_file:
            log_file.write(json_filename + "\n")

# Save it
with open(os.path.join(args.root_dir, "temporal_pref_15k.json"), "w") as file:
    json.dump(sft_data, file)

# Then check for saving the checkpoint
for item in sft_data:
    if 'rejected' not in item:
        print("temporal_preference_15k.json does not have the 'rejected' key for all items")
        break
    else:
        print("temporal_preference_15k.json has the 'rejected' key for all items")