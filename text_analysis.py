import requests
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import pandas as pd


class Extraction():
    def __init__(self, url):
        self.url = url
        self.stop_words = self.get_stop_words()
        self.post = self.get_post()
        self.positive_words = self.extract_positive_words()
        self.negative_words = self.extract_negative_words()
        self.post_tokens = self.tokenize()
        self.clean_post_tokens = self.clean_tokens()


    # def read_data(self, file):
    #     """function to read excel data and return the dataframe"""
    #     data = pd.read_excel(file)
    #     return data


    def get_stop_words(self):
        """function to read stop words from stop_words.txt and return a list
        that contains stop words"""
        stop_words_list = []
        with open('files/stop_words.txt', 'r') as f:
            stop_words_list.extend(f.read().split('\n'))
        return stop_words_list


    def extract_html(self):
        """function to extract article's html content
        and give the html to extract_text() for extraction of text
        from the html"""
        url = str(self.url)
        res = requests.get(url, headers={"User-Agent": "XY"})
        html = res.content
        return self.extract_text(html)


    def extract_text(self, html):
        """function to extract article's title and post text from
        the html"""
        post = ""

        # parse html
        soup = BeautifulSoup(html, 'html.parser')

        # extract heading text
        for heading in soup.find_all('h1', class_='entry-title'):
            post_title = heading.get_text()

        # extract post content
        for paragraph in soup.find_all('div', class_='td-post-content'):
            # check and remove if there is a pre tag
            if paragraph.pre:
                paragraph.pre.decompose()

            post_text = paragraph.get_text()

        # append post title and post text in a single string
        post = post_title + '\n' + post_text

        return post


    def get_post(self):
        """function to return post with title and text as string"""
        return self.extract_html()


    def tokenize(self):
        """function to tokenize the post and return the tokenized word's list"""
        word_tokens = word_tokenize(self.post.replace('\n', ' '))
        return word_tokens


    def clean_tokens(self):
        """function to clean the tokens list by removing puntuations and the stop words
        """
        stop_words_ = set(stopwords.words('english'))
        stop_words = set(self.stop_words)
        # clean words by removing stop words from the word tokens
        filtered_words_with_punctuations = [
            word for word in self.post_tokens if not word.lower() in stop_words]
        # remove the punctuation marks
        filtered_words_without_punctuations = [
            word.lower() for word in filtered_words_with_punctuations if word.isalnum()]
        return filtered_words_without_punctuations


    def extract_positive_words(self):
        """function to extract positive words list from the master dictionary file"""
        positive_list = []
        with open('files/positive_words.txt', 'r') as f:
            positive_list.extend(f.read().split('\n'))
        positive = [str(word).lower() for word in positive_list]
        positive = [word for word in positive if word not in self.stop_words]
        return positive


    def extract_negative_words(self):
        """function to extract negative words from the master dictionary file"""
        negative_list = []
        with open('files/negative_words.txt', 'r') as f:
            negative_list.extend(f.read().split('\n'))
        negative = [str(word).lower() for word in negative_list]
        negative = [word for word in negative if word not in self.stop_words]
        return negative




