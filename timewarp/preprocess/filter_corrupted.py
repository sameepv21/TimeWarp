import os
import cv2
from tqdm import tqdm
import time
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root_dir', type=str, required=True, help='Path to the preprocessed finevideo dataset')
    return parser.parse_args()

args = parse_args()

# Define directories
video_dir = os.path.join(args.root_dir, "normal_videos")
annotation_dir = os.path.join(args.root_dir, "normal_annotations")

# Check if video files are corrupted and if annotation files exist
corrupted_videos = []
print("Checking for corrupted videos...")
for filename in tqdm(os.listdir(video_dir)):
    video_path = os.path.join(video_dir, filename)
    annotation_path = os.path.join(annotation_dir, filename.replace('.mp4', '.json'))
    
    # Check if video file is corrupted
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        corrupted_videos.append(filename)
        os.remove(video_path)
    
    # Check if annotation file exists
    if not os.path.exists(annotation_path):
        os.remove(video_path)
print("Done")
time.sleep(1)

print("Checking for corrupted annotations...")
# Remove annotation files for deleted videos
for filename in tqdm(os.listdir(annotation_dir)):
    video_path = os.path.join(video_dir, filename.replace('.json', '.mp4'))
    if not os.path.exists(video_path):
        os.remove(os.path.join(annotation_dir, filename))
print("Done")
time.sleep(1)

# Ensure that the same names for video and annotation are there
print("Common name check...")
video_files = os.listdir(video_dir)
annotation_files = [file.replace('.json', '.mp4') for file in os.listdir(annotation_dir)]
common_files = set(video_files) & set(annotation_files)
# Assert that the number of files in both directories are the same
assert len(common_files) == len(video_files) == len(annotation_files)
print("Done")