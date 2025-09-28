output_model_name=videollama3-lhdpo
model_path=DAMO-NLP-SG/VideoLLaMA3-7B
model_base="None"
load_peft=./experiments/videollama3_lp_lhdpo

data_name=perceptiontest
TEST_DATA_DIR=./datasets/perceptiontest
TEST_RESULT_DIR=./evaluation/${data_name}/${output_model_name}

data_path=$TEST_DATA_DIR/llava_hound_valid.json
output_path=$TEST_RESULT_DIR/perceptiontest/inference_test_official

cache_dir=~/.cache
VIDEO_DATA_DIR=./datasets/perceptiontest/frames

bash test/inference/inference_test_qa.sh \
$data_path \
$output_path/${output_model_name} \
$model_path \
$model_base \
$load_peft \
$cache_dir \
$VIDEO_DATA_DIR

bash test/eval/eval_official_zeroshot_qa.sh $output_path/${output_model_name}.jsonl ${TEST_RESULT_DIR}/${data_name}/eval_test_official