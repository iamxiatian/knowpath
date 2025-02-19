import os
import re
from typing import List

from langchain.docstore.document import Document
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter


class ChineseTextSplitter(CharacterTextSplitter):
    def __init__(self, pdf: bool = False, **kwargs):
        super().__init__(**kwargs)
        self.pdf = pdf

    def split_text(self, text: str) -> List[str]:
        """文本切分，来自于：https://github.com/netease-youdao/QAnything/blob/974f9337f9b9c56c12005b86fe9409dc86c9b520/qanything_kernel/utils/splitter/chinese_text_splitter.py"""
        if self.pdf:
            text = re.sub(r"\n{3,}", r"\n", text)
            text = re.sub("\s", " ", text)
            text = re.sub("\n\n", "", text)

        text = re.sub(
            r"([;；.!?。！？\?])([^”’])", r"\1\n\2", text
        )  # 单字符断句符
        text = re.sub(r'(\.{6})([^"’”」』])', r"\1\n\2", text)  # 英文省略号
        text = re.sub(r'(\…{2})([^"’”」』])', r"\1\n\2", text)  # 中文省略号
        text = re.sub(
            r'([;；!?。！？\?]["’”」』]{0,2})([^;；!?，。！？\?])',
            r"\1\n\2",
            text,
        )
        # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
        text = text.rstrip()  # 段尾如果有多余的\n就去掉它
        # 很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
        ls = [i for i in text.split("\n") if i]
        for ele in ls:
            if len(ele) > self.sentence_size:
                ele1 = re.sub(
                    r'([,，.]["’”」』]{0,2})([^,，.])', r"\1\n\2", ele
                )
                ele1_ls = ele1.split("\n")
                for ele_ele1 in ele1_ls:
                    if len(ele_ele1) > self.sentence_size:
                        ele_ele2 = re.sub(
                            r'([\n]{1,}| {2,}["’”」』]{0,2})([^\s])',
                            r"\1\n\2",
                            ele_ele1,
                        )
                        ele2_ls = ele_ele2.split("\n")
                        for ele_ele2 in ele2_ls:
                            if len(ele_ele2) > self.sentence_size:
                                ele_ele3 = re.sub(
                                    '( ["’”」』]{0,2})([^ ])',
                                    r"\1\n\2",
                                    ele_ele2,
                                )
                                ele2_id = ele2_ls.index(ele_ele2)
                                ele2_ls = (
                                    ele2_ls[:ele2_id]
                                    + [i for i in ele_ele3.split("\n") if i]
                                    + ele2_ls[ele2_id + 1 :]
                                )
                        ele_id = ele1_ls.index(ele_ele1)
                        ele1_ls = (
                            ele1_ls[:ele_id]
                            + [i for i in ele2_ls if i]
                            + ele1_ls[ele_id + 1 :]
                        )

                id = ls.index(ele)
                ls = ls[:id] + [i for i in ele1_ls if i] + ls[id + 1 :]
        return ls

    def load_file(filepath) -> List[Document]:
        loader = TextLoader(filepath, autodetect_encoding=True)
        splitter = ChineseTextSplitter(pdf=False)
        docs = loader.load_and_split(splitter)
        return docs

    def write_check_file(filepath, docs):
        folder_path = os.path.join(os.path.dirname(filepath), "tmp_files")
        if not os.path.exists(folder_path):
            os.path.makedirs(folder_path)
        fp = os.path.join(folder_path, "load_file.txt")
        with open(fp, "a+", encoding="utf-8") as fout:
            fout.write(f"filepath={filepath}, len={len(docs)}")
            fout.write("\n")
            for doc in docs:
                fout.write(str(doc))
                fout.write("\n")
