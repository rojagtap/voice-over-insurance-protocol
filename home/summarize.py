from nltk.probability import FreqDist
from heapq import nlargest
from collections import defaultdict
from nltk import word_tokenize


def get_tokens(sentence_tokens, word_tokens):
    sentence_ranks = score_tokens(word_tokens, sentence_tokens)
    return summarize(sentence_ranks, sentence_tokens, int(len(sentence_tokens) * 4 / 100))


def summarize(ranks, sentences, length):
    if int(length) > len(sentences):
        print("Error, more sentences requested than available. Use --l (--length) flag to adjust.")
        exit()

    indexes = nlargest(length, ranks, key=ranks.get)
    final_sentences = [sentences[j] for j in sorted(indexes)]
    return ' '.join(final_sentences)


def score_tokens(filtered_words, sentence_tokens):
    word_freq = FreqDist(filtered_words)
    d = set(line.strip() for line in open('home/files/input/keyws.txt'))
    ranking = defaultdict(int)

    for i, sentence in enumerate(sentence_tokens):
        for word in word_tokenize(sentence.lower()):
            if word in word_freq:
                ranking[i] += word_freq[word]
            if word in d:
                ranking[i] += 4
    return ranking
