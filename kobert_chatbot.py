# -*- coding: utf-8 -*-
"""KoBERT_chatbot.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17cSrbCsDh4jD7n2AQYakyECne74EBl4U
"""

!pip install mxnet
!pip install gluonnlp pandas tqdm
!pip install sentencepiece
!pip install transformers==3
!pip install torch

!pip install git+https://git@github.com/SKTBrain/KoBERT.git@master

import torch
from torch import nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import gluonnlp as nlp
import numpy as np
import pandas as pd
from tqdm import tqdm, tqdm_notebook

from kobert.utils import get_tokenizer
from kobert.pytorch_kobert import get_pytorch_kobert_model

from transformers import AdamW
from transformers.optimization import get_cosine_schedule_with_warmup

##GPU 사용 시
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

bertmodel, vocab = get_pytorch_kobert_model()

from google.colab import drive
drive.mount('/content/drive')

dataset_train = nlp.data.TSVDataset("/content/drive/MyDrive/train_label.tsv", field_indices=[0,1], num_discard_samples=0)

tokenizer = get_tokenizer()
tok = nlp.data.BERTSPTokenizer(tokenizer, vocab, lower=False)

class BERTDataset(Dataset):
    def __init__(self, dataset, sent_idx, label_idx, bert_tokenizer, max_len,
                 pad, pair):
        transform = nlp.data.BERTSentenceTransform(
            bert_tokenizer, max_seq_length=max_len, pad=pad, pair=pair)

        self.sentences = [transform([i[sent_idx]]) for i in dataset]
        self.labels = [np.int32(i[label_idx]) for i in dataset]

    def __getitem__(self, i):
        return (self.sentences[i] + (self.labels[i], ))

    def __len__(self):
        return (len(self.labels))

## Setting parameters
max_len = 64
batch_size = 128
warmup_ratio = 0.1
num_epochs = 5
max_grad_norm = 1
log_interval = 200
learning_rate =  5e-5

data_train = BERTDataset(dataset_train, 0, 1, tok, max_len, True, False)
#data_test = BERTDataset(dataset_test, 0, 1, tok, max_len, True, False)

from numpy import dot
from numpy.linalg import norm
import numpy as np
def cos_sim(A, B):
       return dot(A, B)/(norm(A)*norm(B))

data_train.__getitem__(1)[0]

cos_sim(data_train.__getitem__(1)[0],data_train.__getitem__(1)[0])

answers = pd.read_csv("/content/drive/MyDrive/result_answer.tsv", delimiter='\t', header=None)

while(1):
  input_sentence = input()
  temp_df = pd.DataFrame([[input_sentence, 1]], columns = [['질문', '답변']])
  temp_df = temp_df.values
  test_set = BERTDataset(temp_df, 0, 1, tok, max_len, True, False) 
  result = []
  for i in range(data_train.__len__()):
    result.append(cos_sim(test_set.__getitem__(0)[0],data_train.__getitem__(i)[0]))
  print(answers[1][result.index(max(result))])