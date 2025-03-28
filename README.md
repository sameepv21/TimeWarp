# Harnessing Synthetic Preference Data for Enhancing Temporal Understanding of Video-LLMs

![Teaser Image](img/pipeline.png)

This repository will provide access to the dataset, pretrained checkpoints, inference, and the training code for our paper, TimeWarp. We provide our training scripts with modified versions taking from [LLaVA-Hound](https://github.com/RifleZhang/LLaVA-Hound-DPO) as the backbone for easy reproducibility.

# TODOs:
- [x] Release timewarp data generation script
- [ ] Release checkpoints for LLaVA-Hound and Video-LLaMA3
- [ ] Release training, evaluation, and inference code
- [ ] Replace citation and links with the original one

# Dataset
> You can directly download the raw frames used for finetuning at LINK or follow the below steps to set it up from scratch
* Download the raw FineVideo Dataset from [HuggingFaceFV/FineVideo](https://huggingface.co/HuggingFaceFV/finevideo)
* Once downloaded, run the below commands to preprocess the dataset.
```bash
python timewarp/preprocess/preprocess.py --root_dir path_to_finevideo_data --save_dir path_to_saving_videos --scale 5k

python timewarp/preprocess/filter_corrupted.py --root_dir path_to_saved_root_dir

python timewarp/preprocess/final_assertions.py --root_dir path_to_saved_root_dir

python timewarp/preprocess/shuffle_clips.py --root_dir path_to_saved_root_dir
```
* After preprocessing, below commands will generate question answering pairs for preference data and MCQs for the benchmark (TimeWar).
```bash
python timewarp/pref_data/merge_normal_captions.py --root_dir path_to_saved_root_dir

python timewarp/pref_data/merge_shuffled_captions.py --root_dir path_to_saved_root_dir

python timewarp/pref_data/generate_sft_explicit.py --root_dir path_to_saved_root_dir

python timewarp/pref_data/generate_pref_explicit.py --root_dir path_to_saved_root_dir

python timewarp/benchmark/generate_normal_benchmark.py --root_dir path_to_saved_root_dir

python timewarp/benchmark/generate_shuffled_benchmark.py --root_dir path_to_saved_root_dir
```


# Checkpoints

| Methods                     | LLaVA-Hound | Video-LLaMA3 | InternVideo |
|-----------------------------|-------------|--------------| ----------- |
| SFT                         | [Link](#)   | [Link](#)    | [Link](#)   |
| Base-DPO                    | [Link](#)   | [Link](#)    | [Link](#)   |
| Combined (ours)             | [Link](#)   | [Link](#)    | [Link](#)   |
| TimeWarp-Implicit (ours)    | [Link](#)   | [Link](#)    | [Link](#)   |
| TimeWarp-Explicit (ours)    | [Link](#)   | [Link](#)    | [Link](#)   |

# Citing
If you find TimeWarp useful, consider citing:

```bibtex
@article{patel2024tripletclip,
    author = {Patel, Maitreya and Kusumba, Abhiram and Cheng, Sheng and Kim, Changhoon and Gokhale, Tejas and Baral, Chitta and Yang, Yezhou},
    title = {TripletCLIP: Improving Compositional Reasoning of CLIP via Synthetic Vision-Language Negatives},
    journal={Advances in neural information processing systems},
    year = {2024},
}
```