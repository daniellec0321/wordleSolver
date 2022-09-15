#!/usr/bin/python3

from Word import Word
from Pair import Pair



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



# initializes the positions list
def init_positions(positions):
    
    # append to the list five times
    for i in range(0, 5):
        positions.append({'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'})



"""
# updates letter map with the info from the user's guess
def update_positions(word, colors, positions, req_letters):
    
    # fix word and colors to be lowercase
    word = word.lower()
    colors = colors.lower()

    # create a temporary dictionary and counter to deal with duplicates
    temp = dict()
    num_letter_count = dict()

    # iterate through word and color
    for i in range(0, 5):
        
        # add to true letter count
        if word[i] in num_letter_count:
            num_letter_count[word[i]] += 1
        else:
            num_letter_count[word[i]] = 1
        
        # if color is green or yellow, add to req letters and temp dict
        if colors[i] == 'y' or colors[i] == 'g':

            # initialize pair
            tPair = Pair()
            tPair.first = 1
            tPair.second = False
            req_letters[word[i]] = tPair

            if word[i] in temp:
                temp[word[i]] += 1
            else:
                temp[word[i]] = 1

            # updating req letters to reflect temp
            req_letters[word[i]].first = temp[word[i]]

            # now update positions, if its yellow
            if colors[i] == 'y':
                
                # delete from positions at that spot
                if word[i] in positions[i]:
                    positions[i].remove(word[i])

            # update positions if its green
            if colors[i] == 'g':

                # delete everything BUT that letter from positions
                positions[i].clear()

                # add that letter to positions
                positions[i].add(word[i])

        # if a color is gray and not in req letters, remove it from every set in positions
        if colors[i] == 'a' and word[i] not in req_letters:

            for j in range(0, 5):

                # remove from set
                if word[i] in positions[j]:
                    positions[j].remove(word[i])
"""



# updates letter map with the info from the user's guess
def update_positions(word, colors, positions, req_letters):

    # reset req_letters
    req_letters.clear()
    
    # fix word and colors to be lowercase
    word = word.lower()
    colors = colors.lower()

    # keep track of letters and their color
    yg = dict()
    a = dict()

    # iterate through word and color
    for i in range(0, 5):

        if colors[i] == 'y' or colors[i] == 'g':
            if word[i] in yg:
                yg[word[i]] += 1
            else:
                yg[word[i]] = 1

        else:
            if word[i] in a:
                a[word[i]] += 1
            else:
                a[word[i]] = 1

    # iterate through yg letters
    for letter in yg:
        
        # if letter is in a, THEN ADD A LOCK
        if letter in a:
            
            tPair = Pair()
            Pair.first = yg[letter]
            Pair.second = True
            req_letters[letter] = tPair

        # do not have a lock otherwise
        else:
            
            tPair = Pair()
            Pair.first = yg[letter]
            Pair.second = False
            req_letters[letter] = tPair

    # updating positions
    for i in range(0, 5):
        
        # if color is green
        if colors[i] == 'g':
            positions[i].clear()
            positions[i].add(word[i])

        # if color is yellow
        if colors[i] == 'y':
            if word[i] in positions[i]:
                positions[i].remove(word[i])

        # if color is gray
        if colors[i] == 'a':

            # check that it is not in yg
            if not word[i] in yg:

                # remove from every set
                for j in range(0, 5):

                    # remove from set
                    if word[i] in positions[j]:
                        positions[j].remove(word[i])

            # otherwise, just remove from that set
            else:
                positions[i].remove(word[i])
            
        


# iterate through available words and find what we can play
def find_words(the_words, positions, req_letters, num_tries):

    # the list we will return
    r = list()

    # iterate through the words
    for word in the_words:

        valid_word = True

        # create a temp dict for this current word
        temp = dict()
        for letter in word.string:
            
            # add to dict
            if letter in temp:
                temp[letter] += 1
            else:
                temp[letter] = 1

        # test this dictionary against req letters
        for letter in req_letters:

            # first, test if this temp dict even has that letter
            if letter not in temp:
                valid_word = False
                break

            # if the letter exists, then they must also have correct amount
            else:
                if temp[letter] < req_letters[letter].first:
                    valid_word = False
                    break

                # check for lock
                if req_letters[letter].second == True:
                    if temp[letter] != req_letters[letter].first:
                        valid_word = False
                        break

        # if word is false, continue
        if valid_word == False:
            continue

        # now, test the word against positions
        for i in range(0, 5):
            
            # if that letter is not in the positions vector
            if word.string[i] not in positions[i]:

                # set to false and break
                valid_word = False
                break

        # if word is still true, add to new list
        if valid_word == True:
            r.append(word)

    # sort the list and give back the top choices
    # if num_tries > 2:
        # r.sort(key=get_common_rank)
    # else:
        # r.sort(reverse=True, key=get_info_rank)

    # create duplicate list to sort
    r1 = list()
    for word in r:
        r1.append(word)

    # sort the lists
    r.sort(reverse=True, key=get_info_rank)
    r1.sort(key=get_common_rank)

    # create the top choices list
    iter = 0
    top_choices = list()
    top_choices1 = list()

    for word in r:
        top_choices.append(word)
        iter += 1
        
        if iter >= 5:
            break

    iter = 0
    for word in r1:
        top_choices1.append(word)
        iter += 1
        
        if iter >= 5:
            break

    return top_choices, top_choices1, r



def get_info_rank(dummy):
    return dummy.info_rank



def get_common_rank(dummy):
    return dummy.common_rank

# initiate variables
the_words = list()
top_choices = list()
top_choices1 = list()
read_file(the_words)

print(len(the_words), "possible words")

req_letters = dict()
positions = list()
init_positions(positions)

num_tries = 1

while (1):
    
    word = input('Enter the word: ')
    colors = input('Enter the colors: ')

    update_positions(word, colors, positions, req_letters)

    num_tries += 1

    top_choices, top_choices1, the_words = find_words(the_words, positions, req_letters, num_tries)

    print(len(the_words), "possible words")

    print("\nBest choice:")
    if len(the_words) < 100:
        print(top_choices1[0].string)
    else:
        print(top_choices[0].string)

    print("\nBest info words:")
    for word in top_choices:
        print(word.string)

    print("\nBest common words:")
    for word in top_choices1:
        print(word.string)

    print(" ")
