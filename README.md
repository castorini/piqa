# piqa

Freetext question answering on Raspberry Pi (PiQA)

## Dependencies

This project requires Anserini as a dependency. Please organize the directory structure as follows.

```
.
├── Anserini
└── piqa
```

One can build Anserini by running the following inside `Anserini`:

```
mvn clean package appassembler:assemble
```

Install other Python dependencies with `pip` via:

```
pip install -r requirements.txt
```

We also use the SpaCy library, and we need to download English models for it:

```
python -m spacy download en
```

Install front-end dependencies by running `npm install` inside the `static` directory.

## Configuration

Copy `config.cfg.example` to `config.cfg` and make necessary changes, such as setting the index path and API keys.

## Running

Run server:

```
python server.py
```

Run UI (inside `static`):

```
npm start
```
