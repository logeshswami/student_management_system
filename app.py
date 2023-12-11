from flask import Flask
from pymongo import MongoClient
from dotenv import load_dotenv
from flask_marshmallow import Marshmallow
from views.student_views import student_bp
from views.subject_views import subject_bp
from views.teacher_views import teacher_bp
from views.student_record_views import student_record_bp


app = Flask(__name__)
ma = Marshmallow()
ma.init_app(app)
app.register_blueprint(student_bp)
app.register_blueprint(subject_bp)
app.register_blueprint(teacher_bp)
app.register_blueprint(student_record_bp)

if __name__ == '__main__':
    app.run(debug=True)