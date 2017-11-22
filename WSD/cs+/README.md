# Supervised WSD

### Introduction

選用supervised方法，使用人工標註數據，用RNN方法訓練。

### Difficulties

缺少訓練資料，而人工標註資料量有限。

### Dataset

從斷詞好的電影字幕資料中篩選出含有“坐”字的800個句子，過濾掉三個詞以下的句子，再根據CWN中的“坐”的含義對每個句子中的“坐”字含義進行人工標註。以其中680個句子作為training set，120個作為test set。

坐的含義（CWN）：
- 1.  不及物動詞 ( VA )
維持上身直立，臀部放在椅子或其它物體上支撐身體重量的姿勢。
- 2.  不及物動詞 ( VA )
將身體由其它姿勢變成坐著的姿勢。
- 3.  及物動詞 ( VC )
搭乘有座位的交通工具。
- 4.  及物動詞 ( VC )
搭乘有座位的遊樂設施。
- 5.  及物動詞 ( VC )
容納後述的使用人數。
- 6.  副詞 ( D )
表擁有特定職位卻不做事
- 7.  不及物動詞 ( VA )
坐著修練，通常盤腿，身體端正而放鬆，注意呼吸及意念，佛教、印度教等宗教或氣功當中的一種修練方式。
- 8.  不及物動詞 ( VA )
婦女生產後調養身體。
- 9.  及物動詞 ( VC )
在監獄中服刑。
- 10.  及物動詞 ( VC )
比喻維持在特定地位。
- 11.  及物動詞 ( VCL )
房屋背對著後述方位。常用「坐…朝…」。
- 12.  及物動詞 ( VC )
以後述狀態為進一步發展的基礎，後接數目。常用「坐…望…」。


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
