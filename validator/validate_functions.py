import re
from marshmallow import ValidationError

#FUNCTION TO VALIDATE ALPHABETS
def validate_alphabet(value):
   if not re.match(r'^[a-zA-Z]*(?:\s[a-zA-Z]*)*$', value):
        raise ValidationError('must contian only alphabets')

#FUNCTION TO VALIDATE ADDRESS
def validate_address(value):
    if not re.match(r'^[a-zA-Z0-9-:.]*(?:\s[a-zA-Z0-9-:.]*)*$', value):
        raise ValidationError("invalid value given for address")

#FUCNTION TO VALIDATE FELILDS WITH SPECIAL CHARACTERS
def validate_special(value):
    if not re.match("[a-zA-Z0-9,:]+$", value):
        raise ValidationError('must contian only alphabets')

#FUNCTON TO VALIDATE ID
def validate_id(value):
    if not re.match("^[A-Z]{3}[0-9]{3,4}$",value):
        raise ValidationError("invalid format for id")

#FUCNTION TO REMOVE EXTRA SPACES
def remove_extra_spaces(value):
    if isinstance(value, str):
        return ' '.join(value.split())  
    elif isinstance(value, list):
        return [remove_extra_spaces(item) for item in value]
    elif isinstance(value, dict):
        return {key: remove_extra_spaces(val) for key, val in value.items()}
    else:
        return value

#ENUM VALUES FOR MONTHS   
month =['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']



