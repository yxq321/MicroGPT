"""
本文件基于Llama大模型，主要有两个函数:

- 聊天函数

- 知识库函数
"""

from langchain.llms import LlamaCpp

# from langchain.embeddings import LlamaCppEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.document_loaders import TextLoader

# from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma

from settings import model_file, data_file, is_apple_silicon

from langchain.embeddings import HuggingFaceInstructEmbeddings


EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
embeddings = HuggingFaceInstructEmbeddings(  # embeddings = LlamaCppEmbeddings(model_path="../llama.cpp/models/llama-2-7b-chat.ggmlv3.q4_0.bin")
    model_name=EMBEDDING_MODEL_NAME,
    model_kwargs={"device": "mps" if is_apple_silicon else "cpu"},
)

llm = LlamaCpp(
    model_path=model_file,
    n_ctx=2048,
    n_batch=128,
    n_gpu_layers=1 if is_apple_silicon else 0,
    streaming=True,
)

# 另一种方式
# from llama_cpp import Llama
# llm = Llama(
#    model_path=model_file,
#    n_ctx=512,
#    n_batch=128,
#    n_gpu_layers=1,
# )

from langchain.text_splitter import RecursiveCharacterTextSplitter

loader = TextLoader(data_file)
docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=0)
texts = text_splitter.split_documents(docs)
db = Chroma.from_documents(texts, embeddings)

# set prompt template
prompt_msg = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.
{context}
Question: {question}
Answer:"""
prompt_tpl = PromptTemplate(
    template=prompt_msg, input_variables=["context", "question"]
)


def kb_llm(p: str) -> str:
    """
    Llama-KB问答

    Examples:
        >>> kb_llm("Who is hongxing")

    Args:
        p: 提示词.

    Returns:
        大模型生成的回复(结合KB库)
    """
    similar_doc = db.similarity_search(p, k=1)
    context = similar_doc[0].page_content

    prompt = f"{prompt_tpl.format(context=context, question=p)}"
    print(prompt)

    query_llm = LLMChain(
        llm=llm,
        prompt=prompt_tpl,
    )
    response = query_llm.run({"context": context, "question": p})
    return response


def ask_llm(
    stream_handler,
    prompt: str = "Hello.",
    string_dialogue: str = "",
) -> str:
    """
    单纯机器人问答.

    Args:
        stream_heandler: 流输出对象.
        prompt: 提示词.
        string)dialogue: 历史纪录.

    Returns:
        生成的LLM回答.
    """
    msg = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'.Assistant: How may I assist you today?\n\n"
    msg += string_dialogue
    msg += prompt
    msg += "\n\nAssistant:"
    print(f"prompt: {msg}")
    response = llm(
        msg,
        max_tokens=-1,
        echo=False,
        temperature=0.1,
        top_p=0.9,
        callbacks=[stream_handler],
    )
    print(f"output: {response}")
    # return output["choices"][0]["text"] # no langchain
    return response  # with langchain


if __name__ == "__main__":
    p = "what does Hongxing Shu like?"
    print(kb_llm(p))
