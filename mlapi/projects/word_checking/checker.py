from utils.flashtext import KeywordProcessor
from utils.decorators import singleton


@singleton
class WordChecker:
    def __init__(self):
        self.kw_processor = KeywordProcessor()

    def load_keywords(self, words_file):
        self.kw_processor.add_keyword_from_file(words_file)

    def check(self, txt):
        keywords_found = self.kw_processor.extract_keywords(txt)
        return keywords_found


if __name__ == "__main__":
    keyword_processor = KeywordProcessor()
    keyword_processor.add_keyword_from_file("data/words/sensitive_words.txt")
    keywords_found = keyword_processor.extract_keywords("世界第一")