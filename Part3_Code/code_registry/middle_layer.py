import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
def get_model(name):
    if name=="nltk":
        return nltk_model()

def init():
    pass
    
class nltk_model:
#代码来源：https://cloud.tencent.com/developer/article/1346772
    def process(self,sent):
        tokens = nltk.word_tokenize(sent)  #分词
        tagged = nltk.pos_tag(tokens)  #词性标注
        entities = nltk.ne_chunk(tagged, binary=True)#chunk.ne_chunk(tagged)  #命名实体识别
        return entities
    def prepro(self,sent):
        return sent
        
        
    def pre(self,sent):
        sent=self.prepro(sent)
        r=[]
        t=self.process(sent)
        for i in t:
            if "NN" in i[-1]:
                r.append(i[0])
        return r
        
    
if __name__=="__main__":   
    #nltk.download('punkt')
    #nltk.download('averaged_perceptron_tagger')
    #nltk.download('maxent_ne_chunker')
    #nltk.download('words')
    ex= 'European authorities fined Google a record $5.1 billion on Wednesday for abusing its power in the mobile phone market and ordered the company to alter its practices'
    sent= pre(ex)
    print(sent)

