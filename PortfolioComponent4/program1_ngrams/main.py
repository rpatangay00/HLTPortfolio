#!/usr/bin/python

#import statements
import pathlib
import sys
import pickle
from nltk import word_tokenize
from nltk.util import ngrams


# taking in a filename as an arguement and returns a tuple of 2 dicts.
def read_file(filename):
    with open(pathlib.Path.cwd().joinpath(rel_path), 'r', encoding="utf8") as f:
        readIn_txt = f.read().replace('\n', '') #having a variable readIn_txt that reads in the text from the file
        # with the newlines removed using the replace function

    # Tokenize the text

    unigrams = word_tokenize(str_text) # Also... using NLTK to create bigrams
    bigrams = list(ngrams(unigrams, 2)) # NLTK to create unigrams lists

    unigram_dict = {t: unigrams.count(t) for t in set(unigrams)} # unigram dict
    bigram_dict = {b: bigrams.count(b) for b in set(bigrams)} # bigram dict

    return bigram_dict, unigram_dict

# return the dicts for the bigram and unigram


# MAIN FUNCTION

if __name__ == '__main__':
    # providing the files to be read as sysargs
    if len(sys.argv) < 4:
        print("Please enter filenames as sys args as follows:")
        print("run the file like so...  ""./main.py <filename(s)>"" ")
        print("data/LangId.train.English " "data/LangId.train.French " "data/LangId.train.Italian")
        quit()

    for i in range(1, 4):  # sysargs indexes 1-3
        # using pickle
        rel_path = sys.argv[i]
        print("\nNow reading " + rel_path + ".")
        bigrams, unigrams = read_file(rel_path)

        # pickle dicts
        print("Pickling bigrams...")
        bigrams_file = open('bigrams%d.pickle' % i, 'wb')
        pickle.dump(bigrams, bigrams_file)
        bigrams_file.close() #close the file

        print("Pickling unigrams...")
        unigrams_file = open('unigrams%d.pickle' % i, 'wb')
        pickle.dump(unigrams, unigrams_file)
        unigrams_file.close() #close the file
