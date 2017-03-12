from flask import Blueprint
import sys

reload(sys)
sys.setdefaultencoding("utf8")

main = Blueprint('main', __name__, static_folder='static', template_folder='templates')

from . import sys_info
