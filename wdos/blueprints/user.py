from flask import Blueprint,render_template,flash,redirect,url_for,send_file,make_response,request
from wtforms import BooleanField,SubmitField
from flask_wtf import FlaskForm

from wdos.extensions import mongo,bootstrap
from wdos.forms.user import CaseForm,ClientForm,DocumentsForm,CreateDocumentsForm
from wdos.utils import is_banjiao,str_client,ishan,c_d_list
from io import BytesIO
from docxtpl import DocxTemplate

user_bp = Blueprint('user',__name__)

#案件相关名称清单
@user_bp.context_processor
def name_list():
    name_dict = {
            'name_list':{
                'case_number':'案号',
                'case_cause':'案由',
                'case_subject_matter':'标的',
                'case_start_time':'立案时间' ,
                'original_case_number':'原审案号' ,
                'judgement_content':'判决内容/执行目的' ,
                'judgement_time':'判决时间' ,
                'case_end_cause':'结案原因/执行过程' ,
                'case_end_time':'结案时间' ,
                
                'client_sex':'性别',
                'client_c_d':'申请人/被执行人',
                'client_name':'名字',
                'client_address':'住址',
                'client_id':'公民身份证号码',
                'client_phone_number':'当事人手机号码'
                }

            }

    return name_dict  


@user_bp.route('/new_case',methods = ['GET','POST'])
def new_case():
    form = CaseForm()
    if form.validate_on_submit():
        case_number =form.case_number.data
        case_cause = form.case_cause.data
        case_subject_matter= form.case_subject_matter.data
        case_start_time = form.case_start_time.data
        original_case_number = form.original_case_number.data
        judgement_content = form.judgement_content.data
        judgement_time = form.judgement_time.data
        case_end_cause = form.case_end_cause.data
        case_end_time = form.case_end_time.data
        case_id = str(hash(case_number + case_start_time))
        case_number = is_banjiao(case_number)

        mydict = {
                'case_id':case_id,
                'case_number':case_number,
                'case_cause':case_cause,
                'case_subject_matter':case_subject_matter,
                'case_start_time':case_start_time ,
                'original_case_number':original_case_number ,
                'judgement_content':judgement_content ,
                'judgement_time':judgement_time ,
                'case_end_cause':case_end_cause ,
                'case_end_time':case_end_time ,
                'clients':[]
                }

        in_db = mongo.db.case.find({'$or':[{'case_number':case_number},{'case_id':case_id}]}).count()

        if in_db == 0:
            x = mongo.db.case.insert_one(mydict)
            flash('案件信息提交成功'+ str(in_db))
            find = mongo.db.case.find_one({'case_id':case_id},{'_id':0,'case_id':0})
            return render_template('/user/case_details.html',find = find ,case_id = case_id)
        else:
            flash(in_db,'warning')
            return render_template('/user/index.html',form = form )

    return render_template('/user/index.html',form = form )

@user_bp.route('/')
def case():
    find  = mongo.db.case.find({},{'_id':0})

    return render_template('user/case.html',find = find)
          

#下载文件
@user_bp.route('/downloads/<document_name>',methods = ['GET'])
def downloads(document_name):
    docxs = mongo.db.new_document.find_one({'filename':document_name})

    if docxs:
        docx = BytesIO(docxs['context'])
        filename = docxs['filename']

        return send_file(docx,as_attachment = True ,attachment_filename = filename)
    else:
        return "no case" + document_name


#详情
@user_bp.route('/case_details/<case_id>' ,methods=['GET','POST'])
def case_details(case_id):
    find = mongo.db.case.find_one({'case_id':case_id} ,{'_id':0,'case_id':0,'complaints':0,'defendants':0})
    find_docxs = mongo.db.new_document.find({'case_id':case_id})
    if find_docxs:
        all_docxs = [docx['filename'] for docx in find_docxs]
        return render_template('/user/case_details.html',find = find ,case_id = case_id,all_docxs = all_docxs)
    else:
        filename = None




