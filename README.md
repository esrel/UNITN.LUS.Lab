# Language Understanding Systems Lab (LUS)

## Outline

0. [Lexicon and Corpora](notebooks/corpus_preprocessing.ipynb)
    
    - Corpus
        - Descriptive Statistics
    
    - Lexicon
        - Lexicon & Size
        - Frequency List
        - Lexicon Operations
            - Frequency Cut-Off
            - Stop-words and Stop-word Removal
    
    - Corpus Pre-processing [TODO]
        - Normalization
        - Tokenization/Detokenization
        - Lowercasing/Truecasing
        - Word Classes and Normalization
            - Removal vs. Generalization
        - Lemmatization
        - Stemming

0. [Ngram Modeling](notebooks/ngram_modeling.ipynb)

    - Ngrams
        - Ngram Counting
        - Ngram Probabilties
        
    - Ngram Language Models

        - Markov Models: Markov Chain
        - Markov Property (Assumption)   
        - Maximum Likelihood Estimation

0. Classification [TODO]
    - Bayes (Conditional Independence) Assumption 
    - Naive Bayes Classifier

0. [Sequence Labeling](notebooks/sequence_labeling.ipynb)
    - Markov Models: Hidden Markov Models
    - Tagging
        - Part-of-Speech Tagging [TODO]
    - Chunking [TODO]
    - Shallow Parsing
        - Joint Segmentation and Classification
        - Named Entity Recognition [TODO]


----------
## Weighted Finite State Machine Exercises (with [OpenFST](http://www.openfst.org/) & [OpenGRM](http://www.opengrm.org/))

0. [WFSM Operations](notebooks/wfsm_operations.ipynb)
0. [Ngram Modeling](notebooks/wfsm_ngram_modeling.ipynb) 
0. [Sequence Labeling](notebooks/wfsm_sequence_labeling.ipynb)