from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import numpy as np
from langchain.vectorstores import FAISS
from langchain_core.documents import Document


class FAISSWrapper(FAISS):
    chunk_size: int = 250
    chunk_content: bool = True
    score_threshold: float = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def asimilarity_search_with_score_by_vector(
        self,
        embedding: List[float],
        k: int = 4,
        filter: Optional[Union[Callable, Dict[str, Any]]] = None,
        fetch_k: int = 20,
        **kwargs: Any,
    ) -> List[Tuple[Document, float]]:
        if filter:
            embedding = [e for e, f in zip(embedding, filter) if f]

        if fetch_k is not None:
            k = fetch_k

        scores, indices = self.index.search(
            np.array([embedding], dtype=np.float32), k
        )

        docs = []
        id_set = set()
        store_len = len(self.index_to_docstore_id)
        for j, i in enumerate(indices[0]):
            # 如果索引无效或者得分低于阈值，则忽略
            if i == -1 or 0 < self.score_threshold < scores[0][j]:
                continue
            _id = self.index_to_docstore_id[i]
            doc = self.docstore.search(_id)
            if not self.chunk_content:
                if not isinstance(doc, Document):
                    raise ValueError(
                        f"Could not find document for id {_id}, got {doc}"
                    )
                doc.metadata["score"] = int(scores[0][j])
                docs.append(doc)
                continue
            id_set.add(i)
            docs_len = len(doc.page_content)
