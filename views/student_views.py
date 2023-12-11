from flask import request, jsonify,Blueprint
from validator.student_validator import ma, StudentSchema, StudentsListSchema
from validator.validate_functions import remove_extra_spaces
#from app import students_collection
from models.student import students_collection
from validator.record_exist_check import check_record
from dotenv import load_dotenv
import os
import json

load_dotenv()

student_schema = StudentSchema()
student_list_schema = StudentsListSchema()
student_bp = Blueprint("student",__name__)

# INSERT STUDETNT DETAILS
@student_bp.route('/student', methods=['POST'])
def create_student():
    data = request.json
    records = data["student_records"]
    err = student_list_schema.validate(data)
    if (not err):
        for student in records:
            if not check_record("student", student["id"]):
                student = remove_extra_spaces(student)
                result = students_collection.insert_one(student)
            else:
                return f"record with id {student['id'] } already exist",200

        return jsonify({"message": " All Student Record created successfully"}),200

    else:
        return err,400

# GET STUDENT DETAILS


@student_bp.route('/student', methods=['GET'])
def get_students():
    students = list(students_collection.find())
    return json.dumps(students, default=str),200

# GET STUDENT DETAIL USING PAGINATION


@student_bp.route('/student/pagination', methods=['GET'])
def get_students_pagination():
    page_no = int(request.args.get("page_no"))
    page_length = int(os.environ.get("page_length"))
    students = list(students_collection.find().skip(
        page_no*page_length).limit(page_length))
    return json.dumps(students, default=str),200

# GET SPECIFIC STUDENT DETAILS USING THEIR ID


@student_bp.route('/student/<string:student_id>', methods=['GET'])
def get_student(student_id):
    student = students_collection.find_one({"id": student_id})
    if student:
        return json.dumps(student, default=str), 200
    else:
        return "record not found",404

# UPDATE STUDENT DETAILS


@student_bp.route('/student/<string:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.json
    err = student_schema.validate(data)
    if (not err):
        data = {"personal_information": data["personal_information"]}
        data = remove_extra_spaces(data)
        result = students_collection.update_one(
            {"id": student_id}, {"$set": data})
        if result.modified_count > 0:
            return jsonify({"message": "Student updated successfully"}),200
        else:
            return jsonify({"message": "Student not updated/record not found"}),404
    else:
        return err,400

# DELETE STUDETNT DETAILS


@student_bp.route('/student/<string:student_id>', methods=['DELETE'])
def delete_student(student_id):
    result = students_collection.delete_one({"id": student_id})
    if result.deleted_count > 0:
        return jsonify({"message": "Student deleted successfully"}),200
    else:
        return jsonify({"message": "Student not found"}),400



