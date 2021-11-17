from text_analysis import Analysis
import pandas as pd


# initialise lists
positive_scores = []
negative_scores = []
polarity_scores = []
subjective_scores = []
average_sentence_lengths = []
complex_words_percentages = []
fog_indexes = []
average_words_per_sentences = []
complex_words_counts = []
words_counts = []
syllable_counts = []
personal_pronouns_counts = []
average_word_lengths = []



def read_input(file):
    # read input data
    data = pd.read_excel(file)
    return data


def get_scores(file):
    # loop through the urls and append the result to the lists
    for url in read_input(file)['URL']:
        analysis = Analysis(url, 'files/master_dictionary.xlsx')
        positive_scores.append(analysis.positive_score)
        negative_scores.append(analysis.negative_score)
        polarity_scores.append(analysis.polarity_score)
        subjective_scores.append(analysis.subjective_score)
        average_sentence_lengths.append(analysis.average_sentence_length)
        complex_words_percentages.append(analysis.complex_words_percentage)
        fog_indexes.append(analysis.fog_index)
        average_words_per_sentences.append(analysis.average_words_per_sentence)
        complex_words_counts.append(analysis.complex_words_count)
        words_counts.append(analysis.words_count)
        syllable_counts.append(analysis.syllable_count)
        personal_pronouns_counts.append(analysis.personal_pronouns_count)
        average_word_lengths.append(analysis.average_word_length)
        print(len(positive_scores))
    


def write_data(output_file="output.xlsx"):
    get_scores()    
    # read the output file    
    output_file = pd.read_excel('files/output.xlsx')
    # separate url and url id from the rest of the data
    url_dataframe = output_file[['URL_ID', 'URL']]
    # store the columns other than url and url id, to concatenate the two dataframes
    scores_dataframe = output_file.drop(url_dataframe.columns, axis=1)
    # convert the column names to list
    df_cols = scores_dataframe.columns.to_list()
    # zip all the lists, provide the column names and convert them to dataframe 
    result = pd.DataFrame(list(zip(positive_scores,negative_scores,polarity_scores,subjective_scores,average_sentence_lengths,
                            complex_words_percentages,fog_indexes,average_words_per_sentences,complex_words_counts,
                            words_counts,syllable_counts, personal_pronouns_counts, average_word_lengths)), columns=df_cols)

    # concatenate the scores and the url data
    output_data = pd.concat([url_dataframe, result], axis=1)
    # export the data as output_data.xlsx
    output_data.to_excel(output_file)
    
    
    
if __name__ == "__main__":
    data = get_scores('files/Input.xlsx')
    write_data()