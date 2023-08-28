# copied from https://gist.github.com/mortymike/70711b028311681e5f3c6511031d5d43
# 解决streaming output的问题，使用generator 来替代 callback

from threading import Thread
from queue import Queue, Empty
from threading import Thread
from collections.abc import Generator
from langchain.llms import OpenAI
from langchain.callbacks.base import BaseCallbackHandler


# Defined a QueueCallback, which takes as a Queue object during initialization. Each new token is pushed to the queue.
class QueueCallback(BaseCallbackHandler):
    """Callback handler for streaming LLM responses to a queue."""

    def __init__(self, q):
        self.q = q

    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        self.q.put(token)

    def on_llm_end(self, *args, **kwargs: Any) -> None:
        return self.q.empty()


# Create a function that will return our generator
def stream(input_text) -> Generator:
    # Create a Queue
    q = Queue()
    job_done = object()

    # Initialize the LLM we'll be using
    llm = OpenAI(streaming=True, callbacks=[QueueCallback(q)], temperature=0)

    # Create a funciton to call - this will run in a thread
    def task():
        resp = llm(input_text)
        q.put(job_done)

    # Create a thread and start the function
    t = Thread(target=task)
    t.start()

    content = ""

    # Get each new token from the queue and yield for our generator
    while True:
        try:
            next_token = q.get(True, timeout=1)
            if next_token is job_done:
                break
            content += next_token
            yield next_token, content
        except Empty:
            continue


if __name__ == "__main__":
    for next_token, content in stream("How cool are LLMs?"):
        print(next_token)
        print(content)
