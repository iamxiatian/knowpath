import json

import requests


class Chatbot:
    """对话机器人，与LLM进行对话，提交Prompt，返回结果。

    Examples:

        .. code-block:: python

        from knowpath.llm import Chatbot
        chatbot = Chatbot("http://localhost:1119/v1",
                            model="./Qwen2.5-7B-Instruct")
        response = chatbot.complete("hello")
        print(resposne)

    """

    def __init__(self, base_url: str, model: str):
        """Initialize the chatbot.

        Args:
            completion_url (str): The service url for LLM completions.
                Defaults to None.
            chat_url (str): The service url for LLM chats.
            model (str): model name
        """
        self.completion_url = f"{base_url}/completions"
        self.chat_url = f"{base_url}/chat/completions"
        self.model = model

    def complete(
        self,
        prompt: str,
        temperature: float = 0,
        n_choices: int = 1,
        use_beam_search=False,
        max_tokens: int = 256,
        skip_special_tokens: bool = True,
    ) -> str:
        """根据输入的提示，继续续写内容。

        续写和chat不同，例如输入“你好”，对于续写来说，会接着续写出“，我是小明……”，
        而对于chat，则可能是“你好，我们来聊天吧。”

        Args:
            n_choices (int): number of return candidates.
                Defaults to 1.
        """
        payload = json.dumps(
            {
                "model": self.model,
                "prompt": [prompt],
                "n": n_choices,
                "best_of": n_choices,
                "use_beam_search": use_beam_search,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "skip_special_tokens": skip_special_tokens,
            }
        )
        headers = {"Content-Type": "application/json"}

        response = requests.request(
            "POST", self.completion_url, headers=headers, data=payload
        )

        return response.text

    def chat(
        self,
        system_prompt: str = "You are a helpful assistant.",
        user_prompt: str = "Hello!",
        temperature: float = 0,
        n_choices: int = 1,
        top_p: float = 0.8,
        repetition_penalty: float = 1.05,
        max_tokens: int = 256,
        skip_special_tokens: bool = True,
    ) -> str:
        """以对话方式与LLM进行交互。

        Args:
            n_choices (int): number of return candidates.
                Defaults to 1.
        """
        use_beam_search = n_choices > 1
        payload = json.dumps(
            {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    },
                ],
                "temperature": temperature,
                "top_p": top_p,
                "n": n_choices,
                "best_of": n_choices,
                "use_beam_search": use_beam_search,
                "repetition_penalty": repetition_penalty,
                "max_tokens": max_tokens,
                "skip_special_tokens": skip_special_tokens,
            }
        )
        headers = {"Content-Type": "application/json"}
        response = requests.request(
            "POST", self.chat_url, headers=headers, data=payload
        )
        return response.text
