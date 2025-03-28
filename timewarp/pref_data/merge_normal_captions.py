import os
import json
from tqdm import tqdm
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root_dir', type=str, required=True, help='Root directory')
    return parser.parse_args()

args = parse_args()

for annotation_file in tqdm(sorted(os.listdir(os.path.join(args.root_dir, "normal_annotations")))):
    annotation_file_path = os.path.join(args.root_dir, "normal_annotations", annotation_file)
    with open(annotation_file_path, 'r') as f:
        annotation_data = json.load(f)
    annotation_data['combined_captions'] = " ".join(annotation_data['description'])

    with open(annotation_file_path, 'w') as f:
        json.dump(annotation_data, f)

annotation_files = os.listdir(os.path.join(args.root_dir, "normal_annotations"))
for annotation_file in annotation_files:
    annotation_file_path = os.path.join(args.root_dir, "normal_annotations", annotation_file)
    with open(annotation_file_path, 'r') as f:
        annotation_data = json.load(f)
    if 'combined_captions' not in annotation_data:
        raise ValueError(f"'combined_captions' key not found in {annotation_file}")
