# encoding: utf8
from __future__ import unicode_literals

import re
import unicodedata
from typing import Dict


# TODO: Improve the configuration to be optional.
class NeologdNormalizer:
    """
    neologd-based text normalizer
    refs : https://github.com/neologd/mecab-ipadic-neologd/wiki/Regexp.ja#python-written-by-hideaki-t--overlast
    """

    def __init__(self) -> None:
        pass

    def unicode_normalize(self, cls: str, s: str) -> str:
        pt = re.compile("([{}]+)".format(cls))

        def norm(c: str) -> str:
            return unicodedata.normalize("NFKC", c) if pt.match(c) else c

        s = "".join(norm(x) for x in re.split(pt, s))
        s = re.sub("－", "-", s)
        return s

    def remove_extra_spaces(self, s: str) -> str:
        s = re.sub("[ 　]+", " ", s)
        blocks = "".join(
            (
                "\u4E00-\u9FFF",  # CJK UNIFIED IDEOGRAPHS
                "\u3040-\u309F",  # HIRAGANA
                "\u30A0-\u30FF",  # KATAKANA
                "\u3000-\u303F",  # CJK SYMBOLS AND PUNCTUATION
                "\uFF00-\uFFEF",  # HALFWIDTH AND FULLWIDTH FORMS
            )
        )
        basic_latin = "\u0000-\u007F"

        def remove_space_between(cls1: str, cls2: str, s: str) -> str:
            p = re.compile("([{}]) ([{}])".format(cls1, cls2))
            while p.search(s):
                s = p.sub(r"\1\2", s)
            return s

        s = remove_space_between(blocks, blocks, s)
        s = remove_space_between(blocks, basic_latin, s)
        s = remove_space_between(basic_latin, blocks, s)
        return s

    def normalize_neologd(self, s: str) -> str:
        s = s.strip()
        s = self.unicode_normalize("０-９Ａ-Ｚａ-ｚ｡-ﾟ", s)

        def maketrans(f: str, t: str) -> Dict[int, int]:
            return {ord(x): ord(y) for x, y in zip(f, t)}

        s = re.sub("[˗֊‐‑‒–⁃⁻₋−]+", "-", s)  # normalize hyphens
        s = re.sub("[﹣－ｰ—―─━ー]+", "ー", s)  # normalize choonpus
        s = re.sub("[~∼∾〜〰～]", "", s)  # remove tildes
        s = s.translate(maketrans("!\"#$%&'()*+,-./:;<=>?@[¥]^_`{|}~｡､･｢｣", "！”＃＄％＆’（）＊＋，－．／：；＜＝＞？＠［￥］＾＿｀｛｜｝〜。、・「」"))

        s = self.remove_extra_spaces(s)
        s = self.unicode_normalize("！”＃＄％＆’（）＊＋，－．／：；＜＞？＠［￥］＾＿｀｛｜｝〜", s)  # keep ＝,・,「,」
        s = re.sub("[’]", "'", s)
        s = re.sub("[”]", '"', s)
        return s
