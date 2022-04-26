#!/usr/bin/python3

from flask import Flask, render_template, request
import socket

app = Flask(__name__)
base = 'index.html'

# importing my classes
import Word
import funcs

# global variables
the_words = list()
letter_map = dict()
num_tries = 0



def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]

    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP



@app.route("/")
def index():
    global the_words
    global letter_map
    global num_tries

    guesses, the_words = funcs.find_words(letter_map, the_words, num_tries)
    num_tries += 1

    if (len(guesses) == 0):
        return reset()

    return render_template(base, guesses=guesses, haveGuesses=(len(guesses)>0))



@app.route("/submitGuess", methods=["POST"])
def submitGuess():
    global num_tries
    global letter_map
    global the_words

    num_tries += 1
    guess = request.form["guess"]
    colors = request.form["colors"]

    if not guess or not colors:
        return index()

    guess = guess.rstrip()
    colors = colors.rstrip()
    
    # reset letter map
    letter_map.clear()
    funcs.init_letter_map(letter_map)

    # updating the letter map
    funcs.update_letter_map(guess, colors, letter_map)
    # top_choices, the_words = funcs.find_words(letter_map, the_words, num_tries)

    return index()



@app.route("/reset")
def reset():
    global num_tries
    global the_words
    global letter_map

    num_tries = 0
    the_words.clear()
    letter_map.clear()
    funcs.init_letter_map(letter_map)
    funcs.read_file(the_words)

    return index()



def main():
    global num_tries
    global the_words
    global letter_map

    funcs.read_file(the_words)
    funcs.init_letter_map(letter_map)

    app.run(host=getIP(), port=80)
    pass



if __name__ == "__main__":
    main()
