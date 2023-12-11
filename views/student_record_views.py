from flask import Blueprint, request, jsonify
from validator.student_record_validator import StudentRecordSchema, StudentRecordListSchema,ExamSchema, ma,calcualtions
import json
from validator.validate_functions import remove_extra_spaces
from validator.record_exist_check import check_record
from models.student_record import student_records_collection
from dotenv import load_dotenv
import os

load_dotenv()
student_record_bp = Blueprint("student_record",__name__)
student_record_schema = StudentRecordSchema()
student_record_list_schema = StudentRecordListSchema()
exam_schema = ExamSchema()

# INSERT STUDENT RECORD


@student_record_bp.route('/student_records', methods=['POST'])
def create_student_record():
    data = request.json
    records = data["student_records"]
    academic_year = data["academic_year"]
    err = student_record_list_schema.validate(data)
    if not err:
        for student in records:
            if not check_record("student_records", student["id"], academic_year):
                student = remove_extra_spaces(student)
                collection = student_records_collection[academic_year]
                roll_status = collection.find_one({"roll_number":student["roll_number"], "standard":student["standard"] })
                if not roll_status:
                    result = collection.insert_one(student)
                else:
                    return "Already other student exist for the given roll number in this standard"
            else:
                return f"record with id {student['id'] } already exist",200

        return jsonify({"message": " All Student Record created successfully"}),201

    else:
        return err,400

# GET STUDENT RECORD


@student_record_bp.route('/student_records', methods=['GET'])
def get_student_records():
    academic_year = request.args.get("academic_year")
    student_records = list(student_records_collection[academic_year].find())
    return json.dumps(student_records, default=str),200

# PAGINATION


@student_record_bp.route('/student_records/pagination', methods=['GET'])
def get_student_records_pages():
    academic_year = request.args.get("academic_year")
    page_no = int(request.args.get("page_no"))
    page_length = int(os.environ.get("page_length"))
    student_records = list(student_records_collection[academic_year].find().skip(
        page_no*page_length).limit(page_length))
    return json.dumps(student_records, default=str),200



# GET SPECIFC STUDENT RECORD
@student_record_bp.route('/student_records/<string:student_record_id>', methods=['GET'])
def get_student_record(student_record_id):
    academic_year = request.args.get("academic_year")
    student_record = student_records_collection[academic_year].find_one(
        {"id": student_record_id})
    if student_record:
        return str(student_record),200
    return "record not found",404


# INSERT MARKS
@student_record_bp.route('/student_records/insert_mark/<string:student_record_id>', methods=['PUT'])
def insert_mark(student_record_id):
    academic_year = request.args.get("academic_year")
    exam_type = request.args.get("exam_type")
    data = request.json
    data = calcualtions(data)
    if (data == "insufficent "):
       return "plealse check number of subjects to which you gave marks",200
    data = remove_extra_spaces(data)
    err = exam_schema.validate(data)
    if not err:
        result = student_records_collection[academic_year].update_one(
            {"id": student_record_id}, {"$set": {f"exam.{exam_type}": data}})
        if result.modified_count > 0:
            return jsonify({"message": "Student Record updated successfully"}),200
        return jsonify({"message": "Student Record not found"}),404
    else:
        return err,400


# UPDATE STUDENT RECORD
@student_record_bp.route('/student_records/<string:student_record_id>', methods=['PUT'])
def update_student_record(student_record_id):
    academic_year = request.args.get("academic_year")
    data = request.json
    err = student_record_schema.validate(data)
    if not err:
        update_data = remove_extra_spaces(data["exam"])
        result = student_records_collection[academic_year].update_one(
            {"id": student_record_id}, {"$set": update_data})
        if result.modified_count > 0:
            return jsonify({"message": "Student Record updated successfully"}),200
        return jsonify({"message": "Student Record not found"}),404
    else:
        return err,400

# DELETE STUDENT RECORD


@student_record_bp.route('/student_records/<string:student_record_id>', methods=['DELETE'])
def delete_student_record(student_record_id):
    academic_year = request.args.get("academic_year")
    result = student_records_collection[academic_year].delete_one(
        {"id": student_record_id})
    if result.deleted_count > 0:
        return jsonify({"message": "Student Record deleted successfully"}),200
    return jsonify({"message": "Student Record not found"}),404

# CALCULATE RANK FOR STUDENTS


@student_record_bp.route("/student_records/calculate_rank", methods=['PUT'])
def find_rank():
    academic_year = request.args.get("academic_year")
    standard = request.args.get("standard")
    exam_type = request.args.get("exam_type")
    print(exam_type)

    records = student_records_collection[academic_year].find(
        {"standard": standard}).sort(f"exam.{exam_type}.total", -1)
    index = 1
    for student in records:
        print(student["exam"][exam_type])
        if ((student["exam"][exam_type]["result"]).lower() != "fail"):
            student_records_collection[academic_year].update_one(
                {"id": student["id"]}, {"$set": {F"exam.{exam_type}.rank": index}})
            index += 1

    return "rank calculated",200


