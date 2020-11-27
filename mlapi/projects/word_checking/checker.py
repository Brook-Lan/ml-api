import re

from utils.flashtext import KeywordProcessor
from utils.decorators import singleton


@singleton
class FlashtextWordChecker:
    def __init__(self):
        self.kw_processor = KeywordProcessor()
        self.kw_processor.set_non_word_boundaries([])

    def add_keywords_from_file(self, words_file):
        self.kw_processor.add_keyword_from_file(words_file)

    def add_keywords(self, words):
        self.kw_processor.add_keywords_from_list(words)

    def check(self, txt):
        keywords_found = self.kw_processor.extract_keywords(txt)
        return keywords_found


@singleton
class ReWordChecker:
    def __init__(self):
        pass

    def add_keywords(self, words):
        self.word_p =  re.compile("|".join(words))

    def add_keywords_from_file(self, words_file):
        with open(words_file) as f:
            words = [w.strip() for w in f]
            self.add_keywords(words)

    def check(self, txt):
        keywords_found = self.word_p.findall(txt)
        return keywords_found


WordChecker = ReWordChecker
# WordChecker = FlashtextWordChecker


if __name__ == "__main__":
    word_check = WordChecker()
    word_check.add_keywords(["北京","欢迎","您"])

    words_found = word_check.check("333北京欢迎您！")
    print(words_found)