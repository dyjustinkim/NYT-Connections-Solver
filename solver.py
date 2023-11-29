from bs4 import BeautifulSoup
import requests
import string
import json
from collections import Counter


def find_counter(word):
    link = "https://en.wikipedia.org/wiki/" + word 
    page = requests.get(link)
    soup = BeautifulSoup(page.text, "html.parser")
    f = open('common_words.json')
    common_words = json.load(f)

    body = soup.find_all("p")
    word_list = []
    for paragraphs in body:
        text = paragraphs.getText()
        all_words = text.translate(str.maketrans('', '', string.punctuation + "0123456789" + "–")).lower().split()
        list_x = [word for word in all_words if word not in common_words]
        word_list.extend(list_x)


    return Counter(word_list)

def compare_counters(countera, counterb):

    shared_words = list(filter(lambda x: x in countera, counterb))
    if type(list(countera.values())[0]) == int:
        new_counter = dict([(word, (countera[word], counterb[word])) for (word, freq) in countera.items() if word in shared_words])
    else:
        new_counter = dict([(word, (countera[word][0], countera[word][1], counterb[word][0], counterb[word][1])) 
                            for (word, freq) in countera.items() if word in shared_words and sum(countera[word]) + sum(counterb[word]) > 7])
    new_counter = dict(sorted(new_counter.items(), key=lambda x:sum(x[1])))
    return(new_counter)

def enter_four_words():
    val = input("Enter four words: ")
    words = val.lower().split(", ")
    for i, word in enumerate(words):
        words[i] = word.replace(" ", "_") 
    comparea = (compare_counters(find_counter(words[0]), find_counter(words[1])))
    compareb = (compare_counters(find_counter(words[2]), find_counter(words[3])))
    comparec = (compare_counters(comparea, compareb))
    for x in comparec:
        print(x, comparec[x])
    print(len((comparec)))

enter_four_words()