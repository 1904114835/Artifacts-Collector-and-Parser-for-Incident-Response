import pickle
loaded_model = pickle.load(open('phishing.pkl', 'rb'))
def pre_url(url):
    return loaded_model.predict([url]).item()

print(pre_url("www.google.com"))