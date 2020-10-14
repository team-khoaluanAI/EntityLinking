def findWikipedia(api_entity, api_type, path_label, path_type, path_fact, path_sameas):
    yago_entities = []
    yago_entity = ""
    wiki_link = "#"

    api_entity = '"' + api_entity + '"' + "@vi"  # "Hà Nội"@vi

    temp = getYagoEntity(api_entity, path_label)
    #print("DS temp:",temp)

    if not temp: #ko có thực thể yago nào được tìm thấy
        return wiki_link
    elif len(temp) < 2: #1 thực thể yago thì khỏi xét loại
        yago_entity = temp[0]
    else:
        for ye in temp:
            # print(ye)
            types = getYagoType(ye, path_type)
            # print(types)
            for j in range(len(types)):
                if api_type in convertYagoType(types[j]):
                    #print("Entity này đã có loại YAGO khớp api type !!")
                    yago_entities.append(ye)
                    break; #chỉ cần 1 loại thỏa là OK

        # print("DS entities: ",yago_entities)
        length = len(yago_entities)
        # print(length)
        if not yago_entities:
            return wiki_link
        elif length >= 2:
            counts = []
            for en in yago_entities:
                counts.append(countEntityinFact(en, path_fact))
            # print(counts)
            max = counts[0]
            imax = 0
            for i in range(length):
                if counts[i] > max:
                    max = counts[i]
                    imax = i
            yago_entity = yago_entities[imax]
        else:
            yago_entity = yago_entities[0]

    wiki_link = getWikipediaLink(yago_entity, path_sameas)

    return wiki_link

# read file 'labels' and get entities yago
def getYagoEntity(api_en, path):
    label_file = open(path, encoding='utf8')
    labels = []
    for line in label_file:
        if (api_en in line):
            yago_line = line
            labels.append(yago_line.split('\t')[0]) # many yago entites for 1 api entity
    label_file.close()
    return labels

# read file 'types' and get types belong to entity yago
def getYagoType(yago_en, path):
    type_file = open(path, encoding='utf8')
    types = []
    for line in type_file:
        if (yago_en in line):
            type = line.split('\t')[2]
            type = type.replace("<http://schema.org/", "")
            types.append(type.replace(">", ""))
    type_file.close()
    return types

# read file wiki in yago and get link wikipedia
def getWikipediaLink(yago_en, path):
    link_file = open(path, encoding='utf8')
    link = ''
    for line in link_file:
        if (yago_en in line): # only a entity yago was get wikilink
            wiki_line = line
            link = wiki_line.split('\t')[2]
            link = link[0:link.find('^')].replace('"', "")
            break
    link_file.close()
    return link

# read file "facts" and count
def countEntityinFact(entity, path):
    fact_file = open(path, encoding='utf8')
    count = 0
    for line in fact_file:
        if (entity in line):
            count += 1
    fact_file.close()
    return count

# convert YAGO type to API type
def convertYagoType(yago_type):
    api_type = []
    # n yago types - 1 api type
    if yago_type in ('Book', 'Movie', 'MusicComposition', 'TVSeason', 'MovieSeries',
                     'BookSeries', 'TVSeries', 'TVEpisode'):
        api_type.append('PRO_Art')
    elif yago_type in ('Game', 'VideoGame', 'MobileApplication'):
        api_type.append('PRO_Other')

    # 1 yago type - 1 api type
    elif yago_type == 'Article':
        api_type.append('PRO_Printing')
    elif yago_type == 'Corporation':
        api_type.append('ORG_Corporation')
    elif yago_type == 'InfectiousDisease':
        api_type = 'DIS'
    elif yago_type == 'GovernmentOrganization':
        api_type.append('ORG_Political')
    elif yago_type == 'Person':
        api_type.append('PER')
    elif yago_type == 'Vehicle':
        api_type.append('PRO_Vehicle')

    # 1 yago type - n api types
    elif yago_type == 'Product':
        api_type.append('PRO_Food ')
        api_type.append('PRO_Drug')
        api_type.append('PRO_Other ')
    elif yago_type == 'Place':
        api_type.append('LOC_Geological')
        api_type.append('LOC_Region')
        api_type.append('LOC_GPE')
        api_type.append('LOC_Other')
    else:
        api_type.append('not exists')

    return api_type


def convertTexttoLink(link, entity):
    return "<a href='"+link+"'target='_blank'><b>"+entity+"</b></a>"
    
def find_all_indexes(input_str, search_str):
    l1 = []
    length = len(input_str)
    index = 0 #index là biến chạy
    while index < length:
        i = input_str.find(search_str, index) #tìm từ trái qua từ vị trí index
        if i == -1:
            return l1 #không tìm thấy
        l1.append(i)
        index = i + 1 #tìm từ vị trí sau vị trí tìm dc trc đó
    return l1

def checkText(text, e, vitri):
    flag = 1; #hợp lệ 
    # print("chac",text[vitri+len(e)])
    if(text[vitri+len(e)] == '<'):
        flag = 0
    elif(text[vitri-1] == '/' or text[vitri-1] == '_' or text[vitri-1] == '>'):
        flag = 0
    return flag

#<a href='https://en.wikipedia.org/wiki/Diego_Maradona'>Maradona</a>
# <a href='https://vi.wikipedia.org/wiki/Origami'target='_blank'><b>Origami</b></a>

def replaceEntitytoLink(text, en, link, index):
    kq = text
    if(checkText(kq, en, index) != 0): # không thay từ trong link wikipedia
        kq = kq[:index]+link+kq[index+len(en):]
        # print(kq)
    else:
        idx = text.find(en, index+1)
        return replaceEntitytoLink(kq, en, link, idx)
    return kq