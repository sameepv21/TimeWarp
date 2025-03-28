import json
import cv2
import os
import numpy as np
from tqdm import tqdm
from moviepy.editor import VideoFileClip, concatenate_videoclips
import time
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root_dir', type=str, required=True, help='Root directory')
    return parser.parse_args()

args = parse_args()

# Set random seed
np.random.seed(42)
video_dir = os.path.join(args.root_dir, "normal_videos")
annotation_dir = os.path.join(args.root_dir, "normal_annotations")

for filename in tqdm(sorted(os.listdir(video_dir))):
    id = filename.replace(".mp4", "")
    # id = "-KwARMxsvFw" # Debug
    # filename = "-KwARMxsvFw.mp4"
    annotation_filename = id + ".json"

    with open(os.path.join(annotation_dir, annotation_filename), "r") as f:
        data = json.loads(f.read())

    scene_timestamps = data.get("scene_timestamps", [])
    descriptions = data.get("description", [])

    flag = False
    
    if len(scene_timestamps) > 1:
        # Combine scene_timestamps and descriptions into a list of tuples
        timestamp_description_pairs = list(zip(scene_timestamps, descriptions))
        
        # Shuffle the list of tuples
        np.random.shuffle(timestamp_description_pairs)
        
        # Ensure the order is actually shuffled
        while timestamp_description_pairs == list(zip(scene_timestamps, descriptions)):
            np.random.shuffle(timestamp_description_pairs)
        
        # Separate the shuffled scene_timestamps and descriptions
        shuffled_scene_timestamps, shuffled_descriptions = zip(*timestamp_description_pairs)
        
        data["scene_timestamps"] = list(shuffled_scene_timestamps)
        data["description"] = list(shuffled_descriptions)

    # Save the shuffled data to a new JSON file
    with open(os.path.join(args.root_dir, "shuffled_annotations", annotation_filename), "w") as f:
        json.dump(data, f)

    # Load the video
    original_video = VideoFileClip(os.path.join(video_dir, filename), audio=False)
    
    # Shuffle the clips
    clips = data['scene_timestamps']
    segments = []

    try:
        for start_seconds, end_seconds in clips:
            if start_seconds < end_seconds:
                segment = original_video.subclip(start_seconds, end_seconds)
                segments.append(segment)
        shuffled_video = concatenate_videoclips(segments)
        shuffled_video.write_videofile(os.path.join(args.root_dir, "shuffled_videos", filename), codec='mpeg4', audio=False)
    except Exception as e:
        # Save the errorneous videos
        with open("shuffle_error_log.txt", "a") as error_log:
            error_log.write(filename + "\n")
    time.sleep(0.5)