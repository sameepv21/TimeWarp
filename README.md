# Harnessing Synthetic Preference Data for Enhancing Temporal Understanding of Video-LLMs

![Pipeline Overview](img/pipeline.png)

This repository provides the dataset generation tools, pretrained checkpoints, and training code for TimeWarp - a framework for enhancing temporal understanding in Video-LLMs through synthetic preference data.

## 📋 Status

- ✅ TimeWarp data generation scripts released
- ⏳ Checkpoints for LLaVA-Hound and Video-LLaMA3 (coming soon)
- ⏳ Training, evaluation, and inference code (coming soon)
- ⏳ Official citation and links (coming soon)

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Required packages: `pandas`, `tqdm`, `opencv-python`, `moviepy`, `openai`

### Dataset Setup

#### Option 1: Download Preprocessed Data
Download the preprocessed frames directly from [LINK] (coming soon)

#### Option 2: Generate from Scratch

1. **Download FineVideo Dataset**
   ```bash
   # Download from HuggingFace
   # https://huggingface.co/HuggingFaceFV/finevideo
   ```

2. **Run Preprocessing Pipeline**
   ```bash
   # Make scripts executable
   chmod +x setup_dataset.sh generate_data.sh
   
   # Run preprocessing (creates normal and shuffled videos)
   ./setup_dataset.sh path/to/finevideo path/to/output 5000
   
   # Generate preference data and benchmarks
   ./generate_data.sh path/to/output
   ```

### Manual Commands (Alternative)

If you prefer to run commands individually:

**Preprocessing:**
```bash
python timewarp/preprocess/preprocess.py --root_dir <finevideo_path> --save_dir <output_path> --scale 5000
python timewarp/preprocess/filter_corrupted.py --root_dir <output_path>
python timewarp/preprocess/final_assertions.py --root_dir <output_path>
python timewarp/preprocess/shuffle_clips.py --root_dir <output_path>
```

**Data Generation:**
```bash
python timewarp/pref_data/merge_normal_captions.py --root_dir <output_path>
python timewarp/pref_data/merge_shuffled_captions.py --root_dir <output_path>
python timewarp/pref_data/generate_sft_explicit.py --root_dir <output_path>
python timewarp/pref_data/generate_pref_explicit.py --root_dir <output_path> \
    --shuffled_dir_name shuffled \
    --annotation_dir_name shuffled_annotations \
    --video_dir_name shuffled_videos
python timewarp/benchmark/generate_normal_benchmark.py --root_dir <output_path>
python timewarp/benchmark/generate_shuffled_benchmark.py --root_dir <output_path>
```

## 📊 Model Checkpoints

| Method | LLaVA-Hound | Video-LLaMA3 | InternVideo |
|--------|-------------|--------------|-------------|
| SFT | [Coming Soon](#) | [Coming Soon](#) | [Coming Soon](#) |
| Base-DPO | [Coming Soon](#) | [Coming Soon](#) | [Coming Soon](#) |
| Combined (ours) | [Coming Soon](#) | [Coming Soon](#) | [Coming Soon](#) |
| TimeWarp-Implicit | [Coming Soon](#) | [Coming Soon](#) | [Coming Soon](#) |
| TimeWarp-Explicit | [Coming Soon](#) | [Coming Soon](#) | [Coming Soon](#) |

## 📁 Repository Structure

```
TimeWarp/
├── setup_dataset.sh      # Preprocessing pipeline
├── generate_data.sh       # Data generation pipeline
└── timewarp/
    ├── preprocess/        # Video preprocessing scripts
    ├── pref_data/         # Preference data generation
    └── benchmark/         # Benchmark generation
```

## 📚 Citation

If you find TimeWarp useful, please cite:

```bibtex
@article{timewarp2024,
    title={TimeWarp: Enhancing Temporal Understanding of Video-LLMs},
    author={Author names},
    journal={Conference/Journal},
    year={2024}
}
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.