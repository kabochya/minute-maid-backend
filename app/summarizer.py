from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.edmundson import EdmundsonSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.sum_basic import SumBasicSummarizer
from sumy.summarizers.kl import KLSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

AVAILABLE_METHODS = {
    "luhn": LuhnSummarizer,
    "edmundson": EdmundsonSummarizer,
    "lsa": LsaSummarizer,
    "text-rank": TextRankSummarizer,
    "lex-rank": LexRankSummarizer,
    "sum-basic": SumBasicSummarizer,
    "kl": KLSummarizer,
}

LANGUAGE = "english"

def summarize(text, sentence_count, summarizer_type="lsa"):
    summarizer_class = AVAILABLE_METHODS[summarizer_type]
    parser = PlaintextParser(text, Tokenizer(LANGUAGE))
    # Default is english
    stemmer = Stemmer(LANGUAGE)
    summarizer = summarizer_class(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)
    return summarizer(parser.document, sentence_count)

if __name__=="__main__":
    with open("data/test3.txt", "r") as f:
        for s in summarize(f.read(), 3):
            print(s)
