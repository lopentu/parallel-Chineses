提供了三個模型用以偵測語言地區：
1. simple_nb.py：使用multinominal naive bayes
2. binary_nb.py：使用binary naive bayes
3. tfidf_nb.py：使用tfidf naive bayes
提供nb.py，可以使用參數‘simple’、‘binary’、‘tfidf’在終端分別跑不同的模型并查看結果

nb.py說明：
1. nb.py直接使用med.csv作為輸入，也就是week3作業計算的最大編輯距離，med.csv為5組電影字幕產生的結果，詳見med_compute.py說明
2. nb.py通過參數limit來調節過濾的資料量，med中norm_med結果為0即代表tw字幕與cn字幕完全相同，數值越大差異越大，limit設0時即過濾掉所有norm_med為0的資料，設1.0時即過濾掉 所有norm_med小於等於1的資料，增加limit可以增大訓練資料中tw與cn的差異
3. nb.py輸出結果為：在給定模型下，分別訓練limit為0，0.5，1，1.5所產生的資料，并以9：1隨機切分training data與test data，simple和binary模型各隨機切分100次，最後輸出平均的accuracy，tfidf由於訓練時間過長，僅隨機切分3次輸出平均accuracy

med_compute.py說明：
1. med_compute.py讀入一個list，list包含若干組tw與cn字幕檔案地址，並且斷詞字典放在字幕檔案同一文件夾下。
2. 輸出文檔med.csv為所有tw與cn字幕產生的aligned sentences的med以及norm_med（med除以tw與cn字幕中的最大長度）

模型结论：
隨著limit增加（0->0.5->1->1.5），accuracy先升高后下降（訓練資料量逐漸下降）：
simple：66.62%， 68.55%， 69.47%， 66.57%
binary：65.11%， 66.97%， 67.77%， 65.73%
tfidf: 66.28%(0), 68.73%(1), tfidf訓練時間過長，建議run前修改一下需要跑的limit值和times
