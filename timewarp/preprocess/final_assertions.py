import os
from tqdm import tqdm
import argparse
import json

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root_dir', type=str, required=True, help='Root directory')
    return parser.parse_args()

args = parse_args()

root_dir = args.root_dir
annotation_dir = os.path.join(root_dir, "normal_annotations")
video_dir = os.path.join(root_dir, "normal_videos")

annotation_files = [f for f in os.listdir(annotation_dir) if f.endswith('.json')]
video_files = [f for f in os.listdir(video_dir) if f.endswith('.mp4')]

annotation_names = [f.split('.')[0] for f in annotation_files]
video_names = [f.split('.')[0] for f in video_files]

for annotation_file in tqdm(annotation_files):
    annotation_name = annotation_file.split('.')[0]
    if annotation_name not in video_names:
        os.remove(os.path.join(annotation_dir, annotation_file))
    
    with open(os.path.join(annotation_dir, annotation_file), "r+") as f:
        data = json.load(f)
        data["scene_timestamps"] = [[int(start), int(end)] for start, end in data["scene_timestamps"]]
        f.seek(0)
        json.dump(data, f)
        f.truncate()

for video_file in tqdm(video_files):
    video_name = video_file.split('.')[0]
    if video_name not in annotation_names:
        os.remove(os.path.join(video_dir, video_file))

print(f"Number of files in video directory: {len(os.listdir(video_dir))}")
print(f"Number of files in annotation directory: {len(os.listdir(annotation_dir))}")