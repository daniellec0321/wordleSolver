#!/usr/bin/python3

from Word import Word
from string import ascii_lowercase



# reads in a file and then puts it into word vector
def read_file(the_words):

    # read file
    with open('common-words.txt') as f:
        the_strings = f.readlines()

    # initializing variables
    iter = 0
    the_map = dict()

    # fill in dictionary
    for string in the_strings:
        the_map[string.rstrip()] = iter
        iter += 1

    # read in info words
    with open('info-words.txt') as f2:
        for line in f2:
            temp_word = Word(line.rstrip(), the_map)
            the_words.append(temp_word)



# initializes the letter map
def init_letter_map(letter_map):

    # iterate through letters
    for letter in ascii_lowercase:
        letter_map[letter] = ['n', 'n', 'n', 'n', 'n']



# updates letter map with the info from the user's guess
def update_letter_map(word, colors, letter_map):
    
    # fix word and colors to be lowercase
    word = word.lower()
    colors = colors.lower()

    gray_indices = list()
    g_y_letters = list()

    # iterate through the letters of the word
    for jter in range(0, len(colors)):

        if colors[jter] == 'a':
            letter_map[word[jter]][jter] = 'a'
            gray_indices.append(jter)

        elif colors[jter] == 'y':
            letter_map[word[jter]][jter] = 'y'
            g_y_letters.append(word[jter])

        elif colors[jter] == 'g':
            letter_map[word[jter]][jter] = 'g'
            g_y_letters.append(word[jter])

        else:
            print("invalid color")

    # if there are no yellow or green positions for the same letter that is gray
    # then we can safely remove it from the map
    for i_gi in range(0, len(gray_indices)):

        letter_full_gray = True

        for i_gyl in range(0, len(g_y_letters)):

            # if the letter is gray and yellow or gray and green, then pass it
            if word[gray_indices[i_gi]] == g_y_letters[i_gyl]:

                letter_full_gray = False
                break

        # if letter is still full gray, then we can remove from map
        if letter_full_gray == True:
            if (word[gray_indices[i_gi]]) in letter_map:
                letter_map.pop(word[gray_indices[i_gi]])



def find_words(letter_map, the_words, num_tries):

    # testing variables
    no_req_letter = 0
    not_enough_req_letter = 0
    green_wrong = 0
    contains_letter_not_in_map = 0
    bad_yellow_gray_pos = 0

    # initialize variables
    new_words = list()
    req_letters = dict()

    # first, iterate through the map to find the required letters
    for elem in letter_map:

        # loop through the current word's color vector
        for the_color in letter_map[elem]:

            # add to set
            if (the_color == 'y') or (the_color == 'g'):

                # if the letter is not in map
                if elem in req_letters:
                    req_letters[elem] += 1
                else:
                    req_letters[elem] = 1

    # iterate through the words
    for i in range(0, len(the_words)):

        # assume word is valid until proven otherwise
        valid_word = True

        #first, iterate through the req_letters set and make sure it has all the needed letters
        if req_letters:

            # iterating through the required letters
            for curr_letter in req_letters:

                # assume letter is not there
                letter_found = False

                # iterating through the letters in the string to see if that letter is there
                for word_sec in the_words[i].string:

                    # if letter found, then set to true
                    if word_sec == curr_letter:
                        letter_found = True
                        break

                # if letter_found is still false, then this word is not valid
                # break and continue
                if letter_found == False:
                    valid_word = False
                    # print(the_words[i].string, "does not contain req letter")
                    break

                # if there is multiple of that letter, then we need to make sure that this word has the right amount
                if req_letters[curr_letter] > 1:

                    num_letters = 0

                    # iterate through the word to find the number of times that letter appears
                    for k in range(0, len(the_words[i].string)):
                        if the_words[i].string[k] == curr_letter:
                            num_letters += 1

                    # if letter does not appear enough, then word is not valid
                    if num_letters < req_letters[curr_letter]:
                        valid_word = False
                        # print(the_words[i].string, "doesn't have enough of req letter")
                        break

                # now, we need to make sure that if this req_letter is green, that it's in the right position
                # iterate through the letter_map to find if there is a green somewhere
                for j in range(0, len(letter_map[curr_letter])):

                    # if the color is green, then make sure that letter is at the position in the word
                    if letter_map[curr_letter][j] == 'g':

                        # test the word to see if it has that green letter at the correct spot
                        if not the_words[i].string[j] == curr_letter:
                            valid_word = False
                            # print(the_words[i].string, "has green in wrong spot")
                            break

                # breaks here if a test wasn't passed
                if valid_word == False:
                    break

        # if a word is still false, then continue on to analyze next word
        if valid_word == False:
            continue

        # Now, we need to test the position of each letter in the word
        # iterate through the word's letters
        for j in range(0, len(the_words[i].string)):

            curr_letter = the_words[i].string[j]

            # first make sure the letter is in the map
            if not curr_letter in letter_map:

                # if we are here, the the letter is not in the map
                # word is not valid anymore; set to false and break
                valid_word = False
                break

            # now, test against the letter_map
            # if gray or yellow IN THE SAME POSITION, then set to false and break
            if (letter_map[curr_letter][j] == 'y') or (letter_map[curr_letter][j] == 'a'):
                valid_word = False
                # print(the_words[i].string, "has green or yellow in wrong spot")
                break

        # if word is still true, then append to new words
        if valid_word == True:
            # print(the_words[i].string, "appended")
            new_words.append(the_words[i])

    # sorting the words
    if num_tries > 2:
        new_words.sort(key=get_common_rank)
    else:
        new_words.sort(reverse=True, key=get_info_rank)

    # get top choices
    top_choices = list()
    iterator = 1
    for choice in new_words:
        top_choices.append(choice)
        iterator += 1
        if (iterator > 10):
            break

    # return the words
    return top_choices, new_words



def get_info_rank(dummy):
    return dummy.info_rank



def get_common_rank(dummy):
    return dummy.common_rank
