import nltk
from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import json
import httplib
import copy
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
import re
class article:

    def  __init__(self,para):
        #self.para = json.load(para)
        self.para = para
        self.changeWords={}
        self.wordschanged={}
        self.sentiment = 0.5
        self.adj={}
        self.tagWords(self.para)
    def tagWords(self, para):
        wnl = WordNetLemmatizer()
        #lines_list = tokenize.sent_tokenize(para)
        lines_list = para.split('.')
        for line in lines_list:
            text = tokenize.word_tokenize(line)
            taggedWords = nltk.pos_tag(text)
            adjWords=[]
            #print line,taggedWords
            for i in xrange(len(taggedWords)):
                if i > 0 and taggedWords[i][1] == 'JJ':
                    if taggedWords[i-1][1] == "RB" :
                        self.wordschanged[line]= {taggedWords[i-1][0]: "_"}
                    elif len(adjWords)>0:
                        adjWords =[ word[0] for word in taggedWords if word[1]== 'JJ']
                if taggedWords[i][1] == 'JJS':
                    newWord = wnl.lemmatize(taggedWords[i][0], 'a').encode("ascii")
                    if newWord:
                        self.wordschanged[line] = {taggedWords[i][0]: newWord}
                    else:
                        self.wordschanged[line] = {taggedWords[i][0]: "_"}
                if taggedWords[i][1] == 'RBS':
                    newWord = wnl.lemmatize(taggedWords[i][0], 'r').encode("ascii")
                    if newWord:
                        self.wordschanged[line] = {taggedWords[i][0]: newWord}
                    else:
                        self.wordschanged[line] = {taggedWords[i][0]: "_"}


            if len(adjWords)>0:
                self.changeWords[line]=adjWords
            print 'line :' + line


    def sentimentAnalysis(self, text):
        conn = httplib.HTTPConnection("text-processing.com")
        payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"text\"\r\n\r\n" + text + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"

        headers = {
            'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
            'cache-control': "no-cache",
            'postman-token': "36b9dc89-4fc9-753e-dae7-9529757924da"
        }

        conn.request("POST", "/api/sentiment/", payload, headers)

        res = conn.getresponse()
        data = res.read()

        #print(data.decode("utf-8"))
        ss = json.loads(data)
        neg = ss["probability"]['neg']
        neutral = ss["probability"]['neutral']
        pos = ss["probability"]['neg']
        if ss["label"] == "neg" or pos > 0.75: #max(pos, neg) < 2 * min(pos, neg):
            return False
        return True

    def checkSentenceGrammar(self,setence):
        return False

    def getSynonym(self, word):
        conn = httplib.HTTPConnection("words.bighugelabs.com")
        headers = {
            'cache-control': "no-cache",
            'postman-token': "1690a85d-c7ee-56b2-abc1-f7141a9a03ed"
        }
        conn.request("POST", "/api/2/940e7865c406ab5b09b3fcef90fadde0/" + word + "/json", headers=headers)
        res = conn.getresponse()
        data = res.read()
        print data
        allSyns = json.loads(data)
        syns =  allSyns["adjective"]["syn"]
        for syn in syns:
            if word is not syn and self.sentimentAnalysis(syn):
                print 'syn chosen:', syn
                return syn
        return ''


    def main(self,para, sentiment):
        lines_list = self.changeWords.keys()
        for sentence in lines_list:
            print sentence
            if not self.sentimentAnalysis(sentence):
                changeWords = self.changeWords[sentence]
                if len(changeWords) == 0 :
                    print 'here'
                    continue
                tempSentence = copy.deepcopy(sentence)
                for currentWord in changeWords:
                    print currentWord
                    synonym = self.getSynonym(currentWord)
                    if self.sentimentAnalysis(tempSentence.replace(currentWord,synonym)):
                        print currentWord,synonym
                        if sentence in self.wordschanged:
                            self.wordschanged.get(sentence)[currentWord]=synonym
                        else:
                            self.wordschanged[sentence]={currentWord:synonym}
                    else :
                        tempSentence.replace(synonym,currentWord)
            print self.wordschanged

        return self.wordschanged

# paragraph = "It was one of the worst movies I've seen, despite good reviews. Unbelievably bad acting!! Poor direction. VERY poor production.The movie was bad. Very bad movie. VERY bad movie. VERY BAD movie. VERY BAD movie!"
# paragraph2="I never really thought about it like that, but Q is so right. I instantly flashed back to sixth grade, seventh grade, eighth grade and straight through high school, and to the universal language all kids speak: A substitute in the classroom means a day off, no work, a break until the teacher decides to come back and question why nothing got accomplished"
# para3 = "Mary is tallest "
# arti = article(paragraph2)
# data = arti.main(paragraph2,0.5)
# print data
# json_data = json.dumps(data)
