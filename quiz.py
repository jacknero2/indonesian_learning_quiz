#!/usr/bin/env python3

import csv
import sys
import os
import random
import webbrowser
import pandas

random.seed()

data = []

for i in csv.reader(open("info.csv")):
    data.append(i)

score=0
review_words=[]
result_file = "results.txt"
mnemonic_file = "mnemonics.csv"

mnemonics = []

with open(mnemonic_file, "a") as f:
    pass

for i in csv.reader(open("mnemonics.csv")):
    mnemonics.append(i)

def usage(status=0):
    print(f'''Usage: {os.path.basename(sys.argv[0])} [flags]
    -o     Run quiz in order
    -s     Save results
    -l N   Change length of quiz to N (default is 5)
    -t     Answer questions in target language
    -f str Will search the database for the word
    -a     Open a website that allows you to listen for natural audio
    -ai    Open a website that allows you to listen to ai generated audio
    -m     Give the opportunity to add to the mnemonic database
    -c N   Specify the number of cycles through your words
''')
    sys.exit(status)

def question(question_num: int, length: int, index: int, target=False):
    global score
    print(f"{question_num}/{length}")
    if target == True:
        answer = input(f"\tWhat is \"{data[index][2]}\" in Indonesian?\n\t")
        if answer.lower() == data[index][1].lower():
            print("\tCorrect!")
            score+=1
        else:
            response = random.randint(1,3)
            if response == 1:
                print(f"\tIncorrect, \"{data[index][1]}\" is the correct answer...")
            if response == 2:
                print(f"\tIncorrect, \"{data[index][1]}\" is the right choice...")
            if response == 3:
                print(f"\tIncorrect, \"{data[index][1]}\" is correct, like are you even trying...?")
            if data[index] not in review_words:
                review_words.append(data[index])
    if target == False:
        answer = input(f"\tWhat is \"{data[index][1]}\" in English?\n\t")
        if answer.lower() == data[index][2].lower():
            print("\tCorrect!")
            score+=1
        else:
            response = random.randint(1,3)
            if response == 1:
                print(f"\tIncorrect, \"{data[index][2]}\" is the correct answer...")
            if response == 2:
                print(f"\tIncorrect, \"{data[index][2]}\" is the right choice...")
            if response == 3:
                print(f"\tIncorrect, \"{data[index][2]}\" is correct, like are you even trying...?")
            if data[index] not in review_words:
                review_words.append(data[index])

def search(word: str, data: list)->list:
    indexes = [index for index, sublist in enumerate(data) if word in sublist]
    if len(indexes) == 0:
        return [False, []]
    else:
        return [True, data[indexes[0]], indexes]

def add_mnemonic(word: str):
    search_result = search(word, mnemonics)
    if not search_result[0]:
        with open(mnemonic_file, "a") as f:
            menumonic_to_add = input(f"\tEnter your mnemonic for \"{word}\": ")
            f.write(f"{word},{menumonic_to_add}\n")
    else:
        print()
        print(f"\tYour mnemonic for \"{word}\" is \"{search_result[1][1]}\"")
        change = input("\tWould you like to change this mnemonic to something else? (y/n): ")
        if change.lower() == 'y':

            information = pandas.read_csv(mnemonic_file, header=None, names=['word','mnemonic'])
            information.loc[search_result[2][0], 'mnemonic'] = input(f"\tMnemonic for{word}: ")
            information.to_csv(mnemonic_file, index=False) 
            print("\tUpdated!")
    print()

def results(length: int) ->list:
    result_list = []
    result_list.append("\nResults")
    result_list.append(f"\tLength of quiz: {length} questions")
    result_list.append(f"\tScore: {score}/{length}")
    result_list.append("\tReview words:")
    for i in review_words:
        result_list.append(f"\t\t{i[1]} : {i[2]}")
    return result_list

def open_audio(audio: bool, audio_ai: bool, word: str) -> None:
    url2 = f"https://www.howtopronounce.com/indonesian/{word}"
    url1 = f"https://forvo.com/word/{word}/#ind"
    if audio:
        webbrowser.open(url1)
    if audio_ai:
        webbrowser.open(url2)

def quiz(ordered=False, save=False, target=False, audio=False, audio_ai=False, mnemonic=False, cycles=1, length = 5) -> None:
    w = 0

    while w < cycles:
        print("--------------------------------")
        print(f"Cycle {w + 1}")
        print("--------------------------------")
        i = 0
        
        while (i < length):
            if (ordered == True):
                question(i+1, length, i, target)
                open_audio(audio, audio_ai, data[i][1])
                if mnemonic:
                    add_mnemonic(data[i][1])
            else:
                index = random.randint(0,999)
                question(i+1, length, index, target)
                open_audio(audio, audio_ai, data[index][1])
                if mnemonic:
                    add_mnemonic(data[index][1])
            i+=1
        w+=1
    if save == True:
        for index, m in enumerate(results(length)):
            print(m)
            if index == 0:
                continue
            with open(result_file, "a") as f:
                f.write(m + '\n')
    

def main(arguments=sys.argv[1:], stream=sys.stdin) -> None:
    # Parse command-line options

    ordered = False
    save = False
    target = False
    length = 5
    searcher = False
    audio = False
    audio_ai = False
    mnemonic = False
    cycles = 1
    keyword = ""

    while arguments:
        argument = arguments.pop(0)
        if argument == '-o':
            ordered = True
        elif argument == '-s':
            save = True
        elif argument == '-t':
            target = True
        elif argument == '-l':
            length = int(arguments.pop(0))
        elif argument == '-f':
            searcher = True
            keyword = arguments.pop(0)
        elif argument == '-a':
            audio = True
        elif argument == '-ai':
            audio_ai = True
        elif argument == '-m':
            mnemonic = True
        elif argument == '-c':
            cycles = int(arguments.pop(0))
        elif argument == '-h':
            usage(0)
        else:
            usage(1)

    if searcher == True:
        if search(keyword, data)[0]:
            print(f"\"{keyword}\" is in the database")
        else:
            print(f"\"{keyword}\" is not in the database")

    quiz(ordered, save, target, audio, audio_ai, mnemonic, cycles, length)
    

if __name__ == '__main__':
    main()