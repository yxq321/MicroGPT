# MicroGPT

中文版请点击 [这里](README.md).

## Screenshots
- Chatbot mode
    ![av](res/chatbot.png)

- Knowledge mode
    ![avatar](res/kb.png)

# Installation
1. (recommend)Firstly please install [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html), then create Python enviorment.
    ```bash
    conda create -n MicroGPT python=3.11
    conda activate MicroGPT
    ```
2. Clone this git repos:
    ```bash
    git clone https://github.com/yxq321/MicroGPT.git
    cd MicroGPT
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Download and configure LLM model file.
    1. Download Llama2 bin file(gguf format) (mostly you can get it from Huggingface).
    2. Configure the path of your llama2 bin file.
        ```bash
        vi setting.py # change model_file based on your file location.
        ```
5. Run the program:
    ```bash
    streamlit run streamlit_app.py
    # 或指定端口
    # streamlit run streamlit_app.py --server.port=8088 
    ```
6. (opt)Configure supervisor to manage it:
   ```bash
   sudo cp supervisor_microgpt.conf /etc/supervisor/conf.d/microgpt.conf
   sudo vi /etc/supervisor/conf.d/microgpt.conf # change the file based on your env.
   systemctl restart supervisor
   ```

# Contacts

Welcomed to report any bug:

- Email: yxq321(at)gmail.com
