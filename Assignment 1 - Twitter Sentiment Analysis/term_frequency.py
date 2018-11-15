import json
import sys
import re

instance = {}
count = 0

def get_term_frequency(file):
    '''

    '''
    global count
    for line in file:
        
        result = json.loads(line)

        #Get text
        str = result.get('text','NA')

        #Remove mentions & hyperlinks
        str = re.sub(r'@[A-Za-z0-9_]+','',str)
        str = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', str, flags=re.MULTILINE)
        str = re.sub(r'RT :','',str)

        
        list_of_words = re.compile('\w+').findall(str)
        
        #Get counts
        for word in list_of_words:
            word = word.lower()
            instance[word] = instance.get(word,0) + 1
            count = count + 1

def print_frequency():

    #print("\nPrinting only the high frequency words with term_frequency > 0.003:\n")
    
    for key,value in instance.items():
        #if(value/count>0.0003):
            #print('sd')
        print("%s %0.9f" % (key, value/count))
        
def main():
    
    tweet_file = open(sys.argv[1])
    get_term_frequency(tweet_file)
    print_frequency()


if __name__ == '__main__':
    main()
