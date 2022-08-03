import middle_layer
import numpy as np
s=""
if __name__=="__main__":
    model=middle_layer.get_model("nltk")
    lib=np.load("lib.npy")
    res=model.pre(s)
    alert=[]
    for r in res:
        if r not in lib:
            alert.append(r)
    print(alert)