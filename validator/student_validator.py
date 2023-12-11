from marshmallow import Schema, fields,validate,ValidationError,validates
from flask_marshmallow import Marshmallow
from validator.validate_functions import validate_alphabet,validate_special,validate_id,validate_address,month
import re

ma = Marshmallow()



#Fucntion to validate gross income    
def validate_gross_income(value):
         if value not in ["< 3 LAKHS","> 5 LAKHS && 10 LAKHS <","> 10 LAKHS && 15 LAKHS <","> 15 LAKHS && 20 LAKHS <","> 20 LAKHS"]:
              raise ValidationError("given value for gross income is invalid")
    

#Schema to validate Identifcation marks
class IdentifyMarkSchema(Schema):
        location = fields.Str(require = True,validate=validate.Length(min=3, max=10))
        identification_type = fields.Str(required = True)
        identification_marks_description = fields.Str(required = True,validate=validate_alphabet)
        @validates("identification_type")
        def validate_identification_mark(self,value):
                if value not in ["SCAR","WOUND","MOLE","COLOR-PATCH"] :
                    raise ValidationError("Invalid identification type")

#Schema for address
class AddressSchema(Schema):
        address_line_1 = fields.Str(required = True,validate=validate_address)
        address_line_2 = fields.Str(required = True,validate=validate_address)
        address_line_3 = fields.Str(required = True,validate=validate_address)
        nationality = fields.Str(required = True,validate=validate_alphabet)
        locality = fields.Str(required = True,validate=validate_alphabet)
        pincode = fields.Int(required = True)
       
#Schema for personal informatin       
class PersonalInfoSchema(Schema):
    first_name = fields.Str(required=True,validate=validate_alphabet)
    last_name = fields.Str(required=True,validate=validate_alphabet)
    initial = fields.Str(required = True,validate=validate_alphabet)
    identification_marks =fields.List(fields.Nested(IdentifyMarkSchema,required = True))
    address_info = fields.Nested(AddressSchema,required = True)
    fathers_name = fields.Str(required = True,validate=validate_alphabet)
    mothers_name = fields.Str(required = True,validate=validate_alphabet)
    fathers_occupation =  fields.Str(required = True,validate=validate_special)
    mothers_occupation = fields.Str(required = True,validate=validate_special)
    gross_annual_income = fields.Str(required = True,validate=validate_gross_income)

   
#Schema  for student        
class StudentSchema(Schema):
    id = fields.Str(required=True,validate=validate_id)
    student_name = fields.Str(required=True,validate=validate_alphabet)
    date_of_admission = fields.DateTime(required=True)
    month_of_admission = fields.Str(required =True,validate=validate.OneOf(month))
    personal_information = fields.Nested(PersonalInfoSchema,required=True)

#Schema for list of students
class StudentsListSchema(Schema):
      student_records = fields.List(fields.Nested(StudentSchema,required = True))


#Sample student recored
'''

 {"student_records":[
  {
    "date_of_admission": "2005-10-10T09:11:11Z",
    "id": "MYT094",
    "month_of_admission": "MAR",
    "personal_information": {
      "address_info": {
        "address_line_1": "addressline",
        "address_line_2": "addres",
        "address_line_3": "addres",
        "locality": "urapakam",
        "nationality": "Indian",
        "pincode": 602105
      },
      "fathers_name": "fathersname",
      "fathers_occupation": "Driver",
      "first_name": "student",
      "gross_annual_income": "< 3 LAKHS",
      "identification_marks": [
        {
          "identification_marks_description": "bigmole",
          "identification_type": "MOLE",
          "location": "face"
        }
      ],
      "initial": "S",
      "last_name": "name",
      "mothers_name": "mothersname",
      "mothers_occupation": "homemaker"
    },
    "student_name": "studentname"
  }]}
'''