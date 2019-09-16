from flask import Blueprint,render_template

admin_bp = Blueprint('admin',__name__)

@admin_bp.route('/main')
def admin_main():
    #return "admin_main "
    return render_template('admin/index.html')
