from flask import Blueprint,render_template
from wdos.forms.admin import LoginForm


admin_bp = Blueprint('admin',__name__)

@admin_bp.route('/main')
def admin_main():
    form = LoginForm()
    return render_template('admin/index.html',form = form  )
