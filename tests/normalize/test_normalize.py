import pytest

from nlputils.normalize.normalization import NeologdNormalizer


class TestNormalization:
    class TestNormalizeNeologd:
        def test_success(self) -> None:
            normalizer = NeologdNormalizer()
            assert "0123456789" == normalizer.normalize_neologd("０１２３４５６７８９")
            assert "ABCDEFGHIJKLMNOPQRSTUVWXYZ" == normalizer.normalize_neologd("ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ")
            assert "abcdefghijklmnopqrstuvwxyz" == normalizer.normalize_neologd("ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ")
            assert "!\"#$%&'()*+,-./:;<>?@[¥]^_`{|}" == normalizer.normalize_neologd("！”＃＄％＆’（）＊＋，－．／：；＜＞？＠［￥］＾＿｀｛｜｝")
            assert "＝。、・「」" == normalizer.normalize_neologd("＝。、・「」")
            assert "ハンカク" == normalizer.normalize_neologd("ﾊﾝｶｸ")
            assert "o-o" == normalizer.normalize_neologd("o₋o")
            assert "majikaー" == normalizer.normalize_neologd("majika━")
            assert "わい" == normalizer.normalize_neologd("わ〰い")
            assert "スーパー" == normalizer.normalize_neologd("スーパーーーー")
            assert "!#" == normalizer.normalize_neologd("!#")
            assert "ゼンカクスペース" == normalizer.normalize_neologd("ゼンカク　スペース")
            assert "おお" == normalizer.normalize_neologd("お             お")
            assert "おお" == normalizer.normalize_neologd("      おお")
            assert "おお" == normalizer.normalize_neologd("おお      ")
            assert "検索エンジン自作入門を買いました!!!" == normalizer.normalize_neologd("検索 エンジン 自作 入門 を 買い ました!!!")
            assert "アルゴリズムC" == normalizer.normalize_neologd("アルゴリズム C")
            assert "PRML副読本" == normalizer.normalize_neologd("　　　ＰＲＭＬ　　副　読　本　　　")
            assert "Coding the Matrix" == normalizer.normalize_neologd("Coding the Matrix")
            assert "南アルプスの天然水Sparking Lemonレモン一絞り" == normalizer.normalize_neologd("南アルプスの　天然水　Ｓｐａｒｋｉｎｇ　Ｌｅｍｏｎ　レモン一絞り")
            assert "南アルプスの天然水-Sparking*Lemon+レモン一絞り" == normalizer.normalize_neologd(
                "南アルプスの　天然水-　Ｓｐａｒｋｉｎｇ*　Ｌｅｍｏｎ+　レモン一絞り"
            )
