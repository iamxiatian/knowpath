from abc import ABC
from typing import Any, List, Mapping, Optional

import torch
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.models.qwen2.modeling_qwen2 import Qwen2ForCausalLM
from transformers.models.qwen2.tokenization_qwen2_fast import (
    Qwen2TokenizerFast,
)

model_name = "/root/xiatian/models/Qwen2.5-7B-Instruct"

model: Qwen2ForCausalLM = AutoModelForCausalLM.from_pretrained(
    model_name, torch_dtype="auto", device_map="cpu"
)

tokenizer: Qwen2TokenizerFast = AutoTokenizer.from_pretrained(model_name)
device = torch.device("cuda:0")
model = model.to(device)


class Qwen(LLM, ABC):
    max_token: int = 10000
    temperature: float = 0.7
    top_p: float = 0.9
    history_len: int = 3

    def __init__(self):
        super().__init__()

    @property
    def _llm_type(self) -> str:
        return "Qwen"

    @property
    def _history_len(self) -> int:
        return self.history_len

    def set_history_len(self, history_len: int = 10) -> None:
        self.history_len = history_len

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
    ) -> str:
        messages = [
            {"role": "system", "content": "你是知路助手！"},
            {"role": "user", "content": prompt},
        ]

        text: str = tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        model_inputs = tokenizer(
            [text], return_tensors="pt", max_length=512, truncation=True
        ).to(model.device)
        generated_ids = model.generate(**model_inputs, max_new_tokens=512)
        # 生成的id删除前面和输入相同的id
        generated_ids = [
            output_ids[len(input_ids) :]
            for input_ids, output_ids in zip(
                model_inputs.input_ids, generated_ids
            )
        ]
        generated_texts = tokenizer.batch_decode(
            generated_ids, skip_special_tokens=True
        )
        return generated_texts[0]

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        return {
            "max_token": self.max_token,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "history_len": self.history_len,
        }


if __name__ == "__main__":
    import torch

    torch.cuda.is_available()
    device = torch.device("cuda:0")
    x = torch.FloatTensor([1, 2])
    x.to(device)
    print(x)
