import sys
import re
import json

new_terms = {}   

def get_term_sentiment_dictionary(file):
    '''
    This function reads into a dictionary all sentiment scores from AFINN-111
    '''
    sent_scores = {}
    for line in file:
        term,sent_score = line.split("\t")
        sent_scores[term] = int(sent_score)
    return sent_scores

def get_tweets(file,sent_scores):
    '''
    This function returns the tweet text from our collection
    '''
    for line in file:

        result = json.loads(line)
        
        #Get text
        str = result.get('text','NA')

        #Remove mentions & hyperlinks
        str = re.sub(r'@[A-Za-z0-9_]+','',str)
        str = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', str, flags=re.MULTILINE)
        str = re.sub(r'RT :','',str)
        
        list_of_words = re.compile('\w+').findall(str)
        get_score(list_of_words,sent_scores)

   
def get_score(list,sent_scores):
    """
    This function scores new words

    Methodology: Average sentiment of all tweets containing that word
    """
    final_score = 0
    for word in list: 
        word = word.lower()
        if word in sent_scores.keys():
            final_score+=sent_scores[word]  
        elif word not in sent_scores.keys():
            if word not in new_terms:
                new_terms[word] = [final_score]
            else:
                new_terms[word].append(final_score)
            final_score+=0

def display_words(new_terms):
    """
    This function displays all new words and their associated sentiments. 
    """
    new_term_scores = {}
    for term, sentiment in new_terms.items():
        new_term_scores[term] = sum(sentiment) / len(sentiment)
    
    for new_term, score in new_term_scores.items():
        print(new_term, score)


def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    sent_scores = get_term_sentiment_dictionary(sent_file)
    get_tweets(tweet_file,sent_scores)
    display_words(new_terms)


if __name__ == '__main__':

    main()
