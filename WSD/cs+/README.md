# Supervised WSD

### Introduction

（為什麼選 supervised 方法）

### Difficulties

（碰到的問題，如：CWN lemma 與 sense 對不起來）

### Dataset

（如何做出 labeled data，label 的根據是什麼）

### Model I — Simple RNN Classifier

利用非常簡單的 Recurrent Neural Network 做分類器來判斷詞義

##### Structure

堆疊單層 gated recurrent unit 和一層 full-connected layer

```python
inputs = Input(shape=(X.shape[1], X.shape[2]))
rec_lyr = GRU(32)(inputs)
dns_lyr = Dense(Y.shape[1], activation='softmax')(rec_lyr)
model = Model(input=inputs, output=dns_lyr)
model.compile(optimizer='rmsprop',
              loss='categorical_crossentropy',
              metrics=['accuracy'])
```

##### Steps

- 以 character-level 的原句作為 input，word sense 的 ID 作為 output
- one-hot 編碼訓練資料的 input 及 output
- 以 categorical cross-entropy 作為 loss 來訓練模型

##### Results

|         | assign top |  RNN | RNN(wider) | RNN(deeper) |
| ------- | ---------: | ---: | ---------: | ----------: |
| f1score |       0.35 | 0.65 |       0.72 |        0.75 |

