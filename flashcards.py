#!/usr/local/bin/python3

from random import shuffle
import os
import glob
from sys import platform
# to ask questions
import inquirer
# to read csv
import csv
# to color print lines
from colorama import init as colorama_init, Fore, Back, Style
colorama_init()

if platform == 'win32':
  unused_variable = os.system("cls")
else:
  os.system('clear')

# Read in potential flashcard files
flashcards = (glob.glob("./flashcards/*.csv"))
flashcardDict = []
flashcardNames = []

for flashcard in flashcards:
  strSplit = flashcard.split("/")
  fileName = strSplit[len(strSplit) - 1]
  flashcard = { "name": fileName, "path": flashcard}
  flashcardDict.append(flashcard)
  flashcardNames.append(fileName)

# Choose between flashcard files
print("\n Hello! Use arrow keys to select a list of flashcards and press enter to continue.\n")
pickFlashcardsQuestion = [inquirer.List(
    'Flashcards',
    message="What would you like to study?",
    choices=flashcardNames,
)]
selectedFlashcards = inquirer.prompt(pickFlashcardsQuestion)['Flashcards']  # returns a dict
print(selectedFlashcards)

# Read in questions from csv
# file = csv.DictReader(open('./flashcards/aws-study-notes - Questions.csv'))
filePathIndex = next((index for (index, d) in enumerate(flashcardDict) if d["name"] == selectedFlashcards), None)
file = csv.DictReader(open(flashcardDict[filePathIndex]["path"]))
questions = []
for question in file:
  questions.append(question)

# Find all unique tags in flashcards
tags = []
for item in questions:
  # Transform tags in dictionary from comma separated string to a list of strings
  item['Tags'] = [x.strip() for x in item['Tags'].split(',')]
  tags = tags + item['Tags']

# Change tags to a set and back to a list to find unique tags
tags = list(set(tags))

# Beginning of user interface
print("\n Press space to select categories and press enter to continue.\nContinue pressing enter to cycle through the flashcards.\n")

pickTagsQuestion = [inquirer.Checkbox(
    'Tags',
    message="What would you like to study?",
    choices=['All Topics'] + tags,
)]
selectedTags = inquirer.prompt(pickTagsQuestion)['Tags']  # returns a dict

# Filter questions based on tags selected by user
if 'All Topics' not in selectedTags:
  questions = list(filter(lambda x: not set(x['Tags']).isdisjoint(selectedTags), questions))

# Loop through questions
shuffle(questions)
qLength = len(questions)
i = 0
try:
  while i < len(questions):
    print(Style.DIM + Fore.WHITE + '(' + str(i+1) + '/' + str(qLength) + ')' + ' ' + ', '.join(questions[i]['Tags']))
    input(Style.NORMAL + Fore.CYAN + questions[i]['Question'])
    input(Fore.GREEN + questions[i]['Answer'] + "\n")
    i+=1
except KeyboardInterrupt:
  print(Style.RESET_ALL)
  print("\nGood Luck on your test!\n")
  exit()

print(Style.RESET_ALL)
print("\nThat's all the question I have for you.\n")
good_luck = ''
with open("good_luck.txt", "r") as file:
    for line in file:
      good_luck += line
print(good_luck)
