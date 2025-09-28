#!/bin/bash

# TimeWarp Dataset Preprocessing Script
# Usage: ./setup_dataset.sh <path_to_finevideo_data> <path_to_save_dir> <scale>

if [ $# -ne 3 ]; then
    echo "Usage: $0 <path_to_finevideo_data> <path_to_save_dir> <scale>"
    echo "Example: $0 /data/finevideo /data/processed 5000"
    exit 1
fi

ROOT_DIR=$1
SAVE_DIR=$2
SCALE=$3

echo "Starting TimeWarp dataset preprocessing..."
echo "Input directory: $ROOT_DIR"
echo "Output directory: $SAVE_DIR"
echo "Scale: $SCALE videos"

# Step 1: Preprocess videos
echo "Step 1/4: Preprocessing videos..."
python timewarp/preprocess/preprocess.py --root_dir "$ROOT_DIR" --save_dir "$SAVE_DIR" --scale "$SCALE"

# Step 2: Filter corrupted files
echo "Step 2/4: Filtering corrupted videos..."
python timewarp/preprocess/filter_corrupted.py --root_dir "$SAVE_DIR"

# Step 3: Final assertions
echo "Step 3/4: Running final assertions..."
python timewarp/preprocess/final_assertions.py --root_dir "$SAVE_DIR"

# Step 4: Shuffle clips
echo "Step 4/4: Creating shuffled clips..."
python timewarp/preprocess/shuffle_clips.py --root_dir "$SAVE_DIR"

echo "Preprocessing complete!"
