#!/usr/bin/env python3

import csv
import sys
import os
import random
import webbrowser

random.seed()

data = []

for i in csv.reader(open("info.csv")):
    data.append(i)

score=0
review_words=[]
result_file = "results.txt"

def usage(status=0):
    print(f'''Usage: {os.path.basename(sys.argv[0])} [flags]
    -o     Run quiz in order
    -s     Save results
    -l N   Change length of quiz to N (default is 5)
    -t     Answer questions in target language
    -f str Will search the database for the word
    -a     Open a website that allows you to listen for natural audio
    -ai    Open a website that allows you to listen to ai generated audio
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
            print(f"\tIncorrect, \"{data[index][1]}\"")
            if data[index] not in review_words:
                review_words.append(data[index])
    if target == False:
        answer = input(f"\tWhat is \"{data[index][1]}\" in English?\n\t")
        if answer.lower() == data[index][2].lower():
            print("\tCorrect!")
            score+=1
        else:
            print(f"\tIncorrect, \"{data[index][2]}\"")
            if data[index] not in review_words:
                review_words.append(data[index])

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

def quiz(ordered=False, save=False, target=False, audio=False, audio_ai=False, length = 5) -> None:
    i = 0
    
    while (i < length):
        if (ordered == True):
            question(i+1, length, i, target)
            open_audio(audio, audio_ai, data[i][1])
        else:
            index = random.randint(0,999)
            question(i+1, length, index, target)
            open_audio(audio, audio_ai, data[index][1])
        i+=1
    
    if save == True:
        for index, m in enumerate(results(length)):
            print(m)
            if index == 0:
                continue
            with open(result_file, "a") as f:
                f.write(m + '\n')

def search(word: str):
    if any(word in sublist for sublist in data):
        print(f"\n\"{word}\" is in the database\n")
    else:
        print(f"\n\"{word}\" is not in the database\n")
def main(arguments=sys.argv[1:], stream=sys.stdin) -> None:
    # Parse command-line options

    ordered = False
    save = False
    target = False
    length = 5
    searcher = False
    audio = False
    audio_ai = False
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
        elif argument == '-h':
            usage(0)
        else:
            usage(1)

    if searcher == True:
        search(keyword)

    quiz(ordered, save, target, audio, audio_ai, length)
    

if __name__ == '__main__':
    main()