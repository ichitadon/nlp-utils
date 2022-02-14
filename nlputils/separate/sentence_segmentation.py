import re
from typing import List, Match


class SentenceSegmentation:

    # default patterns for Japanese
    DEAFULT_CORNER_BRACKET_PATTERN = r"「[^「」]*」"
    DEAFULT_PARENS_PATTERN = r"\([^()]*\)"
    DEFAULT_PUNCTUATION_PATTERN = r"。!?！？"

    # default chars
    DEFAULT_ESCAPE_CHAR = "▨"
    DEFAULT_SEPARATOR_CHAR = "⇎"

    def __init__(
        self,
        parens_regex_patterns: List[str] = [DEAFULT_PARENS_PATTERN, DEAFULT_CORNER_BRACKET_PATTERN],
        punctuation_pattern: str = DEFAULT_PUNCTUATION_PATTERN,
        escape_char: str = DEFAULT_ESCAPE_CHAR,
        separator_char: str = DEFAULT_SEPARATOR_CHAR,
    ) -> None:
        """
        Initialize SentenceSegmentation.
        """
        # check args
        assert (
            escape_char != separator_char
        ), "`escape_char` and `separator_char` are same. please input different char to each args."
        assert (
            punctuation_pattern != ""
        ), "`punctuation_pattern` is empty. please input punctuation word or separator word."

        # initialize chars
        self.escape_char = escape_char
        self.separator_char = separator_char

        # initialize regex patterns
        self.punctuation_pattern = punctuation_pattern
        self.parens_regex_patterns = parens_regex_patterns
        self.escape_pattern = rf"(?<!{self.escape_char})([{self.punctuation_pattern}])(?!{self.escape_char})"
        self.unescape_pattern = rf"({self.escape_char})([{self.punctuation_pattern}])({self.escape_char})"

    def _punctuation_repl(self, match: Match[str]) -> str:
        """
        Function for `repl` parameter in re.sub. Escape punctuation between parentheses.
        """
        repl = rf"{self.escape_char}\1{self.escape_char}"
        result = re.sub(self.escape_pattern, repl, match.group(0))
        return result

    def separate(self, text: str) -> List[str]:
        """
        Separate target sentences by considering parentheses in the separator.
        """
        target_text = text

        # escape punctuation between parens
        for pattern in self.parens_regex_patterns:
            target_text = re.sub(pattern, self._punctuation_repl, target_text)

        # split sentences with target punctuations
        target_text = re.sub(self.escape_pattern, f"\\1{self.separator_char}", target_text)

        # remove escape char from target_text
        target_text = re.sub(self.unescape_pattern, "\\2", target_text)

        # split sentence with separator
        result = target_text.split(self.separator_char)
        if result[-1] == "":
            result.pop()

        return result
