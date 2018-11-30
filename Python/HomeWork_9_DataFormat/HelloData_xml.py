import xml.etree.ElementTree as ET
import operator

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

# XML parsing
parser = ET.XMLParser(encoding="utf-8")
tree = ET.parse("newsafr.xml", parser=parser)

titles = []
root = tree.getroot()
xml_title = root.find("channel/title")
xml_items = root.findall("channel/item")
for xmli in xml_items:
    description = xmli.find("description").text.split()
    for word in description:
        if len(word) > word_length:
            words.append(word.lower())

words_popular = word_usage(words)
words_sorted = sorted(words_popular.items(), key=operator.itemgetter(1), reverse=True)
print('Список Top-{} самых популярный слов новостной ленты:'.format(top))
show_top(top, words_sorted)
