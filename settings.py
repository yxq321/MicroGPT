"""
配置文件
"""

# 存放数据信息的文件，只验证过:
# 1. 英文
# 2. 文本文件
data_file = "data/file.txt"

# 可以从huggingface下载GGUF格式的模型文件(GGML不再支持了)
# 例如:  https://huggingface.co/rozek/LLaMA-2-7B-32K_GGUF/tree/main (找到里面的 Files and Versions)
model_file = "../llama.cpp/models/Llama2-Chinese-7b-Chat-gguf-model-q4_0.bin"


# 大模型文件可以通过这里下载: https://huggingface.co/Xorbits/chatglm2-6B-GGML/tree/main
chatglm_model_file = "../llama.cpp/models/chatglm2-ggml-q4_0.bin"


# 如果是苹果 M1(*) / M2(*) 等CPU，请配置 True
is_apple_silicon = False
