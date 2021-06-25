from nltk.tokenize import WhitespaceTokenizer
from nltk import ngrams
from nltk import Counter
import re
import random


class PredictiveTextGenerator:

    def __init__(self):
        self.document = ''
        self.tokenized = []
        self.trigrams = []
        self.ht_dictionary = {}
        self.pattern = r'[!|\.|\?]$'
        self.process_text()
        self.build_sentences()

    # Takes input string of a file name. Reads the file. Tokenizes each word on whitespace.
    # Creates trigrams from the tokens. The first two words of each trigram are the head,
    # the third is the tail. Creates default dict of every head and every tail for each head.
    def process_text(self):
        self.document = input()
        with open(self.document, 'r', encoding='utf-8') as f:
            tk = WhitespaceTokenizer()
            self.tokenized = tk.tokenize(f.read())
            self.trigrams = list(ngrams(self.tokenized, 3))
            for head1, head2, tail in self.trigrams:
                head = f"{head1} {head2}"
                self.ht_dictionary.setdefault(head, []).append(tail)

    def get_start_word(self):
        start_words = []
        for word in self.tokenized:
            if word[0].isupper() and not re.search(self.pattern, word):
                start_words.append(word)
        start = random.choice(start_words)
        for item in self.ht_dictionary:
            if item.startswith(start + " "):
                return item

    def build_sentences(self):
        sentence = 10
        while sentence > 0:
            words = []
            start_word = self.get_start_word()
            first, second = start_word.split()
            words.append(first)
            words.append(second)
            for _ in range(2):  # Ensures at least 5 tokens per sentence.
                tails = Counter(self.ht_dictionary[start_word])
                for tail, count in tails.most_common(1):
                    words.append(tail)
                    start_word = f"{start_word.split()[1]} {tail}"
            while True:  # Repeatedly adding tails until sentence ending punctuation encountered.
                tails = Counter(self.ht_dictionary[start_word])
                for tail, count in tails.most_common(1):
                    if not re.search(self.pattern, tail):
                        words.append(tail)
                        start_word = f"{start_word.split()[1]} {tail}"
                    else:
                        words.append(tail)
                        print(*words)
                        sentence -= 1
                        break
                break


generator = PredictiveTextGenerator()