#生成文书并存入new_document
@user_bp.route('/creat_documents/<case_id>',methods = ['POST','GET'])
def creat_documents(case_id):
    class DocumentsForm(FlaskForm):
        pass
    tems = mongo.db.templates.find()
    for tem in tems:
        setattr(DocumentsForm,tem['filename'],BooleanField(tem['filename']))
    setattr(DocumentsForm,'开始生成',SubmitField('开始生成'))

    form = DocumentsForm()
    if form.validate_on_submit():

        find = mongo.db.case.find_one({'case_id':case_id},{'_id':0} )
        clients_detail = find
        clients_detail['complaints'] = str_client(find['complaints'])
        clients_detail['defendants'] = str_client(find['defendants'])
        clients_detail['complaints_detail'] =[] 
        clients_detail['defendants_detail'] = [] 
        for client in find['clients']:
            c =( client['client_sex'] + ',' 
            + client['client_ymd'] + ','
            + client['client_address'] +','
            + '公民身份证号码:' + client['client_id'] + '.')
            if client['client_c_d'] == '申请人':
                strc = '申请人:' + client['client_name'] + ',' + c
                clients_detail['complaints_detail'].append(strc)
            else:
                strc = '被执行人:' + client['client_name'] + ',' + c
                clients_detail['defendants_detail'].append(strc)

        mes  = request.form 

        for k,v in mes.items():
            if v:
                data = mongo.db.templates.find_one({'filename':k})
                if data:
                    tem_stream = BytesIO(data['context'])

                    doc = DocxTemplate(tem_stream)
                    doc.render(clients_detail)

                    target_stream = BytesIO()

                    doc.save(target_stream)
                    filename = find['case_number'] + k
                    n = mongo.db.new_document.find({'filename':filename}).count()
                    if n == 0:
                        mongo.db.new_document.insert({'case_id':case_id ,'filename':filename,'context':target_stream.getvalue()})
                    else:
                        mongo.db.new_document.update({'filename':filename},{'$set':{'case_id':case_id ,'filename':filename,'context':target_stream.getvalue()}})

                    tem_stream.close()
                    target_stream.close()

        flash('文书已全部生成','success')
        return  redirect(url_for('user.case_details',case_id = case_id ))

    return render_template('/user/creat_documents.html',case_id = case_id,form = form )

@user_bp.route('/edit/<case_id>',methods = ['POST','GET'])
def case_edit(case_id):
    form = CaseForm()
    find = mongo.db.case.find_one({'case_id':case_id} )

    if form.validate_on_submit():
        case_number = form.case_number.data 
        case_cause = form.case_cause.data
        case_subject_matter = form.case_subject_matter.data 
        case_start_time = form.case_start_time.data 
        original_case_number = form.original_case_number.data 
        judgement_content = form.judgement_content.data 
        judgement_time = form.judgement_time.data 
        case_end_cause = form.case_end_cause.data
        case_end_time = form.case_end_time.data 

        mydict = {
                'case_id':case_id,
                'case_number':case_number,
                'case_cause':case_cause,
                'case_subject_matter':case_subject_matter,
                'case_start_time':case_start_time ,
                'original_case_number':original_case_number ,
                'judgement_content':judgement_content ,
                'judgement_time':judgement_time ,
                'case_end_cause':case_end_cause ,
                'case_end_time':case_end_time ,
                }
        old_dict = {'case_id':case_id}
        mongo.db.case.update_one(old_dict,{ "$set":mydict})
        flash('案件信息编辑成功','success')
        return redirect(url_for('user.case_details',case_id = case_id))

    form.case_number.data =find['case_number']
    form.case_cause.data =find['case_cause']
    form.case_subject_matter.data =find['case_subject_matter']
    form.case_start_time.data =find['case_start_time']
    form.original_case_number.data =find['original_case_number']
    form.judgement_content.data =find['judgement_content']
    form.judgement_time.data =find['judgement_time']
    form.case_end_cause.data =find['case_end_cause']
    form.case_end_time.data =find['case_end_time']

    return render_template('user/case_edit.html',form  = form,case_id = case_id,find = find)

