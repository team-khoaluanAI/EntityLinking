import EntityRecognition as ER
import EntityLinking as EL
import sys
import time
import math

def timeSince(since):
    now = time.time()
    s = now - since
    m = math.floor(s / 60)
    s -= m * 60
    return '%dm %ds' % (m, s)

if __name__ == '__main__':
    label_link = 'Yago(vi)/labels.nt'
    sameas_link = 'Yago(vi)/wiki_link.nt'
    type_link = 'Yago(vi)/types.nt'
    fact_link = 'Yago(vi)/facts.nt'

    string = ''
    for word in sys.argv[1:]:
        string += word + ' '
    text = string
    # text="Messi cùng đồng đội bị Bayern vùi dập ở trận tứ kết Champions League diễn ra rạng sáng 15/8 (giờ Hà Nội)."


    query_text = ER.getJson(text)
    query_text = ER.ast.literal_eval(ER.json.dumps(query_text)) # Remove u before key
   
    bd, kt, types = ER.processJson(query_text)
    entities = ER.getEntities(text, bd, kt)
    if not bd:
        text = ("Không có thực thể để xử lý !!")
        output = text.encode("utf-8")
    else:
        #những loại dưới đây sẽ ko xét đến khi định hướng thực thể
        check = ['TIME_DateDuration', 'TIME_Date', 'TIME_Year', 'TIME_Time', 'NUM_Age', 'NUM_Percent', 'NUM_Money', 'NUM_Phone']

        new_text = text
        length = len(entities)
        for i in  range(length):
            #start = time.time()
            if types[i] in check:
                continue
            else:
                wiki_link = EL.findWikipedia(entities[i], types[i], label_link, type_link, fact_link, sameas_link)
                link = EL.convertTexttoLink(wiki_link, entities[i])
                idx = new_text.find(entities[i])
                new_text = EL.replaceEntitytoLink(new_text, entities[i], link, idx)
        output = new_text.encode("utf-8")

    print(output.decode('cp1252','surrogateescape'))


