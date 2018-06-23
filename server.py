import argparse
import configparser
import os
import sys

from flask import Flask, jsonify, request

from ranking.simple_sentence_ranker import SimpleSentenceRanker
from retrieval.sentence_retriever import SentenceRetriever

app = Flask(__name__)
sent_retriever = None
sent_ranker = None

@app.route('/', methods=['GET'])
def hello():
    return 'Hello! The server is up... :)'

@app.route('/wit_ai_config', methods=['GET'])
def wit_ai_config():
    return jsonify({'WITAI_API_SECRET': app.config['Frontend']['witai_api_secret']})

@app.route('/answer', methods=['POST'])
def answer():
    try:
        req = request.get_json(force=True)
        question = req['question']
        num_hits = req.get('num_hits', 30)
        print('Question: {}'.format(question))

        global sent_retriever, sent_ranker
        if sent_retriever is None:
            sent_retriever = SentenceRetriever(app.config)
            sent_ranker = SimpleSentenceRanker()

        sentences = sent_retriever.search(question)
        ranked_sentences = sent_ranker.rank(question, sentences)[:num_hits]
        answers = [{'passage': t[0], 'score': t[1]} for t in ranked_sentences]
        answer_dict = {"answers": answers}
        return jsonify(answer_dict)
    except Exception as e:
        raise e
        error_dict = {'error': 'ERROR - could not parse the question or get answer.'}
        return jsonify(error_dict)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start the Flask API at the specified host, port')
    parser.add_argument('--config', help='config to use', required=False, type=str, default='config.cfg')
    parser.add_argument('--debug', help='debug mode', action='store_true')

    args = parser.parse_args()
    if not os.path.isfile(args.config):
        print('The configuration file ({}) does not exist!'.format(args.config))
        sys.exit(1)

    config = configparser.ConfigParser()
    config.read(args.config)

    for name, section in config.items():
        if name == 'DEFAULT':
            continue

        app.config[name] = {}
        for key, value in config.items(name):
            app.config[name][key] = value

    print('Config: {}'.format(args.config))
    print('Index: {}'.format(app.config['Flask']['index']))
    print('Host: {}'.format(app.config['Flask']['host']))
    print('Port: {}'.format(app.config['Flask']['port']))

    app.run(debug=args.debug, host=app.config['Flask']['host'], port=int(app.config['Flask']['port']))
