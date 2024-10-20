from langchain.vectorstores import FAISS


class FAISSWrapper(FAISS):
    chunk_size: int = 250

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
