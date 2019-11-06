from wdos.extensions import mongo
#转为半角括号
def is_banjiao(s):
    new_number = ''
    for is_ban in s.replace(' ',''):
            if is_ban == '（':
                is_ban = '('
            if is_ban == '）':
                is_ban = ')'
            new_number += is_ban
    return new_number

def str_client(list_c_d):
    str_c_d = ''
    for c_d in list_c_d:
        if c_d != list_c_d[-1]:
            str_c_d += c_d
            str_c_d += ','
        else:
            str_c_d += c_d

    return str_c_d


#判断是否为汉字
def ishan(text):
    # for python 3.x
    # sample: ishan('一') == True, ishan('我&&你') == False
    return all('\u4e00' <= char <= '\u9fff' for char in text)


#刷新申请人与被执行人清单
def c_d_list(c_id):
    find  = mongo.db.case.find_one({'case_id':c_id},{'_id':0})
   
    c_name = []
    d_name = []
    for f in find['clients']:
        if f['client_c_d'] == '申请人':
            c_name.append(f['client_name'])
        else:
            d_name.append(f['client_name'])

    mongo.db.case.update_one({'case_id':c_id},{'$set':{'defendants':d_name}})
    mongo.db.case.update_one({'case_id':c_id},{'$set':{'complaints':c_name}})

