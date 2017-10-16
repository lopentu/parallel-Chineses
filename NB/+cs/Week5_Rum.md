

```python
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
import pandas as pd
import jieba
```


```python
data = pd.read_csv("Schindlers_List_1993.csv")
```


```python
jieba.load_userdict("dict.txt.big")

# data preprocessing
def split_into_tokens(message):
    return list(jieba.cut(message))
```


```python
X_train, X_test, y_train, y_test = train_test_split(data["text"], data["tag"], test_size=0.2)
```


```python
bow_transformer = CountVectorizer(split_into_tokens).fit(X_train)
```


```python
training_lines_bow = bow_transformer.transform(X_train)
test_lines_bow = bow_transformer.transform(X_test)
```


```python
tfidf_transformer = TfidfTransformer().fit(training_lines_bow)
```


```python
training_lines_tfidf = tfidf_transformer.transform(training_lines_bow)
test_lines_tfidf = tfidf_transformer.transform(test_lines_bow)
```


```python
language_detector = MultinomialNB().fit(training_lines_tfidf, y_train)
```


```python
# this is really low. Did I do something wrong???

language_detector.score(test_lines_tfidf, y_test)
```




    0.61349693251533743




```python

```
