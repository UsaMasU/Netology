import json
import operator
from pprint import pprint

top = 10
word_length = 6
words = []

def sort_by_alphabet(input_str):
    return input_str[0]

def sort_by_length(input_str):
    return len(input_str)

def show_top(top_number = 10, words_sorted = []):
    top_list = []
    for num, word_with_count in enumerate(words_sorted):
        if num > top_number - 1:
            break
        print(num+1, ' - ', word_with_count)
        top_list.append(word_with_count)
    return top_list

def word_usage(words):
    words_use = {}
    for word in words:
        count_use = words.count(word)
        words_use[word] = count_use
    return words_use

# JSON parsing
with open("newsafr.json", encoding='utf-8') as datafile:
    json_data = json.load(datafile)
news_items = json_data['rss']['channel']['items']
for description in news_items:
    sort_words = description['description'].split()
    sort_words.sort(key=sort_by_length, reverse=True)
    for word in sort_words:
        if len(word) > word_length:
            words.append(word.lower())

words_popular = word_usage(words)
words_sorted = sorted(words_popular.items(), key=operator.itemgetter(1), reverse=True)
print('Список Top-{} самых популярный слов новостной ленты:'.format(top))
show_top(top, words_sorted)

