
from marshmallow import Schema, fields, validate, ValidationError, validates
from validator.validate_functions import validate_id,month
import re 


def validate_alphabet(value):
    if not re.match(r'^[a-zA-Z]*(?:\s[a-zA-Z]*)*$', value):
        raise ValidationError("Input value error")


def validate_alphanumeric(value):
    if not re.match(r'^[a-zA-Z0-9-:.]*(?:\s[a-zA-Z0-9-:.]*)*$', value):
        raise ValidationError("Input value error")
    
#Schema for Qualification
class QualificationSchema(Schema):
    degree_type = fields.Str(required = True, validate=[validate_alphabet, validate.Length(min=3, max=30)])
    major = fields.Str(required = True, validate=[validate_alphabet, validate.Length(min=2)])
    degree_name = fields.Str(required = True)
    percentage = fields.Float(required = True, validate=validate.Range(min=0, max=100))           
    passed_out_year = fields.Str(required = True)              
    passed_out_month = fields.Str(required = True, validate=validate.OneOf(month))            

#Schema for Documents
class DocumentSchema(Schema):
    document_type = fields.Str(required=True)
    identification_number = fields.Str(required=True, validate=[validate_alphanumeric,validate.Length(min=10, max=20)])
    document_availability_type = fields.Str(required=True, validate=[validate_alphabet, validate.Length(min=3, max=30)])

    @validates("document_type")
    def validate_document_type(self, doc_type):
        if doc_type not in ['AADHAR', 'PAN', 'DRIVING-LICENSE', 'RATION-CARD']:
            raise ValidationError("Input value error")

#Schema for Personal information
class PersonalInfoSchema(Schema):
    address_line_1 = fields.Str(required=True, validate=[validate_alphanumeric, validate.Length(min=3, max=30)])
    address_line_2 = fields.Str(required=True, validate=[validate_alphanumeric, validate.Length(min=3, max=30)])
    address_line_3 = fields.Str(required=True, validate=[validate_alphanumeric, validate.Length(min=3, max=30)]) 
    nationality = fields.Str(required=True, validate=[validate_alphabet, validate.Length(min=3, max=30)])
    martial_status = fields.Str(required=True)
    date_of_birth = fields.DateTime(required=True)
    fathers_name = fields.Str(required=True, validate=[validate_alphabet, validate.Length(min=3, max=30)])
    mother_name = fields.Str(required=True, validate=[validate_alphabet, validate.Length(min=3, max=30)])
    identification_document_details = fields.List(fields.Nested(DocumentSchema, required=True),required=True)


    @validates("martial_status")
    def validate_martial_status(self, value):
        if value not in ['SINGLE', 'MARRIED']:
            raise ValidationError("Input value error")
        
#Schema for Teacher
class TeacherSchema(Schema):
    teacher_id = fields.Str(required=True, validate=validate_id)
    first_name = fields.Str(required= True, validate=[validate_alphabet, validate.Length(min=3, max=30)])
    last_name = fields.Str(required=True, validate=[validate_alphabet, validate.Length(min=1, max=30)])
    gender = fields.Str(required=True)
    subjects = fields.List(fields.Str(required=True, validate=validate_id))
    qualification = fields.List(fields.Nested(QualificationSchema))
    date_of_joining = fields.DateTime(required=True)
    personal_info = fields.Nested(PersonalInfoSchema, required=True)

    
    @validates("gender")
    def validate_gender(self, gender):
        if gender not in ['MALE', 'FEMALE']:
            raise ValidationError("Input value error")

#Schema for List of Teacher      
class TeacherListSchema(Schema):
    teacher_records = fields.List(fields.Nested(TeacherSchema,required = True))

#Sample student records
'''
{"teacher_records":[{
        "teacher_id" : "TEA0010",
        "first_name" : "Amuthaa",
        "last_name" : "A",
        "gender" : "FEMALE",
        "subjects" : [

           "SUB001","SUB002"
        ],
        "qualification" : [
            {
                "degree_type" : "Masters",
                "major" : "English",
                "degree_name" : "Bsc. English",
                "percentage" : 78.5,
                "passed_out_year" : "2016",
                "passed_out_month" : "MAR"
            }
        ],
        "date_of_joining" : "2023-10-09T11:04:37Z",
        "personal_info" : {
            "address_line_1" : "address line one goes here",
            "address_line_2" : "address line two goes here",
            "address_line_3" : "address line three goes here",
            "nationality" : "Indian",
            "martial_status" : "MARRIED",
            "date_of_birth" : "1999-10-09T11:04:37Z",
            "fathers_name" : "father name",
            "mother_name" : "mothers name",
            "identification_document_details" : 
            [
                {
                    "document_type" : "RATION-CARD",
                    "identification_number" : "xxxx-xxxx-xxxx-xxxx",
                    "document_availability_type" : "ORIGINAL"
                }
            ]        
        }    
    }]}
'''