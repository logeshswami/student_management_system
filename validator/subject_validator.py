from marshmallow import Schema, fields,validate,ValidationError,validates
from flask_marshmallow import Marshmallow
from validator.validate_functions import validate_alphabet,validate_special,validate_id
import re


ma = Marshmallow()

#Schema for subjects
class SubjectSchema(Schema):
    subject_code = fields.Str(required=True,validate=validate_id )
    subject_name = fields.Str(required=True,validate= validate_alphabet)
    min_mark = fields.Int(required =True,validate= validate.Range(min=0,max=0))
    max_mark = fields.Int(required =True,validate = validate.Range(min=100,max=200))
    pass_percentage = fields.Int(requierd =True, validate = validate.Range(min=35,max=70))
    board = fields.Str(required = True)
    standard_type = fields.Str(required =True)
    @validates("board")
    def validate_board(self,value):
        if value not in ["STATE-BOARD","CBSE","ICSE"]:
            raise ValidationError("Invalid board type")
    @validates("standard_type")
    def validate_standard(self,value):
        if value not in ["PRIMARY","HIGHER-SECONDARY"]:
            raise ValidationError("invalid standard type")

#Schema for list of subjects      
class SubjectListSchema(Schema):
    subject_records = fields.List(fields.Nested(SubjectSchema,required =True))

#Sample Subject recored
'''
{"subject_records":[{
  
        "subject_code": "SUBJ001",
        "subject_name": "English",
        "min_mark": 0,
        "max_mark": 100,
        "pass_percentage" : 35,
        "board" : "CBSE",
        "standard_type" : "PRIMARY"
    
}]}

'''