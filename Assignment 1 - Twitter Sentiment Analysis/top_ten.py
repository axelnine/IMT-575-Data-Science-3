import sys
import re
import json

hashtag_dict={}

def top_ten_hashtags(file):
    '''
    This function extracts the hashtag frequency for a set of tweets
    '''
    for line in file:

        result = json.loads(line)
        hashtag_object = result.get('entities','NA')
        
        if hashtag_object != 'NA':
            hashtags = hashtag_object.get('hashtags',None)
            if hashtags != None:
                for i in range(0,len(hashtags)):
                    hashtag = hashtags[i].get('text')
                    hashtag_dict[hashtag] = int(hashtag_dict.get(hashtag,0))+1
    
    return hashtag_dict

def print_hashtags(hashtag_dict):
    '''
    Print the top ten hashtags
    '''
    sorted_hashtag_dict =  sorted(hashtag_dict.items(), key=lambda t: t[1], reverse = True)
    
    for i in range(10):
        hashtag,count = sorted_hashtag_dict[i]
        print(hashtag, count)

def main():
    tweet_file = open(sys.argv[1])
    top_ten_hashtags(tweet_file)
    print_hashtags(hashtag_dict)

if __name__ == '__main__':

    main()
    