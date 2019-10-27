from flask import Blueprint,render_template,flash,redirect,url_for,send_file,make_response,request
from io import BytesIO

from wdos.forms.user import CaseForm,CreateDocumentsForm
from wdos.extensions import mongo,bootstrap

from docxtpl import DocxTemplate

user_bp = Blueprint('user',__name__)

@user_bp.route('/new_case',methods = ['GET','POST'])
def new_case():
    form = CaseForm()
    if form.validate_on_submit():
        fayuan = form.fayuan.data
        casenum = form.casenum.data
        yuangao = form.yuangao.data
        beigao = form.beigao.data
        lian_time = form.lian_time.data
        anyou  = form.anyou.data
        biaodi = form.biaodi.data
        yuansheng_anhao = form.yuansheng_anhao.data
        anjian_leibie = form.anjian_leibie.data
        end_time = form.end_time.data

        mydict = {
                '法院':fayuan,
                '案号':casenum,
                '原告':yuangao,
                '被告':beigao,
                '立案时间':lian_time,
                '案由':anyou,
                '标的':biaodi,
                '原审案号':yuansheng_anhao,
                '案件类别':anjian_leibie,
                '结案时间':end_time
                }


        x = mongo.db.run.insert_one(mydict)

        flash('案件信息提交成功')
        return redirect(url_for('user.case'))

    return render_template('/user/index.html',form = form )

@user_bp.route('/',methods = ['GET','POST'])
def case():
    find  = mongo.db.run.find({})
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
@user_bp.route('/<case_id>/case_details' ,methods=['GET','POST'])
def case_details(case_id):
    find = mongo.db.run.find({'案号':case_id} )
    find_docxs = mongo.db.new_document.find({'case_number':case_id})
    if find_docxs:
        all_docxs = [docx['filename'] for docx in find_docxs]
        return render_template('/user/case_details.html',find = find ,case_id = case_id,all_docxs = all_docxs)
    else:
        filename = None
        return render_template('/user/case_details.html',find = find ,case_id = case_id)



#生成文书并存入new_document
@user_bp.route('/<case_id>/creat_documents',methods = ['POST','GET'])
def creat_documents(case_id):
    form = CreateDocumentsForm()
    if form.validate_on_submit():

        find = mongo.db.run.find_one({'案号':case_id},{'_id':0} )
        mes = {}
        mes['执行通知书w.docx'] = form.zxtzs.data
        mes['申请人廉政监督卡（二）w.docx']= form.lzjdk.data
        mes['申请执行人权利义务告知书w.docx'] = form.qlywgzs.data

        for k,v in mes.items():
            if v:

                data = mongo.db.templates.find_one({'filename':k})
                if data:
                    tem_stream = BytesIO(data['context'])

                    doc = DocxTemplate(tem_stream)
                    doc.render(find)

                    target_stream = BytesIO()

                    doc.save(target_stream)
                    filename = case_id + k
                    mongo.db.new_document.insert({'case_number':case_id ,'filename':filename,'context':target_stream.getvalue()})

                    tem_stream.close()
                    target_stream.close()


        flash('文书已全部生成','success')
        return  redirect(url_for('user.case_details',case_id = case_id ))

    return render_template('/user/creat_documents.html',case_id = case_id,form = form )

@user_bp.route('/<case_id>/edit',methods = ['POST','GET'])
def case_edit(case_id):
    form = CaseForm()
    find = mongo.db.run.find({'案号':case_id} )


    if form.validate_on_submit():

        fayuan = form.fayuan.data
        casenum = form.casenum.data
        yuangao = form.yuangao.data
        beigao = form.beigao.data
        lian_time = form.lian_time.data
        anyou  = form.anyou.data
        biaodi = form.biaodi.data
        yuansheng_anhao = form.yuansheng_anhao.data
        anjian_leibie = form.anjian_leibie.data
        end_time = form.end_time.data

        mydict = {
                '法院':fayuan,
                '案号':casenum,
                '原告':yuangao,
                '被告':beigao,
                '立案时间':lian_time,
                '案由':anyou,
                '标的':biaodi,
                '原审案号':yuansheng_anhao,
                '案件类别':anjian_leibie,
                '结案时间':end_time
                }
        old_dict = {'案号':case_id}
        mongo.db.run.update_one(old_dict,{ "$set":mydict})
        flash('案件信息编辑成功')
        return redirect(url_for('user.case_details',case_id = case_id))

    form.fayuan.data = find[0]['法院'] 
    form.casenum.data = find[0]['案号']
    form.anyou.data = find[0]['案由']
    form.yuangao.data = find[0]['原告']
    form.beigao.data = find[0]['被告']
    form.lian_time.data = find[0]['立案时间']
    form.anyou.data = find[0]['案由']
    form.biaodi.data = find[0]['标的']
    form.yuansheng_anhao.data = find[0]['原审案号']
    form.anjian_leibie.data = find[0]['案件类别']
    form.end_time.data = find[0]['结案时间']

    return render_template('user/case_edit.html',form  = form,case_id = case_id)


@user_bp.route('/search')
def search():
    q = request.args.get('q','').replace(' ','')
    if ishan(q) :
        regex = '.*' + q  + '.*'
        find = mongo.db.run.find( { '$or' : [{ '原告' : {'$regex':regex} },{ '被告': {'$regex':regex}  } ,{ '案号' : { '$regex' : regex } }  ] } )
    else:
        #regex = '.*[\(|\（]201[0-9][\)|\）]陕0823执11.*'
        regex = '.*'
        for c in q:
            if c == "(" or c =="（":
                c = '[\(|\（]'
            if c == ")" or c =="）":
                c = '[\)|\）]'

            regex +=  c

        find = mongo.db.run.find( { '案号' : { '$regex' : regex + '.*' } } )
    return render_template('user/search.html',find = list(find))


def ishan(text):
    # for python 3.x
    # sample: ishan('一') == True, ishan('我&&你') == False
    return all('\u4e00' <= char <= '\u9fff' for char in text)
