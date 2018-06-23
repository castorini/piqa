import configparser

import jnius_config
import spacy


class SentenceRetriever(object):

    def __init__(self, config):
        print(config['Flask']['anserini_jar'])
        jnius_config.set_classpath(config['Flask']['anserini_jar'])
        from jnius import autoclass
        self.JString = autoclass('java.lang.String')
        self.JSearcher = autoclass('io.anserini.search.SimpleSearcher')
        self.searcher = self.JSearcher(self.JString(config['Flask']['index']))
        self.nlp = spacy.load('en_core_web_sm')

    def search(self, query):
        hits = self.searcher.search(self.JString(query))
        sentences = []
        for hit in hits:
            spacy_doc = self.nlp(hit.content)
            for s in spacy_doc.sents:
                sentences.append(s)
        return sentences
