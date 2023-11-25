import numpy as np
import pandas as pd
from pprint import pprint
import torch

from evadb.catalog.catalog_type import NdArrayType
from evadb.functions.abstract.abstract_function import AbstractFunction
from evadb.functions.decorators.decorators import forward, setup
from evadb.functions.decorators.io_descriptors.data_types import PandasDataframe
from evadb.functions.gpu_compatible import GPUCompatible
from transformers import BertModel, BertTokenizer
from sentence_transformers import SentenceTransformer


class CosineSimilarityScore(AbstractFunction, GPUCompatible):
    def __init__(self):
        # Initialize BERT tokenizer
        # self.bert_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        # self.bert_model = BertModel.from_pretrained('bert-base-uncased')
        self.model = SentenceTransformer('distilbert-base-nli-mean-tokens')

    @setup(cacheable=False, function_type="Similarity", batchable=False)
    def setup(self):

        pass

    def to_device(self, device: str) -> GPUCompatible:
        return self

    @property
    def name(self) -> str:
        return "CosineSimilarityScore"

    @forward(
        input_signatures=[
            PandasDataframe(
                columns=["chunk", "query"],
                column_types=[NdArrayType.STR, NdArrayType.STR],
                column_shapes=[(1), (1)],
            )
        ],
        output_signatures=[
            PandasDataframe(
                columns=["cosine_similarity_score"],
                column_types=[NdArrayType.STR],
                column_shapes=[(1)],
            )
        ],
    )
    def forward(self, df: pd.DataFrame) -> pd.DataFrame:
        res = pd.DataFrame(columns=["cosine_similarity_score"])

        columns = df.columns.tolist()
        query = df[columns[1]].iloc[0]
        context_chunks = df[columns[0]].tolist()

        query_embedding = self.model.encode(query)
        context_chunks_embeddings = self.model.encode(context_chunks)

        cos_sim_func = torch.nn.CosineSimilarity(dim=0, eps=1e-6)

        b = torch.from_numpy(context_chunks_embeddings)
        highest_sim = 0
        for i in range(len(context_chunks_embeddings)):
            a = torch.from_numpy(query_embedding)
            cos_sim = cos_sim_func(a, b[i])
            res.loc[i] = [cos_sim.item()]
            if cos_sim > highest_sim:
                highest_sim = cos_sim
        print('highest sim: ', highest_sim)
        print('highest sim index: ', np.argmax(res))
        print('highest sim chunk: ', context_chunks[np.argmax(res)])
        return res
