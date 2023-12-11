from flask import Blueprint, request, jsonify
from pymongo import MongoClient
import json
from flask_marshmallow import Marshmallow
from validator.teacher_validator import TeacherSchema, TeacherListSchema
from validator.validate_functions import remove_extra_spaces
from validator.record_exist_check import check_record
from models.teacher import teacher_collection,subjects_collection
from dotenv import load_dotenv
import os

load_dotenv()
teacher_schema = TeacherSchema()
teacher_list_Schema = TeacherListSchema()

teacher_bp = Blueprint("teacher",__name__)

# INSERT TEACHER DETAILS

@teacher_bp.route('/teacher', methods=['POST'])
def create_teacher():
    data = request.json
    records = data["teacher_records"]
    err = teacher_list_Schema.validate(data)
    if not err:
        for teacher in records:
            if not check_record("teacher", teacher["teacher_id"]):
                teacher= remove_extra_spaces(teacher)
                result = teacher_collection.insert_one(teacher)
            else:
                return f"record with id {teacher['teacher_id'] } already exist",200

        return jsonify({"message": "ALL Teacher created successfully"}),200
    else:
        return err ,400

# GET TEACHER DETAILS


@teacher_bp.route('/teacher', methods=['GET'])
def get_teacher_records():
    teacher_record = list(teacher_collection.find())
    return json.dumps(teacher_record, default=str),200

# PAGINATION


@teacher_bp.route('/teacher/pagination', methods=['GET'])
def get_teacher_records_pagination():
    page_no = int(request.args.get("page_no"))
    page_length = int(os.environ.get("page_length"))
    teacher_record = list(teacher_collection.find().skip(
        page_no*page_length).limit(page_length))
    return json.dumps(teacher_record, default=str),200

# GET SPECIFIC TEACHER DETAILS WITH TEACHER ID


@teacher_bp.route('/teacher/<string:teacher_id>', methods=['GET'])
def get_teacher_record(teacher_id):
    teacher_record = teacher_collection.find_one({"teacher_id": teacher_id})
    if teacher_record:
        return json.dumps(teacher_record, default=str),200
    return "record not found",404

# UPDATE TEACHER DETAILS


@teacher_bp.route('/teacher/<string:teacher_id>', methods=['PUT'])
def update_teacher_record(teacher_id):
    data = request.json
    err = teacher_schema.validate(data)
    if not err:
        data = remove_extra_spaces(data)
        result = teacher_collection.update_one(
            {"teacher_id": teacher_id}, {"$set": data})
        if result.modified_count > 0:
            return jsonify({"message": "Teacher Record updated successfully"}),200
        return jsonify({"message": "Teacher Record not found"}),404
    else:
        return err,400

# DELETE TEACHER DETAILS


@teacher_bp.route('/teacher/<string:teacher_id>', methods=['DELETE'])
def delete_teacher_record(teacher_id):
    result = teacher_collection.delete_one({"teacher_id": teacher_id})
    if result.deleted_count > 0:
        return jsonify({"message": "Teacher Record deleted successfully"}),200
    return jsonify({"message": "Teacher Record not found"}),404

# GET SUBJECT OF THE TEACHER WITH TEACHER ID


@teacher_bp.route('/teachersub/<string:sub_code>', methods=['GET'])
def get_teacher_subdetails(sub_code):
    result = subjects_collection.find_one({"subject_code": sub_code})
    if result:
        return jsonify(str(result)),200
    return jsonify({"message": "Subjects not found"}),404


