
import wikipedia
from pattern.en import pluralize,singularize
import nltk
import unicodedata
import math
from heapq import nlargest


def getdata():
    inp =raw_input('Enter the topic:')
    while 1:
        try:
            topic= wikipedia.page(inp)
            content1=topic.content #fetches content from the wikipedia webpage in the form of text
            break
        except wikipedia.exceptions.DisambiguationError as e:
            c=1
            for i in e.options:
                print str(c) + '.' + i
                c+=1
            choice=input('Enter your choice:')
            inp=e.options[choice-1]
            topic= wikipedia.page(inp)
            content1=topic.content
            break

##    1=re.sub("[\(\[].*?[\)\]]", "", summ)
    content1=content1.encode('ascii','ignore')
    content1=content1.lower()
    tokens=nltk.word_tokenize(content1)
    tagged=nltk.pos_tag(tokens)
    freqdic={}
    for i in tagged:
        word=singularize(i[0])
        if i[1] in ['NN','NNS','NNP','NNPS','FW'] and not (word in inp.lower().split()) and word.isalpha() : #iterates through the text and filters out for nouns and the various forms of nouns
            if word in freqdic:                                                                             #makes sure the dictionary doesn't contain the word itself, also no pronouns and numbers
                freqdic[word]+=1
            else:
                freqdic[word]=1
    return freqdic


def runTime() :
    dic1=getdata()
    dic2=getdata()
    #print dic1
    #print dic2
    intersect = []
    for item in dic1.keys(  ):
        if dic2.has_key(item):
            intersect.append(item)

    correspond=[]
    for i in intersect:
        slope = 1.0 * (dic1[i] / dic2[i])
        if slope>1.0:
            slope = (1.0 / slope )
        z_score= math.sqrt( math.pow(dic1[i],2) + math.pow(dic2[i],2) ) # applying distance formula, considering the frequencies in y-x plane.
        z_corrected = slope * z_score #correcting the values using the slope/inverse slope values to reduce the z_score depending on how much more frequent it is in one text compared to the other
        correspond.append(z_corrected)
    my_dict = dict(zip(intersect, correspond)) #creates dictionary from words and corresponding z-scores
    return nlargest(3, my_dict, key=my_dict.get) #returns the 3 common words with highest calculated  in form of a tuple/array



def main():

    while 1:
        choice1 = raw_input("Y to start the program, N to end the program: ")

        if (choice1 in "yY") :
            common_themes = runTime()
            print 'I think the common themes are either of the following :' , common_themes[0], ',' , common_themes[1] , ',' , common_themes[2]
        elif (choice1 in "nN"):
            break
        else:
            print "Enter again"
            continue


main()
