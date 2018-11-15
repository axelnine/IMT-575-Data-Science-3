import sys
import re
import json 

state_dictionary = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'FL': 'Florida',
        'GA': 'Georgia',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MS': 'Mississippi',
        'NC': 'North Carolina',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin'
}

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
    '''
    states = {}
    state_freq = {}
    flag = 0
    for line in file:
        final_score = 0
        result = json.loads(line)
        
        #Get text
        str = result.get('text','NA')
        loc = result.get('place',None)
        if loc!=None:
            country_code = loc.get('country_code',None)
            state_abbreviation = loc.get('full_name',None)[-2:]
            if country_code == 'US':
                words = re.compile('\w+').findall(str)
                for word in words:
                    if word in sent_scores.keys():
                        final_score+=sent_scores[word]  
                    else:
                        final_score+=0
                flag = flag + 1
                
                state_fullname = state_dictionary.get(state_abbreviation,'NA')

                states[state_fullname] = final_score + states.get(state_fullname,0)
                state_freq[state_fullname] = state_freq.get(state_fullname,0) + 1
                list_of_words = re.compile('\w+').findall(str)
            
                final_score = 0
                for word in list_of_words: 
                    word = word.lower()
                    if word in sent_scores.keys():
                        final_score+=sent_scores[word]  
                    else:
                        final_score+=0
    return states,state_freq
            
def printStateScores(states,state_freq):
    '''
    Print happiest state scores.
    '''
    max_score = -99999 # dummy value for taking sum of scores of tweets for every state divided by total tweets from that state
    happiest_state = ''
    for state in state_dictionary.values():
        if(max_score < states[state]/state_freq[state]):
            max_score = states[state]/state_freq[state]
            happiest_state = state

    for key,state in state_dictionary.items():
        if state == happiest_state:
            happiest_state = key
        
    print("%s %f" % (happiest_state,max_score))
        
def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    sent_scores = get_term_sentiment_dictionary(sent_file)
    states,state_freq = get_tweets(tweet_file,sent_scores)
    printStateScores(states,state_freq)
    
if __name__ == '__main__':

    main()