class Analysis(Extraction):
    def __init__(self, data):
        self.extract = Extraction(data)
        self.stop_words = self.extract.stop_words
        self.post_tokens = self.extract.post_tokens
        self.clean_post_tokens = self.extract.clean_post_tokens
        self.positive_words = self.extract.positive_words
        self.negative_words = self.extract.negative_words
        self.post = self.extract.post
        self.positive_score = self.calculate_positive_score()
        self.negative_score = self.calculate_negative_score()
        self.polarity_score = self.calculate_polarity_score()
        self.subjective_score = self.calculate_subjective_score()
        self.average_sentence_length = self.average_sentence_length()
        self.complex_words_count = self.complex_words_count()
        self.complex_words_percentage = self.complex_words_percentage()
        self.fog_index = self.fog_index()
        self.average_words_per_sentence = self.average_sentence_length
        self.words_count = self.clean_word_count()
        self.syllable_count = self.syllable_count_per_word()
        self.personal_pronouns_count = self.personal_pronouns_count()
        self.average_word_length = self.average_word_length()


    def calculate_positive_score(self):
        """function to calculate the positive score of the post
        which can be calculate by counting the positive words present
        in the post"""
        positive_score = 0

        for word in self.clean_post_tokens:
            if word in self.positive_words:
                positive_score += 1

        return positive_score


    def calculate_negative_score(self):
        """function to calculate negative score of the post
        which can be calculate by counting the negative words present
        in the post"""
        negative_score = 0

        for word in self.clean_post_tokens:
            if word in self.negative_words:
                negative_score += 1

        return negative_score


    def calculate_polarity_score(self):
        """function to calculate polarity score
        POLARITY SCORE = (POSITIVE SCORE - NEGATIVE SCORE) / ((POSITIVE SCORE + NEGATIVE SCORE) + 0.0000001)"""
        polarity_score = (self.positive_score - self.negative_score) / \
            ((self.positive_score + self.negative_score) + 0.000001)
        return polarity_score


    def calculate_subjective_score(self):
        """FUNCTION TO CALCULATE SUBJECTIVE SCORE
        SUBJECTIVE SCORE = (POSITIVE SCORE + NEGATIVE SCORE) / (TOTAL WORDS AFTER CLEANING + 0.000001)"""
        subjectivity_score = (self.positive_score + self.negative_score) / \
            (len(self.clean_post_tokens) + 0.000001)
        return subjectivity_score


    def average_sentence_length(self):
        """FUNCTION TO CALCULATE AVERAGE SENTENCE LENGTH
        AVERAGE SENTENCE LENGTH = NUMBER OF WORDS / NUMBER OF SENTENCES"""
        sentence = self.post.split('\n')
        sentence_tokens = []
        for tokens in sentence:
            sentence_tokens.extend(sent_tokenize(tokens))

        average_sentence_length = len(
            self.clean_post_tokens) / len(sentence_tokens)
        return average_sentence_length


    def complex_words_percentage(self):
        """FUNCTION TO CALCULATE COMPLEX WORDS PERCENTAGE
        COMPLEX WORDS PERCENTAGE = NUMBER OF COMPLEX WORDS / NUMBER OF WORDS"""
        percentage_of_complex_words = (
            self.complex_words_count / len(self.clean_post_tokens)) * 100
        return round(percentage_of_complex_words, 2)


    def complex_words_count(self):
        """FUNCTION TO FIND THE NUMBER OF COMPLEX WORDS"""
        complex_words_count = 0
        for word in self.clean_post_tokens:
            result = self.is_complex(word)
            complex_words_count += result
        return complex_words_count


    def is_complex(self, word):
        """FUNCTION TO FIND WHETHER A NUMBER IS COMPLEX OR NOT"""
        syllable = self.syllable_count(word)
        if syllable > 2:
            return 1
        else:
            return 0


    def syllable_count(self, word):
        """FUNCTION TO FIND THE NUMBER OF SYLLABLES IN A WORD"""
        syllable = 0
        for vowel in ['a', 'e', 'i', 'o', 'u']:
            syllable += word.count(vowel)
        for ending in ['es', 'ed', 'e']:
            if word.endswith(ending):
                syllable -= 1
        if word.endswith('le'):
            syllable += 1

        return syllable


    def fog_index(self):
        """FUNCTION TO CALCULATE FOG INDEX
        FOG INDEX = 0.4 * (AVERAGE SENTENCE LENGTH + PERCENTAGE OF COMPLEX WORDS)"""
        fog_index = 0.4 * (self.average_sentence_length +
                           self.complex_words_percentage)
        return fog_index


    def clean_word_count(self):
        """FUNCTION TO FIND THE NUMBER OF CLEAN WORDS PRESENT IN A POST AFTER REMOVING STOP WORDS"""
        clean_words = list()

        for word in self.clean_post_tokens:
            if word not in self.stop_words and word.isalnum():
                clean_words.append(word)

        clean_words_count = len(clean_words)
        return clean_words_count


    def syllable_count_per_word(self):
        """FUNCTION TO FIND THE NUMBER OF SYLLABLE PER WORD"""
        vowels = ['a', 'e', 'i', 'o', 'u']

        syllable_count = 0

        for vowel in vowels:
            for word in self.clean_post_tokens:
                if not (word.endswith('es') or word.endswith('ed')):
                    count = word.lower().count(vowel)
                    syllable_count += count

        return syllable_count


    def personal_pronouns_count(self):
        """FUNCTION TO FIND THE NUMBER OF PERSONAL PRONOUNS PRESENT IN THE POST"""
        personal_pronouns = ['I', 'we', 'We',
                             'my', 'My', 'ours', 'Ours', 'us', 'Us']

        personal_pronouns_count = 0

        for pronoun in personal_pronouns:
            count = self.post_tokens.count(pronoun)
            personal_pronouns_count += count

        return personal_pronouns_count


    def average_word_length(self):
        """FUNCTION TO CALCULATE AVERAGE WORD LENGTH
        AVERAGE WORD LENGTH = SUM OF TOTAL NUMBER OF CHARACTERS PRESENT IN A WORD / TOTAL NUMBER OF WORDS"""
        total_characters = []
        for word in self.post_tokens:
            for character in word:
                total_characters.append(character)

        average_word_length = len(total_characters) / len(self.post_tokens)
        return average_word_length
