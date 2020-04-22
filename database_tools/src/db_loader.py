import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import pandas as pd
import configparser
import os
import random
import re

class Loader:
    """
    A data loader used to track data
    transfers from files to python objects.
    """
    config = configparser.ConfigParser()
    data_frame = pd.DataFrame()
    
    def __init__(self):
        self.config.read('db_loader.config')
        self.config.sections()

    def DataFrame_to_List(self, frame):
        frame_list = [str(row) for row in frame]
        return frame_list

class TrainingDataLoader(Loader):
    """
    A data loader for transferring
    excel file content to yaml files.
    """
    excel_file = ""
    yaml_file = ""
    questions = []
    answers = []
    
    def __init__(self):
        Loader.__init__(self)
        if 'DEFAULT' in self.config:
            self.excel_file = self.config['DEFAULT']['TrainingFileXLSX']
            self.yaml_file = self.config['DEFAULT']['TrainingFileYML']
            self.data_frame = pd.read_excel(self.excel_file)

    def get_column(self, column_name):
        column = self.data_frame[column_name].tolist()
        items = [item for item in column if item]
        return items

    def load(self):
        self.questions = self.get_column("question")
        self.answers = self.get_column("answer")
        self.questions = self.DataFrame_to_List(self.questions)
        self.answers = self.DataFrame_to_List(self.answers)

    def write_to_yaml(self, category_name):
        path = Path('../../ChatBot') / 'responses' / '{}.yml'.format(category_name)
        with open(path, "wb+") as file:
            self.write_yaml_header(file, category_name)
            self.write_to_yaml_items(file, self.questions, self.answers)

    def write_lemmatized(self, category_name):
        path = Path('../../ChatBot') / 'responses' / '{}_lemmatized.yml'.format(category_name)
        with open(path, "wb+") as file:
            self.write_yaml_header(file, category_name)
            self.write_to_yaml_items(file, self.lemmatize(), self.answers)

    def write_stemmed(self, category_name):
        path = Path('../../ChatBot') / 'responses' / '{}_stemmed.yml'.format(category_name)
        with open(path, "wb+") as file:
            self.write_yaml_header(file, category_name)
            self.write_to_yaml_items(file, self.stem(), self.answers)

    def write_yaml_header(self, file, category_name):
        file.write("categories:\n".encode("ascii"))
        category_header = "- " + category_name + "\n\n"
        category_header = category_header.encode("ascii")
        file.write(category_header)
        file.write("conversations:\n".encode("ascii"))

    def write_to_yaml_items(self, file, questions, answers):
        for q, a in zip(questions, answers):
            q = self.filter_symbols(str(q))
            a = self.filter_symbols(str(a))
            a = self.filter_href_multiline(str(a))
            self.write_to_yaml_item(file, "- - ", q)
            self.write_to_yaml_item(file, "  - ", a)
            file.write("\n".encode("ascii"))

    def write_to_yaml_item(self, file, prefix, item_text):
        if RepresentsInt(item_text):
            item = prefix + "'" + item_text + "'" + "\n"
            item = item.encode("ascii")
            file.write(item)
        else:
            item = prefix + item_text + "\n"
            item = item.encode()
            file.write(item)

    def shuffle_phrase(self, q):
        graphemes = q.split()
        random.shuffle(graphemes)
        q = " ".join(graphemes)
        return q

    def filter_symbols(self, phrase):
        phrase = re.sub('-[<>\'`#^]+', '', phrase)
        return phrase

    def filter_href_multiline(self, phrase):
        href = re.findall('https://.*[^\s]*\s', phrase)
        if not href:
            return phrase
        else:
            phrase = ' '.join(phrase.split())
            return phrase

    def shuffle_questions(self):
        shuffled = map(lambda q: self.shuffle_phrase(q), self.questions)
        self.questions = shuffled

    def lemmatize(self):
        import string
        from nltk.stem import WordNetLemmatizer

        lemmatizer = WordNetLemmatizer() 
        table = str.maketrans('', '', string.punctuation)
        qs = self.questions
        new_qs = []

        for q in qs:
            q = q.replace("/", " ")
            q = q.replace("-", " ")
            q = re.sub('[</\?!@&%$()>\'`#^]', ' ', q)
            new_q = str.translate(q, table).split()
            new_q = [lemmatizer.lemmatize(w) for w in new_q]
            new_q = " ".join(new_q)
            new_qs.append(new_q)
        
        return new_qs

    def stem(self):
        import string
        from nltk.stem.snowball import SnowballStemmer
        from nltk.tokenize import word_tokenize

        ss = SnowballStemmer("english", ignore_stopwords=True)
        table = str.maketrans('', '', string.punctuation)
        qs = self.questions
        new_qs = []

        for q in qs:
            q = q.replace("/", " ")
            q = q.replace("-", " ")
            q = re.sub('[</\?!@&%$()>\'`#^]', ' ', q)
            new_q = word_tokenize(q)
            new_q = [ss.stem(w) for w in new_q]
            new_q = " ".join(new_q)
            new_qs.append(new_q)
        
        return new_qs

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def main():
    training_loader = TrainingDataLoader()
    training_loader.load()
    training_loader.write_to_yaml("russ_college")
    training_loader.write_lemmatized("russ_college")
    training_loader.write_stemmed("russ_college")

if __name__ == "__main__":
    main()
