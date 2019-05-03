import pymongo

connection = pymongo.MongoClient('localhost', 27017)
db = connection.testDB
collection = db.get_collection('Tokens')

refine_tokens = {}
tokens = collection.find()
for token in tokens:
    data = token['token']
    for key, values in data.items():
        for value in values:
            refine_tokens[str(value)] = str(key)

def refine_sentence(raw):
    for token_key, token_value in refine_tokens.items():
        raw = raw.replace(token_key, token_value)
    
    return raw

#test1 = '속성가입자'
#test2 = '가입자우대이자금액조건'
#test3 = '서류서비스변상금액한도조건상환'

#print(refine_sentence(test1))
#print(refine_sentence(test2))
#print(refine_sentence(test3))