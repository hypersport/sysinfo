from flask import Blueprint

main = Blueprint('main', __name__, static_folder='static',
                 template_folder='templates')

from . import sys_info
