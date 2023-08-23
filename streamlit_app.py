import streamlit as st
import os

from settings import data_file, model_file, is_apple_silicon

if not os.path.isfile(model_file):
    st.error(f"ERROR: 模型文件: `{model_file}` 不存在，请从网上下载.")
    print(
        f"ERROR: model file: `{model_file}` does NOT exist, please download it from internet (like huggingface)."
    )
    st.stop()


from llm import kb_llm, ask_llm

from langchain.callbacks.base import BaseCallbackHandler  # 实现流式输出


class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        # "/" is a marker to show difference
        # you don't need it
        self.text += token
        self.container.markdown(self.text)


# App title
st.set_page_config(page_title="My local Chatbot")


with open(data_file, "r") as file:
    file_content = file.read()


def clear_chat_history():
    st.session_state.messages = [
        {"role": "assistant", "content": "How may I assist you today?"}
    ]


with st.sidebar:
    st.title("My local Chatbot")
    run_model = st.radio("请选择运行的模式:", ["机器人聊天", "知识库"])
    if run_model == "知识库":
        st.text_area(
            "建议根据下列已入库的内容提问:",
            value=file_content,
            disabled=True,
        )
        st.info(body="e.g: How many kids does Hongxing Shu have?")
        # clear_chat_history()
    st.button("Clear Chat History", on_click=clear_chat_history)
    st.divider()
    st.markdown(
        f"""### 注意
* 中文支持不太好
* 暂不支持流输出(不支持一个字一个字出)(待开发)
### 配置
* 模型文件: `{model_file}`
* 知识库文件: `{data_file}`
"""
    )

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "How may I assist you today?"}
    ]


# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        chat_box = st.empty()
    stream_handler = StreamHandler(chat_box)


# Refactored from https://github.com/a16z-infra/llama2-chatbot
def generate_llama2_response(prompt_input):
    string_dialogue = ""
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
    if run_model == "知识库":
        output = kb_llm(prompt_input)
    else:
        output = ask_llm(
            stream_handler, prompt=prompt_input, string_dialogue=string_dialogue
        )
        # output = ask_llm(prompt=prompt_input, string_dialogue=string_dialogue)
    return output


# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.spinner("Generating..."):
        full_response = generate_llama2_response(prompt)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)
    st.experimental_rerun()  # 重绘
