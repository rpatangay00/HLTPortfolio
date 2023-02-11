import sys
import nltk 
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import random


# preprocessing the raw txt from the file
def preprocessing(raw): 
    tokens = word_tokenize(raw.lower()) 
  # Tokenizing the lowercase

    # variable to store the stopwords
    stop_words = set(stopwords.words('english'))

    # a. reducing the tokens to only those that are alpha, not in the NLTK stopword list.
    # also have length > 5

    tokens = [t for t in tokens if t.isalpha() and t not in stop_words and len(t) > 5]

    # b. lemmatize the tokens and use set() to make a list of unique lemmas

    unique_lemmas = sorted(list(set([WordNetLemmatizer().lemmatize(r) for r in tokens])))

    # c. do POS tagging on the unique lemmas and print the first 20 tagged items

    lemmas_unique_tags = nltk.pos_tag(unique_lemmas)

    # d. create a list of only those lemmas that are nouns

    noun_lemmas = list([x[0] for x in lemmas_unique_tags if x[1].startswith("N")])

    # e. Print the number of tokens and the number of nouns
    
    print('\nTotal Number of Tokens:', len(tokens))
    print('\nTotal Number of Nouns:', len(noun_lemmas))
    print("\nLexical diversity: %.2f" % (len(unique_lemmas) / (len(tokens))))
    print('\nFirst 20 Tagged Items:', lemmas_unique_tags[:20])

    # f. return tokens (not unique tokens) from step a, and nouns from the function

	return tokens, noun_lemmas


# Guessing game function
def word_guess_game(list):
    # Giving the user score of 5
    user_initial_score = 5

    # Rrandomly choosing a word from the 50 words list
    random_word_picked = random.choice(list)[0]
    letter_found = []
    users_guess = []

    print("\n\nYour Score: ", user_initial_score, "\n")

    for element in random_word_picked:
        print('_', end=" ")

    # When the score is below 0 (negative) the game will end.
    while user_initial_score > -1:
        user_letter_input = input('\n\nPlease enter a letter: ').lower()

        # Retrying with a proper input.
        if not user_letter_input.isalpha() and user_letter_input != "!":
            print("\nPlease type a valid letter.")

        # Retrying if user has already bput in this letter previously.
        elif user_letter_input in users_guess:
            print("\nYou have already attempted this letter, please try again.")

        # When user enters '!' game will ends such like when the score becomes negative
        elif user_letter_input != "!":
            # All the guesses the user has made into a list
            users_guess.append(user_letter_input)

            
            if user_letter_input in random_word_picked:
                user_initial_score += 1
                letter_found.append(user_letter_input)
                print("\nThe letter you picked is IN the word.")

            # if letter is not in word subtract 1 from score
            else:
                print("\nThe letter you picked is NOT IN the word")
                user_initial_score -= 1

            # update score and print current status of game
            count = 0
            for element in random_word_picked:
                if element in letter_found:
                    print(element, end=" ")
                    count += 1
                else:
                    print('_', end=" ")

            # after each try show user the score
            print("\nYour Score:", user_initial_score)

            # If word is guessed game over.
            if count == len(random_word_picked):
                
                retry_game = input("\n\nYou made it through! Play again? (Y/N) ")
                if retry_game.lower() == "y":
                    word_guess_game(list)
                else:
                    print("\nThank you for playing!")
                    sys.exit(0)

        else:
            print("\nThanks for playing the word guessing game!")
            sys.exit(0)

    # Show user score if the lost.. show the word.
    print("\n\nYou lost by score...the word was:", random_word_picked)

    retry_game = input("\nPlay again? (Y/N) ")
    if retry_game.lower() == "y":
        word_guess_game(list)
    else:
        print("\nThanks for playing the word guessing game!")
        sys.exit(0)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        print('Input file: ', input_file)

        with open('data.txt'.txt', 'r') as f:
            raw_text = f.read()

        tokens, noun_lemmas = preprocessing(raw_text)
        common_list = []

        # dictionary of nouns 
        counts = {t: tokens.count(t) for t in noun_lemmas}

        # Sort the dictionary by length of word and sort most common 50 words.
        
        words_sorted = sorted(counts.items(), key=lambda x: x[1], reverse=True) #saving to be used in the game
        print("The 50 most common words in this text:")
        for i in range(50):
            common_list.append(words_sorted[i])
            print(words_sorted[i])

        # Game start with the 50 words.
        word_guess_game(common_list)
    else:
        print('ERROR: File name is missing.')