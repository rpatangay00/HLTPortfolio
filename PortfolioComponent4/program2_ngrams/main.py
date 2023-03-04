#import statements
import pathlib
import pickle
from nltk import word_tokenize
from nltk.util import ngrams



def compute_prob(text, unigram_dict, bigram_dict, V):

    text_unigrams = word_tokenize(text)

    text_bigrams = list(ngrams(text_unigrams, 2))

    p_laplace = 1

    for bigram in text_bigrams:

        n = int(bigram_dict.get(bigram)) if bigram in bigram_dict else 0
        d = int(unigram_dict.get(bigram[0])) if bigram[0] in unigram_dict else 0
        p_laplace = p_laplace * ((n + 1) / (d + V))

    return p_laplace


if __name__ == '__main__':
    # Read the pickle files back in
    bigrams1 = pickle.load(open('bigrams1.pickle', 'rb'))    # English bigrams
    unigrams1 = pickle.load(open('unigrams1.pickle', 'rb'))  # English unigrams
    bigrams2 = pickle.load(open('bigrams2.pickle', 'rb'))    # French bigrams
    unigrams2 = pickle.load(open('unigrams2.pickle', 'rb'))  # French unigrams
    bigrams3 = pickle.load(open('bigrams3.pickle', 'rb'))    # Italian bigrams
    unigrams3 = pickle.load(open('unigrams3.pickle', 'rb'))  # Italian unigrams

    int_vocab = len(unigrams1) + len(unigrams2) + len(unigrams3)

    file_probs = open(pathlib.Path.cwd().joinpath('data/LangId.probs'), 'a')

    int_index = 1
    for line in open(pathlib.Path.cwd().joinpath('data/LangId.test'), 'r').readlines():

        probs1 = compute_prob(line, unigrams1, bigrams1, int_vocab)
        probs2 = compute_prob(line, unigrams2, bigrams2, int_vocab)
        probs3 = compute_prob(line, unigrams3, bigrams3, int_vocab)

        if (probs1 >= probs2) and (probs1 >= probs3):
            langProb = 'English'
        elif (probs2 >= probs1) and (probs2 >= probs3):
            langProb = 'French'
        else:
            langProb = 'Italian'

        probString = str(int_index) + ' ' + langProb + '\n'
        int_index += 1
        file_probs.write(probString)

    file_probs.close()
    file_probs = open(pathlib.Path.cwd().joinpath('data/LangId.probs'), 'r')

    file_solutions = open(pathlib.Path.cwd().joinpath('data/LangId.sol'), 'r')
    probs_data = file_probs.readlines()
    sol_data = file_solutions.readlines()
    int_correct = 0
    for i in range(len(probs_data)):
        if probs_data[i] == sol_data[i]:
            int_correct += 1
    accuracy = int_correct / len(probs_data)
    accuracy *= 100
    print('The percentage of correctly classified test cases is ' + str(accuracy) + '%.')

    file_probs.close()
    file_solutions.close()