# 安装运行
1. (推荐)安装并配置[conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html)
    ```bash
    conda create -n MicroGPT python=3.9.16
    conda activate MicroGPT
    ```
2. 获取本仓库地库
    ```bash
    git clone https://github.com/yxq321/MicroGPT.git
    cd MicroGPT
    ```
3. 安装依赖包
    ```bash
    pip install -r requirements.txt
    ```
4. 下载大模型bin文件(可以从网上查找Llama2的bin文件), 以下是举例
    ```bash
    mkdir -p models/ && cd models/
    wget https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/resolve/main/llama-2-7b-chat.ggmlv3.q4_0.bin 
    ```
5. 配置大模型bin文件的路径
    ```bash
    vi setting.py # 根据实际路径，修改 model_file 变量
    ```
6. 运行程序
    ```bash
    streamlit run streamlit_app.py
    ```

# TODO LIST
- 流式输出
- Embedding模型下载
- 支持中文
- 是否支持mps / ngpu_layer
- 差一个requirements.txt
- 知识库问答不支持history