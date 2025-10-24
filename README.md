# TimeWarp: Harnessing Synthetic Preference Data for Enhancing Temporal Understanding of Video-LLMs

<div align="center">

[![arXiv](https://img.shields.io/badge/arXiv-2024.XXXXX-b31b1b.svg?style=flat-square)](https://arxiv.org/abs/2024.XXXXX)
[![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Models-blue?style=flat-square)](https://huggingface.co/time-warp)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)

![Pipeline Overview](img/pipeline.png)

</div>

A framework for enhancing temporal understanding in Video-LLMs through synthetic preference data generation and training.


## 🚀 Installation

```bash
git clone https://github.com/yourusername/TimeWarp.git
cd TimeWarp
pip install -r requirements.txt
```

## 📦 Dataset Setup

### Option 1: Download Preprocessed Data
[![Hugging Face Dataset](https://img.shields.io/badge/%F0%9F%A4%97%20Dataset-TimeWarp-orange?style=flat-square)](https://huggingface.co/datasets/time-warp/timewarp-data)

### Option 2: Generate from Scratch

1. Download the [FineVideo Dataset](https://huggingface.co/HuggingFaceFV/finevideo)
2. Run the preprocessing pipeline:
   ```bash
   chmod +x scripts/*.sh
   ./scripts/setup_dataset.sh path/to/finevideo path/to/output 5000
   ./scripts/generate_data.sh path/to/output
   ```

## 🎯 Training & Evaluation

### Training
Refer to `dpo_scripts/train_dpo.sh` for DPO training configurations.

### Evaluation
Evaluation scripts are available in the `test/` directory for various benchmarks including MVBench, TempCompass, and our TimeWarp benchmarks.

## 📁 Project Structure

```
TimeWarp/
├── 📂 timewarp/           # Core data generation modules
│   ├── preprocess/        # Video preprocessing
│   ├── pref_data/         # Preference data generation
│   └── benchmark/         # Benchmark creation
├── 📂 dpo_scripts/        # DPO training scripts
├── 📂 llava/              # Model implementations
├── 📂 test/               # Evaluation pipelines
├── 📂 inference/          # Inference utilities
└── 📂 scripts/            # Setup and generation scripts
```

## 📚 Citation

If you find our work helpful, please consider citing:

```bibtex
@misc{vani2025harnessingsyntheticpreferencedata,
      title={Harnessing Synthetic Preference Data for Enhancing Temporal Understanding of Video-LLMs}, 
      author={Sameep Vani and Shreyas Jena and Maitreya Patel and Chitta Baral and Somak Aditya and Yezhou Yang},
      year={2025},
      eprint={2510.03955},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2510.03955}, 
}
```

## 🤝 Contributing

We welcome contributions! Please feel free to submit pull requests or open issues for bug reports and potential issues.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

We thank the authors of LLaVA-Hound, Video-LLaMA3, and FineVideo for their foundational work.
