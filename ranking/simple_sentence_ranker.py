import spacy


class SimpleSentenceRanker(object):

    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')

    def rank(self, query, sentences):
        query = self.nlp(query)
        sent_with_scores = [(s.string, query.similarity(s)) for s in sentences]
        sent_with_scores.sort(key=lambda t: t[1], reverse=True)
        return sent_with_scores
