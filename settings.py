"""
配置文件
"""

# 存放数据信息的文件，只验证过:
# 1. 英文
# 2. 文本文件
data_file = "data/file.txt"

# 可以从huggingface下载模型文件
# 例如: https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML (找到里面的 Files and Versions)
model_file = "../llama.cpp/models/Llama2-Chinese-7b-Chat-ggml-model-q4_0.bin"

# 如果是苹果 M1(*) / M2(*) 等CPU，请配置 True
is_apple_silicon = True
