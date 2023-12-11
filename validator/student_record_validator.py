from marshmallow import Schema, fields, validate, validates, ValidationError
from validator.validate_functions import validate_id
from flask_marshmallow import Marshmallow
import re

ma = Marshmallow()

#FUCNTION TO VALIDATE ALPAHABETS 
def validate_alphabet(value):
    if not re.match("[a-zA-Z]+$", value):
        raise ValidationError('must contian only alphabets')

#FUCNTION TO VALIDATE FIELDS WHICH CAN TAKE SPECILAL CHARACTER AND ALPAHABETS AS INPUT  
def validate_special(value):
    if not re.match("[a-zA-Z0-9,:]+$", value):
        raise ValidationError('must contian only alphabets')

exam_types = [
    "MID_TERM_I",
    "MID_TERM_II",
    "MID_TERM-III",
    "QUARTERLY",
    "HALF_YEARLY",
    "ANNUAL",
]

#FUNCTION TO VALIDATE RANK FIELD
def validate_rank(data):
    if data == "U/A" or (isinstance(data, int) and data > 0):
        return
    raise ValidationError("Rank must be an integer or 'U/A'.")

#SCHEMA FOR SUBJECTS
class SubjectSchema(Schema):
    subject_code = fields.Str(required=True,validate=validate_id)
    teacher_id = fields.Str(required=True,validate = validate_id)

#SCHEMA FOR  MARKS
class MarksSchema(Schema):
    subject_code = fields.Str(required=True,validate=validate_id)
    mark = fields.Int(
        required=True,
        validate=validate.Range(min=0, max=200)  
    )
    status = fields.Str(required=True,validate=validate.OneOf(["pass","fail","PASS","FAIL"]))

#SCHEMA FOR EXAM
class ExamSchema(Schema):
    exam_date = fields.DateTime(required=True)
    marks = fields.Nested(MarksSchema, many=True,required = True)
    total = fields.Int(required=True,validate=validate.Range(min=0))
    average = fields.Float(required=True,validate =validate.Range(min=0.0))
    rank = fields.Field(required=True,validate=validate_rank) 
    result = fields.Str(required=True,validate=validate.OneOf(["pass","fail","PASS","FAIL"]))
    comments = fields.Str()

#SCHEMA FOR STUDENT RECORED
class StudentRecordSchema(Schema):
    id = fields.Str(required=True,validate=validate_id)
    roll_number = fields.Int(required=True,validate=validate.Range(min=1))
    standard = fields.Str(required=True,validate=validate_alphabet)
    section = fields.Str(required=True,validate=validate_alphabet)
    subjects = fields.Nested(SubjectSchema, many=True,required = True)
    exam = fields.Dict(
        keys=fields.Str(validate=validate.OneOf(exam_types)),  
        values=fields.Nested(ExamSchema)
    )

#SCHEMA FOR LIST OF STUDENT RECORED
class StudentRecordListSchema(Schema):
    student_records = fields.List(fields.Nested(StudentRecordSchema,required =True))
    academic_year = fields.Int(required =True ,validate = validate.Range(min=1900,max=3000))

#FUNCTION TO PERFORM CALCULATION OF TOATL , AVERAGE , STATUS
def calcualtions(data):
    data["total"] = 0
    data["average"] = 0.0
    data["result"] = "pass"
    if(len(data["marks"]) <5 or len(data["marks"])>6):
        return "insufficent "
    for i in range(len(data["marks"])):
        data["total"] += data["marks"][i]["mark"]

        data["marks"][i]["status"] = "pass" if data["marks"][i]["mark"] >35 else "fail"
        if(data["marks"][i]["status"].lower() == "fail" ):
            data["result"] = "fail"
    data["average"] = data["total"]/ len(data["marks"])
    print(data)
    return data




#SAMPLE STUDENT RECORED
'''{"student_records":[{
        "_id": "652c0f86f4cd83cc4b3be98c",
        "id": "MYT094",
        "roll_number": 94,
        "standard": "X",
        "section": "B",
        "subjects": [
            {
                "subject_code": "SUB001",
                "teacher_id": "TEA001"
            },
            {
                "subject_code": "SUB002",
                "teacher_id": "TEA002"
            },
            {
                "subject_code": "SUB003",
                "teacher_id": "TEA003"
            },
            {
                "subject_code": "SUB004",
                "teacher_id": "TEA004"
            },
            {
                "subject_code": "SUB005",
                "teacher_id": "TEA005"
            }
        ],
        "exam": {
            "ANNUAL": {
                "exam_date": "2005-10-10T09:11:11Z",
                "marks": [
                    {
                        "subject_code": "SUB001",
                        "mark": 99,
                        "status": "pass"
                    },
                    {
                        "subject_code": "SUB002",
                        "mark": 99,
                        "status": "pass"
                    },
                    {
                        "subject_code": "SUB003",
                        "mark": 94,
                        "status": "pass"
                    },
                    {
                        "subject_code": "SUB004",
                        "mark": 99,
                        "status": "pass"
                    },
                    {
                        "subject_code": "SUB005",
                        "mark": 94,
                        "status": "pass"
                    }
                ],
                "total": 485,
                "average": 97.0,
                "rank": 1,
                "result": "pass",
                "comments": "NONE"
            }
        }
    },
    {
        "_id": "652c0f70f4cd83cc4b3be98b",
        "id": "MYT095",
        "roll_number": 95,
        "standard": "X",
        "section": "B",
        "subjects": [
            {
                "subject_code": "SUB001",
                "teacher_id": "TEA001"
            },
            {
                "subject_code": "SUB002",
                "teacher_id": "TEA002"
            },
            {
                "subject_code": "SUB003",
                "teacher_id": "TEA003"
            },
            {
                "subject_code": "SUB004",
                "teacher_id": "TEA004"
            },
            {
                "subject_code": "SUB005",
                "teacher_id": "TEA005"
            }
        ],
        "exam": {
            "ANNUAL": {
                "exam_date": "2005-10-10T09:11:11Z",
                "marks": [
                    {
                        "subject_code": "SUB001",
                        "mark": 90,
                        "status": "pass"
                    },
                    {
                        "subject_code": "SUB002",
                        "mark": 99,
                        "status": "pass"
                    },
                    {
                        "subject_code": "SUB003",
                        "mark": 94,
                        "status": "pass"
                    },
                    {
                        "subject_code": "SUB004",
                        "mark": 99,
                        "status": "pass"
                    },
                    {
                        "subject_code": "SUB005",
                        "mark": 94,
                        "status": "pass"
                    }
                ],
                "total": 476,
                "average": 95.2,
                "rank": 2,
                "result": "pass",
                "comments": "NONE"
            }
        }
    }
    
],
        "academic_year":2023
        }


'''
