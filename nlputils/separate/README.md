# Sentence Segmentation
入力されたテキストを句点等の特定の文字で分割します。

## 使い方

### デフォルトの設定で使用する場合
全角句点（`。`）と各種終端文字（`！`,`？`,`!`,`?`）が出現した場合に分割します。  
全角カギ括弧（`「」`） と半角丸括弧（`()`）に挟まれている文中の句点では分割されません。

``` python
>>> from nlputils.separate import SentenceSegmentation
>>> text = "彼は「こんにちは。」と言った。私も「ごきげんよう。」と返した。"
>>> segmenter = SentenceSegmentation()
>>> segmenter.separate(text)
['彼は「こんにちは。」と言った。', '私も「ごきげんよう。」と返した。']
```

### 無視する対象の括弧を指定する場合
引数 `parens_regex_patterns` にパターンを指定することで、無視する対象の括弧を変更できます。
全角丸括弧（`（）`）を追加する場合は以下のように、リストにパターンを指定します。

``` python
>>> text = "彼は「こんにちは。」と言った。私も（ごきげんよう。）と返した。"
>>> pattern = [
...     SentenceSegmentation.DEAFULT_CORNER_BRACKET_PATTERN,
...     SentenceSegmentation.DEAFULT_PARENS_PATTERN,
...     r"（[^（）]*）",
... ]
>>> segmenter = SentenceSegmentation(parens_regex_patterns=pattern)
>>> segmenter.separate(text)
['彼は「こんにちは。」と言った。', '私も（ごきげんよう。）と返した。']
```

括弧を無視しない場合は以下のように空のリストを指定します。

``` python
>>> segmenter = SentenceSegmentation(parens_regex_patterns=[])
>>> segmenter.separate(text)
['彼は「こんにちは。', '」と言った。', '私も「ごきげんよう。', '」と返した。']
```
