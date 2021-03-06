import numpy as np

from .pagerank import pagerank
from .graph import sent_graph, word_graph
from utils.types_ import *


class TextRank:
    def __init__(
        self,
        min_count: int = 2,
        min_sim: float = 0.3,
        tokenizer: str = "mecab",
        noun: bool = False,
        similarity: str = "cosine",
        df: float = 0.85,
        max_iter: int = 50,
        method: str = "iterative",
        stopwords: List[str] = ["뉴스", "기자"],
    ):
        """
        TextRank Class
        ==============

        Arguments
        ---------
        min_count : int
            Minumum frequency of words will be used to construct sentence graph
        min_sim : float
            Minimum similarity of sents or words will be used to construct sentence graph
        tokenizer : str
            Tokenizer for korean, default is mecab
        noun : bool
            option for using just nouns, default is False but True when use keyword extraction
        similarity : str
            available similarity = ['cosine', 'textrank']
        df : float
            PageRank damping factor, default is 0.85
        max_iter : int
            Number of PageRank iterations
        method : str
            available method = ['iterative', 'algebraic']
        stopwords: list of str
            Stopwords for Korean
        """

        self.tokenizer = tokenizer
        self.min_count = min_count
        self.min_sim = min_sim
        self.noun = noun
        self.similarity = similarity
        self.df = df
        self.max_iter = max_iter
        self.method = method
        self.stopwords = stopwords

    def sent_textrank(self, sents: List[str]) -> None:
        G = sent_graph(
            sents,
            self.min_count,
            self.min_sim,
            self.tokenizer,
            self.noun,
            self.similarity,
            self.stopwords,
        )

        self.R = pagerank(G, self.df, self.max_iter, self.method)
        return None

    def word_textrank(self, sents: List[str]) -> None:
        G, _, self.idx_vocab = word_graph(
            sents,
            self.min_count,
            self.min_sim,
            self.tokenizer,
            noun=True,
            stopwords=self.stopwords,
        )

        self.wr = pagerank(G, self.df, self.max_iter, self.method)
        return None

    def summarize(self, sents: List[str], topk: int = 3) -> List[str]:
        self.sent_textrank(sents)
        idxs = self.R.argsort()[-topk:]
        keysents = [sents[idx] for idx in sorted(idxs)]
        keysents = "\n".join(keysents)
        return keysents

    def keywords(self, sents: List[str], topk: int = 10) -> List[str]:
        self.word_textrank(sents)
        idxs = self.wr.argsort()[-topk:]
        keywords = [self.idx_vocab[idx] for idx in reversed(idxs)]
        return keywords
