#!/bin/bash

# TimeWarp Data Generation Script
# Usage: ./generate_data.sh <path_to_processed_dir>

if [ $# -ne 1 ]; then
    echo "Usage: $0 <path_to_processed_dir>"
    echo "Example: $0 /data/processed"
    exit 1
fi

ROOT_DIR=$1

echo "Starting TimeWarp data generation..."
echo "Working directory: $ROOT_DIR"

# Generate preference data
echo "Step 1/6: Merging normal captions..."
python timewarp/pref_data/merge_normal_captions.py --root_dir "$ROOT_DIR"

echo "Step 2/6: Merging shuffled captions..."
python timewarp/pref_data/merge_shuffled_captions.py --root_dir "$ROOT_DIR"

echo "Step 3/6: Generating SFT data..."
python timewarp/pref_data/generate_sft_explicit.py --root_dir "$ROOT_DIR"

echo "Step 4/6: Generating preference data..."
python timewarp/pref_data/generate_pref_explicit.py --root_dir "$ROOT_DIR" \
    --shuffled_dir_name "shuffled" \
    --annotation_dir_name "shuffled_annotations" \
    --video_dir_name "shuffled_videos"

# Generate benchmarks
echo "Step 5/6: Generating normal benchmark..."
python timewarp/benchmark/generate_normal_benchmark.py --root_dir "$ROOT_DIR"

echo "Step 6/6: Generating shuffled benchmark..."
python timewarp/benchmark/generate_shuffled_benchmark.py --root_dir "$ROOT_DIR"

echo "Data generation complete!"
echo "Generated files:"
echo "  - temporal_sft_15k.json"
echo "  - temporal_pref_15k.json"
echo "  - timewar_normal_benchmark_15k.json"
echo "  - temporal_shuffled_benchmark.json"
