from stanfordcorenlp import StanfordCoreNLP
import numpy as np
#默认英文

def get_stanford_eng():
    stanford_model = StanfordCoreNLP(r'c:\Users\wrl\Desktop\HKU_project\code\code_registry')

    text = """0ee6dec20220704103645-3	E4-70-B8-D4-1F-AC	MicrosoftEdgeAutoLaunch_3CBFCB42A4709007915C7060F5375710  	"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --no-startup-window --win-session-start /prefetch:5"""
     
    res = stanford_model.ner(text)

    print(res)

    return stanford_model

def get_model(name):
    import middle_layer
    middle_layer.init()
    return middle_layer.get_model(name)

if __name__=="__main__":
    import os
    data=[]
    dirl=os.listdir("data/")
    print(dirl)
    for dirl in dirl:
        p="data/"+dirl
        with open(p, "r") as f:  # 打开文件
            d = f.read()  # 读取文件
            data.append(d)
    
    model=get_model("nltk")
    result=[]
    for d in data:
        result.extend(model.pre(d))
    
    print(data)
    