#查找案件
@user_bp.route('/search')
def search():
    q = request.args.get('q','').replace(' ','')
    if ishan(q) :
        regex = '.*' + q  + '.*'
        find = mongo.db.case.find( { '$or' : [{ '原告' : {'$regex':regex} },{ '被告': {'$regex':regex}  } ,{ '案号' : { '$regex' : regex } }  ] } )
    else:
        #regex = '.*[\(|\（]201[0-9][\)|\）]陕0823执11.*'
        regex = '.*'
        for c in q:
            if c == "(" or c =="（":
                c = '[\(|\（]'
            if c == ")" or c =="）":
                c = '[\)|\）]'

            regex +=  c

        find = mongo.db.case.find( { 'case_number' : { '$regex' : regex + '.*' } } )
    return render_template('user/search.html',find = list(find))


#添加当事人
@user_bp.route('/add_client/<case_id>',methods = ['GET','POST'])
def add_client(case_id):
    form = ClientForm()
    if form.validate_on_submit():
        client_c_d         =form.client_c_d.data          
        client_name        =form.client_name.data         
        client_sex         =form.client_sex.data          
        client_ymd         =form.client_ymd.data         
        client_address     =form.client_address.data      
        client_id          =form.client_id.data           
        client_phone_number=form.client_phone_number.data  

        client_dic ={

         'client_c_d'         : client_c_d           ,
         'client_name'        : client_name          ,
         'client_sex'         : client_sex           ,
         'client_ymd'         : client_ymd           ,
         'client_address'     : client_address       ,
         'client_id'          : client_id            ,
         'client_phone_number': client_phone_number  

                }
        x = mongo.db.case.update_one({'case_id':case_id},{'$push':{'clients':client_dic}})
        c_d_list(case_id)
        find= mongo.db.case.find_one({'case_id':case_id})
        flash(client_c_d + client_name + '添加完毕','success')


        return render_template('user/case_details.html',case_id= case_id,find = find)
    return render_template('user/add_client.html',form= form)


@user_bp.route('/delete_client/<case_id>/<client_name>')
def delete_client(case_id,client_name):
    mongo.db.case.update({'case_id':case_id},{'$pull':{'clients':{'client_name': client_name}}})
    
    c_d_list(case_id)
    flash('删除成功','success')
    return redirect(url_for('.case_details',case_id = case_id))


@user_bp.route('/edit_client/<case_id>/<client_name>',methods = ['GET','POST'])
def edit_client(case_id,client_name):
    form = ClientForm()
    if form.validate_on_submit():
        mongo.db.case.update({'case_id':case_id},{'$pull':{'clients':{'client_name': client_name}}})

        client_c_d         =form.client_c_d.data          
        client_name        =form.client_name.data         
        client_sex         =form.client_sex.data          
        client_ymd         =form.client_ymd.data         
        client_address     =form.client_address.data      
        client_id          =form.client_id.data           
        client_phone_number=form.client_phone_number.data  

        client_dic ={
         'client_c_d'         : client_c_d           ,
         'client_name'        : client_name          ,
         'client_sex'         : client_sex           ,
         'client_ymd'         : client_ymd           ,
         'client_address'     : client_address       ,
         'client_id'          : client_id            ,
         'client_phone_number': client_phone_number  }
                
        x = mongo.db.case.update_one({'case_id':case_id},{'$push':{'clients':client_dic}})
        c_d_list(case_id)
        find = mongo.db.case.find_one({'case_id':case_id} ,{'_id':0,'case_id':0})
        flash(client_name + '修改成功','success')
        return render_template('user/case_details.html',case_id= case_id,find = find)

    find = mongo.db.case.find_one({'case_id':case_id})
    find_clients = find['clients']
    for client in find_clients:
        if client['client_name'] == client_name:
            form.client_c_d.data           = client['client_c_d']
            form.client_name.data          = client['client_name']
            form.client_sex.data           = client['client_sex']
            form.client_ymd.data           = client['client_ymd']
            form.client_address.data       = client['client_address']
            form.client_id.data            = client['client_id']
            form.client_phone_number.data  = client['client_phone_number']
            return render_template('/user/edit_client.html',form = form )

    #return find['clients'][0]['client_name']
    return redirect(url_for('.case_details',case_id = case_id))
