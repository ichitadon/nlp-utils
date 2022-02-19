from typing import List

import pytest

from nlputils.separate import SentenceSegmentation


class TestSentenceSegmentation:
    class TestSeparate:
        def test_success_normal(self) -> None:
            testee = "sentence1。sentence2！文3？文4!文5?"
            target = SentenceSegmentation()
            expected = ["sentence1。", "sentence2！", "文3？", "文4!", "文5?"]
            actual = target.separate(testee)
            assert actual == expected

        def test_success_text_with_line_break(self) -> None:
            testee = "sentence1。sentence2\n！文3？\n文4!文5!"
            target = SentenceSegmentation()
            expected = ["sentence1。", "sentence2\n！", "文3？", "\n文4!", "文5!"]
            actual = target.separate(testee)
            assert actual == expected

        def test_success_text_with_corner_bracket(self) -> None:
            testee = "「sentence1。」sentence2！文3？文4!文5?"
            target = SentenceSegmentation()
            expected = ["「sentence1。」sentence2！", "文3？", "文4!", "文5?"]
            actual = target.separate(testee)
            assert actual == expected

        def test_success_text_with_half_parentheses(self) -> None:
            testee = "(sentence1。)sentence2！（文3？文4）!文5?"
            target = SentenceSegmentation()
            expected = ["(sentence1。)sentence2！", "（文3？", "文4）!", "文5?"]
            actual = target.separate(testee)
            assert actual == expected

        def test_success_add_paren_pattern(self) -> None:
            testee = "(sentence1。)sentence2！（文3？文4）!文5?"
            pattern = [
                SentenceSegmentation.DEAFULT_CORNER_BRACKET_PATTERN,
                SentenceSegmentation.DEAFULT_PARENTHESIS_PATTERN,
                SentenceSegmentation.DEAFULT_FULLWIDTH_PARENTHESIS_PATTERN,
            ]
            target = SentenceSegmentation(parens_regex_patterns=pattern)
            expected = ["(sentence1。)sentence2！", "（文3？文4）!", "文5?"]
            actual = target.separate(testee)
            assert actual == expected

        def test_success_add_punctuation_pattern(self) -> None:
            testee = "sentence1。sentence2\n！文3？\n文4!文5!"
            pattern = SentenceSegmentation.DEFAULT_PUNCTUATION_PATTERN + r"\n"
            target = SentenceSegmentation(punctuation_pattern=pattern)
            expected = ["sentence1。", "sentence2\n", "！", "文3？", "\n", "文4!", "文5!"]
            actual = target.separate(testee)
            assert actual == expected

        def test_success_input_empty_paren_pattern(self) -> None:
            testee = "(sentence1。)sentence2！（文3？文4）!文5?"
            pattern: List[str] = []
            target = SentenceSegmentation(parens_regex_patterns=pattern)
            expected = ["(sentence1。", ")sentence2！", "（文3？", "文4）!", "文5?"]
            actual = target.separate(testee)
            assert actual == expected

        def test_failure_input_empty_punctuation_pattern(self) -> None:
            pattern = ""
            with pytest.raises(AssertionError):
                SentenceSegmentation(punctuation_pattern=pattern)

        def test_failure_input_same_escape_char_and_separator_char(self) -> None:
            escape_char = "▨"
            separator_char = "▨"
            with pytest.raises(AssertionError):
                SentenceSegmentation(escape_char=escape_char, separator_char=separator_char)
