import sys
import nltk
from nltk.tokenize import word_tokenize
import math
from collections import defaultdict
import random


def getGrams(data):
    
    bigrams = defaultdict(dict)
    unigrams = {}
    
    for dpoint in data:
        
        tokens = nltk.tokenize.word_tokenize(dpoint) 
        tokens = [word.lower() for word in tokens if word.isalpha()]
        tokens.append("</s>")
        
        if len(tokens) >= 2:
            prev = "<s>"
            
            if prev in unigrams:
                unigrams[prev] = unigrams[prev]+1
            else:
                unigrams[prev] = 1

            for token in tokens:
                
                if token in bigrams[prev]:
                    bigrams[prev][token] = bigrams[prev][token] + 1
                else:
                    bigrams[prev][token] = 1
                    
                if token in unigrams:
                    unigrams[token] = unigrams[token] + 1
                else:
                    unigrams[token] = 1

                prev = token
    return bigrams, unigrams

def normalizeByUnigrams(bigrams,unigrams):
#     dividing bigram counts by the occurences of the first word in unigrams
#     (slide 19)
    for key in bigrams:
        for k,v in bigrams[key].items():
            bigrams[key][k] = v / unigrams[key]
        
def logProb(sentence,bigrams):
    tokens = nltk.tokenize.word_tokenize(sentence) 
    tokens = [word.lower() for word in tokens if word.isalpha()]
    tokens.append("</s>")
    
    prob = 0
    
    prev = "<s>"
    
    for token in tokens:
        
        if token in bigrams[prev]:
            prob += math.log(bigrams[prev][token])
        prev = token
    return prob

def generate(word, bigrams):
    sentence = []
    sentence.append(word)
    for i in range(7):
        nextword = top5(bigrams,sentence[i])
        if len(nextword) > 0:
            if len(nextword) > 1:
                rand = random.randint(0,len(nextword)-1)
            else:
                rand = 0
            while(nextword[rand] == '</s>'):
                rand = random.randint(0,len(nextword)-1)

            sentence.append(nextword[rand])
        else:
            break

    return ' '.join(sentence)
        
        
def top5(bigrams, word):
    return sorted(bigrams[word], key=bigrams[word].get, reverse=True)[:5]






if __name__ == '__main__':
    nltk.download('punkt')

    filename = sys.argv[1]
    file = open(filename)
    data = file.readlines()
    
    bigrams, unigrams = getGrams(data)
    normalizeByUnigrams(bigrams,unigrams)
    
    print(f'Log probability for "{sys.argv[2]}" : {logProb(sys.argv[2],bigrams)}')
    print(f'Generated Sentence for starting word "{sys.argv[3]} : {generate(sys.argv[3],bigrams)}"')
    