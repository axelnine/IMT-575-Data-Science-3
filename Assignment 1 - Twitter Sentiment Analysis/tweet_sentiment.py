import json
import sys
import re


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
    This functions returns all the tweet text collected 
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
    '''
    This function scores and prints each tweet
    '''
    final_score = 0
    for word in list: 
        if word in sent_scores.keys():
            word = word.lower()
            final_score+=sent_scores[word]
        else:
            final_score+=0
    print(final_score)
    

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    sent_scores = get_term_sentiment_dictionary(sent_file)
    get_tweets(tweet_file,sent_scores)

if __name__ == '__main__':
    main()
