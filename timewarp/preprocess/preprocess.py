import pandas as pd
import json
from tqdm import tqdm
import os
from pprint import pprint
import random
from moviepy.editor import VideoFileClip, concatenate_videoclips
import time
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root_dir', type=str, required=True, help='Path to finevideo dataset')
    parser.add_argument("--save_dir", type=str, required=True, help='Path to save the preprocessed videos and annotations')
    parser.add_argument("--scale", type=int, required=True, help='Number of finevideo videos to be taken') # For the purpose os paper, this was chosen to be 15k but can be scaled to any number
    return parser.parse_args()

args = parse_args()

TOTAL_VIDEOS = 0
START_SECONDS = 0.0

video_dir = os.path.join(args.root_dir, "data")
save_annotation_dir = os.path.join(args.save_dir, "normal_annotations")
save_video_dir = os.path.join(args.save_dir, 'normal_videos')
parquet_files = os.listdir(video_dir)
random.seed(42)

selected_parquet_files = []

def convert_timestamp_to_seconds(timestamp):
    h, m, s = timestamp.split(':')
    h = int(h)
    m = int(m)
    s = int(s.split(".")[0])
    ms = int(timestamp.split('.')[-1])
    return h * 3600 + m * 60 + s + ms / 1000

for filename in parquet_files:
    # Ensures that total number of videos as given
    if TOTAL_VIDEOS >= args.scale:
        break

    # Add in selected parquet files
    selected_parquet_files.append(filename)

    # Read entire dataframe
    df = pd.read_parquet(os.path.join(video_dir, filename))

    # For each "video"
    for _, row in tqdm(df.iterrows()):
        flag = False # Checker

        # Increament the number of videos
        TOTAL_VIDEOS += 1

        # Annotation of each video
        json_data = row['json']

        # mp4 / video
        mp4 = row['mp4']
        
        # Save the original "video"
        with open(os.path.join(args.root_dir, 'temp.mp4'), 'wb') as f:
            f.write(mp4)

        # Read the og. video using moviepy
        original_video = VideoFileClip(os.path.join(os.path.join(args.root_dir, 'temp.mp4')), audio=False)
        
        # Video and json filename
        video_id = json_data["original_video_filename"]
        annotation_filename = json_data['original_json_filename']

        # Get all the scenes / clips
        scenes = json_data['content_metadata']['scenes']

        # Create a new json for each video
        new_json_data = {
            "video": video_id,
            "annotation_filename": annotation_filename,
            'description': [],
            'scene_timestamps': [],
        }

        final_end_seconds = -1

        # For each "scene"
        for scene in scenes:
            # Get the activities
            activities = scene['activities']
            
            # Define descriptions
            descriptions = ""

            # Only activity descriptions with 
            if len(activities) > 0:
                # Get the start and end seconds
                clip_st = activities[0]['timestamp']['start_timestamp']
                clip_et = activities[-1]['timestamp']['end_timestamp']

                try:
                    end_seconds = convert_timestamp_to_seconds(clip_et)
                    start_seconds = convert_timestamp_to_seconds(clip_st)
                except Exception as err:
                    flag = True
                    break

                if start_seconds < end_seconds:
                    if end_seconds <= 105:
                        # For each activity in a scene
                        for activity in activities:
                            descriptions += activity['description']
                            descriptions += " "

                        # Get the start and end seconds of each scene
                        new_json_data['scene_timestamps'].append([start_seconds, end_seconds])
                        final_end_seconds = end_seconds
                    else:
                        # Bigger videos handling
                        print("\n\nEnd Seconds ", end_seconds)
                        break
                    
                    # Concatenate and append the description
                    new_json_data['description'].append(descriptions)
        
        # Assertions for error handling
        assert len(new_json_data['description']) == len(new_json_data['scene_timestamps'])

        # Generate and save the trimmed video
        if final_end_seconds < -1:
            flag = True
        final_video = original_video.subclip(START_SECONDS, final_end_seconds)

        # print("\n\n")
        # print("duration of the final video", final_video.duration)
        # pprint(new_json_data)
        # print("\n\n")

        if flag or len(new_json_data['scene_timestamps']) < 2: # Ensures that there are multiple events and scenes in the video.
            TOTAL_VIDEOS -= 1
            continue

        # assert statements
        assert final_video.duration >= new_json_data['scene_timestamps'][-1][1]
        final_video.write_videofile(os.path.join(save_video_dir, video_id), codec='libx264', audio=False)
        
        # Save the annotation directory
        with open(os.path.join(save_annotation_dir, f"{annotation_filename}"), 'w') as json_file:
            json.dump(new_json_data, json_file)

        time.sleep(0.5) # Give some slack for clearing the cache and releasing the file pointers.
        # break
    # break

with open('finevideo_subset.txt', 'w') as f:
    for item in selected_parquet_files:
        f.write("%s\n" % item)