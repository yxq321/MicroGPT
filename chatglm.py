import chatglm_cpp

from settings import chatglm_model_file

from typing import Union

pipeline = chatglm_cpp.Pipeline(chatglm_model_file)

generation_kwargs = dict(
    max_length=2048,
    do_sample=True,
    top_p=0.7,
    temperature=0.95,
    num_threads=0,
    stream=True,
)


def chatglm_llm(prompt: Union[str, list]):
    """
    根据提示词生成内容
    返回值: 是个generator对象
    """
    if isinstance(prompt, list):
        history = get_history(prompt)
    else:
        history = [prompt]  # 转成列表

    gen = pipeline.chat(history, **generation_kwargs)
    # response = ""
    # for token in gen:
    #     # print("a")
    #     response += token
    #     print(token, end="", flush=True)
    #     # print(response)
    return gen


def get_history(prompt: list) -> list:
    """
    拼装成chatGLM的格式
    """
    history = []
    for item in prompt[1:]:  #
        history.append(item["content"])
    return history


# generator = (
#     pipeline.chat(history, **generation_kwargs)
#     if args.mode == "chat"
#     else pipeline.generate(input, **generation_kwargs)
# )

if __name__ == "__main__":
    for token in chatglm_llm("请介绍一下三国的刘备。"):
        print(token, end="", flush=True)
