# coding=utf-8
from flask import Flask
from views import main
from views.custom_filters import format_time, format_size

app = Flask(__name__)
app.add_template_filter(format_time)
app.add_template_filter(format_size)
app.register_blueprint(main)
if __name__ == '__main__':
    app.run(port=9468)
