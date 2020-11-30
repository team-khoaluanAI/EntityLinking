import sys
import requests, json, ast

token = xxxxxxx

def getJson(text):
    link = "https://viettelgroup.ai/nlp/api/v1/ner?header=Content-Type:application/json&header=token:"+token+"&text="+text
    myjson = {"sentence": text}
    r = requests.post(link, json=myjson)
    return json.loads(r.content)

def processJson(loaded_json):
    starts = []
    ends = []
    types = []
    words = []
    for data in loaded_json.items():
        if (data[0] == "result"):
            lists = data[1]
            for lst in lists:
                for k, v in lst.items():
                    if (k == "end_index"):
                        end = v
                        ends.append(end)
                    if (k == "start_index"):
                        start = v
                        starts.append(start)
                    if (k == "type"):
                        t = v
                        types.append(t)
                    if (k == "word"):
                        word = v
                        words.append(word)
    return starts, ends, types, words



if __name__ == '__main__':

    string = ''
    for word in sys.argv[1:]:
        string += word + ' '
    text = string

    # text = "Hồ Chí Minh tên khai sinh là Nguyễn Sinh Cung, là nhà cách mạng, người sáng lập Đảng Cộng sản Việt Nam, một trong những người đặt nền móng và lãnh đạo công cuộc đấu tranh giành độc lập, toàn vẹn lãnh thổ cho Việt Nam trong thế kỷ XX, một chiến sĩ cộng sản quốc tế. Việt Nam là 1 đất nước xinh đẹp."
    query_text = getJson(text)
    query_text = ast.literal_eval(json.dumps(query_text)) # Remove u before key
   
    starts, ends, types, words = processJson(query_text)
    # print(types)
    # print(words)

    length = len(words)
    s =" "
    # for i in range(length):
    #     newtext = words[i]+": "+types[i]+"</br>"
    #     s+=newtext

    temp = types
    # print(length)
    count = 0
    nho = ""
    for i in range(length):
        if(nho == temp[i]):
            continue

        newtext = "<b>"+temp[i]+"</b></br><button class='btn btn-warning btn-sm'> "+words[i]+"</button>"
        a = i+1
        nho = ""
        for j in range(a, length):
            # print(j)
            # print(temp[j])
            if(temp[j] == temp[i]):
                newtext += " <button class='btn btn-warning btn-sm'> "+words[j]+"</button>"
                # print(words[j])
                # print("b",count)
                nho = temp[i]
        s += newtext + "</br></br>"
        # print("a trùng",i)        
    # print(s)


    output = s.encode("utf-8")
    print(output.decode('cp1252','surrogateescape'))


