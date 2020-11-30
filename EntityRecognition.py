import requests, json, ast

token = xxxxxx

def getJson(text):
    link = "https://viettelgroup.ai/nlp/api/v1/ner?header=Content-Type:application/json&header=token:"+token+"&text="+text
    myjson = {"sentence": text}
    r = requests.post(link, json=myjson)
    return json.loads(r.content)

def processJson(loaded_json):
    starts = []
    ends = []
    types = []
    for data in loaded_json.items():
        if (data[0] == "result"):
            lists = data[1]
            for lst in lists:
                for k, v in lst.items():
                    if (k == "end_index"):
                        ends.append(v)
                    if (k == "start_index"):
                        starts.append(v)
                    if (k == "type"):
                        types.append(v)
    return starts, ends, types

def getEntities(text, bd, kt):
    length = len(bd)
    entities = []
    for i in range(length):
        e = text[bd[i]:kt[i]]
        entities.append(e)
    return entities
