from flask import Blueprint,render_template,flash,redirect,url_for

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

@user_bp.route('/<case_id>/case_details' ,methods=['GET','POST'])
def case_details(case_id):
    find = mongo.db.run.find({'案号':case_id} )
    return render_template('/user/case_details.html',find = find ,case_id = case_id)


@user_bp.route('/<case_id>/creat_documents',methods = ['POST','GET'])
def creat_documents(case_id):
    form = CreateDocumentsForm()
    if form.validate_on_submit():
        mes = {}
        mes['zxtzs'] = form.zxtzs.data
        mes['lzjdk']= form.lzjdk.data
        mes['qlywgzs'] = form.qlywgzs.data


        find = mongo.db.run.find({'案号':case_id},{'_id':0} )
        case_data  = find[0]
        doc = DocxTemplate('/home/debian/test_flask/wd/wdos/document_templates/zxhan.docx')
        doc.render(case_data)
        doc.save('./word.docx')


        flash(case_data)
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


