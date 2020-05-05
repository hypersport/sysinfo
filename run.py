from flask import Flask
from views import main
from views.custom_filters import format_time, format_size, socket_type, socket_family, format_addr_port

app = Flask(__name__)
app.add_template_filter(format_time)
app.add_template_filter(format_size)
app.add_template_filter(socket_type)
app.add_template_filter(socket_family)
app.add_template_filter(format_addr_port)
app.register_blueprint(main)

if __name__ == '__main__':
    app.run(port=9468)
