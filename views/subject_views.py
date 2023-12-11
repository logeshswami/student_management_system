from flask import Blueprint, request, jsonify
from validator.subject_validator import SubjectSchema, SubjectListSchema, ma
from validator.validate_functions import remove_extra_spaces
from dotenv import load_dotenv
from validator.record_exist_check import check_record
from models.subject import subjects_collection
import json
import os

load_dotenv()
subject_schema = SubjectSchema()
subject_list_schema = SubjectListSchema()

subject_bp = Blueprint("subject",__name__)

# INSERT SUBJECT DETAILS
@subject_bp.route('/subjects', methods=['POST'])
def create_subject():
    data = request.json
    record = data["subject_records"]

    err = subject_list_schema.validate(data)
    if not err:
        for subject in record:
            if not check_record("subjects", subject["subject_code"]):
                subject =  remove_extra_spaces(subject)
                result = subjects_collection.insert_one(subject)
            else:
                return f"record with id {subject['subject_code'] } already exist",200

        return jsonify({"message": " All Subject Record created successfully"}),201

    else:
        return err,400

# GET SUBJECT DETAILS


@subject_bp.route('/subjects', methods=['GET'])
def get_subjects():
    subjects = list(subjects_collection.find())
    return json.dumps(subjects, default=str),200

# PAGINATION
@subject_bp.route('/subjects/pagination', methods=['GET'])
def get_subjects_pages():
    page_no = int(request.args.get("page_no"))
    page_length = int(os.environ.get("page_length"))
    subjects = list(subjects_collection.find().skip(
        page_no*page_length).limit(page_length))
    return  json.dumps(subjects, default=str),200

# GET SPECIFIC SUBJECT WITH SUBJECT CODE

@subject_bp.route('/subjects/<string:subject_code>', methods=['GET'])
def get_subject(subject_code):
    subject = subjects_collection.find_one({"subject_code": subject_code})
    if subject:
        return jsonify(str(subject)),200
    return "record not found",404

# UPDATE SUBJECT DETAILS


@subject_bp.route('/subjects/<string:subject_code>', methods=['PUT'])
def update_subject(subject_code):
    data = request.json
    err = subject_schema.validate(data)
    if (not err):
        data = {
            "min_mark": data["min_mark"],
            "max_mark": data["max_mark"],
            "pass_percentage": data["pass_percentage"]
        }
        result = subjects_collection.update_one(
            {"subject_code": subject_code}, {"$set": data})
        if result.modified_count > 0:
            return jsonify({"message": "Subject updated successfully"}),200
        return jsonify({"message": "Subject not updated/subject not found"}),404
    else:
        return err,400

# DELETE SUBJECT DETAILS


@subject_bp.route('/subjects/<string:subject_code>', methods=['DELETE'])
def delete_subject(subject_code):
    result = subjects_collection.delete_one({"subject_code": subject_code})
    if result.deleted_count > 0:
        return jsonify({"message": "Subject deleted successfully"}),200
    return jsonify({"message": "Subject not found"}),404


