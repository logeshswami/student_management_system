# STUDENT MANAGEMENT SYSTEM USING FLASK AND MONGO DB

## Introduction

This project contains api required for performing crud operations related to student management such as student basic information, students academic records, subject details ,teacher details etc along with validation for request data.

---

## Requirements

This projects requires **flask** maintaining backend routes , **mongo db** for database, **pymongo** for performing python mongo connectivity , **flak-marshmallow** for validating input requrest data for the routes.

---

## Modules

### 1. Student CRUD
<br>
This module contain the following routes:
<br><br>
**/student** 
<br><br>
Using **POST** method to this route we can insert student records and the records will be inserted only if the request data satisfies the required format, pass array of inputs with
**student_records**  key and academic_year with **academic_year** as key. 
<br><br>
Using **GET** method to this route all the student records will be retured as response.
<br><br>
**/student/pagination**
<br><br>
Using **GET** method to this route and passing **page_no** in request params you can perform pagination.
<br><br>
**/student/<string:student_id>**
<br><br>
Using **GET** method to this route by passing **student_id** in request URL you can able to retrive a specific student details.
<br><br>
Using **PUT** method to this route by passing **student_id** in request URL and form data in json format in request body you can update personl_information of students, data will be updated only if satisfied the validition criteria for student records.
<br><br>
Using **DELETE** method to this route by passing **student_id** in request URL you can delete that particular student data from the database
<br><br>
**Sample format for student records**
```
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
```
<br><br>
### 2. Subject CRUD
<br><br>
This module contain the following routes
<br><br>
**/subjects**
<br><br>
Using **POST** request to this route subject details can be inserted into database only if the request data satisfies the required format, give array of inputs with subject_records as key .
<br><br>
Using **GET** request for this route all the subject records are retrived from database and sent as response.
<br><br>
**/subjects/pagination**
<br><br>
Using **GET** request to this route pagination can be performed in the subject collection.
<br><br>
**/subjects/<string:subject_code>**
<br><br>
Usign **GET**  to this route request by passig the **subject_code** in request URL specific subject detail can be retrived from the database.
<br><br>
Using **PUT** request to this route by passing the **subject_code** in request URL and details to be updated in request body subject record will be updated.
<br><br>
Using **DELETE** request to this route by passing the **subject_code**  in the request URL subject with given code will be deleted from the database.
<br><br>
**Sample format for subject data**
```
{"subject_records":[{
  
        "subject_code": "SUB001",
        "subject_name": "English",
        "min_mark": 0,
        "max_mark": 100,
        "pass_percentage" : 35,
        "board" : "CBSE",
        "standard_type" : "PRIMARY"
    
}]}
```


### 3. Teacher CRUD
<br><br>
This module conatin the following routes:
<br><br>
**/teacher**
<br><br>
Using **POST** request to this route teacher details can be inserted into database only if the request data satisfies the required format for teachre record, give array of records with teacher_records as key.
<br><br>
Using **GET** requrest to this route all the teacher details are retrived from the database and sent as response.
<br><br>
**/teacher/pagination**
<br><br>
Using **GET**request to this route by specifing the page_no in request params pagination can be performed for teacher collection
<br><br>
**/teacher/<string:teacher_id>**
<br><br>
Using **GET** request to this route by specifing the **teacher_id** in request URL specific teacher record with matching **teacher_id** can be retrive from the database and sent as response.
<br><br>
Using **PUT** request to this route by specifing the **teacher_id** in the request URL and updated details in the request body details will be updated  after validating the request data for that teacher.
<br><br>
Using **DELETE** request to this route by specifing the **teacher_id** in the request URL specific teacher record will be removed from the database.
<br><br>
**/teachersub/<string:sub_code>**
<br><br>
Using **GET** request to this route by specifing the **subject_code** in the request URL
subject detail with that subject_code will be sent as response.
<br><br>
**Sample record format for teachers**
```
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
```

### 4.Student_Record CRUD
<br><br>
This module contain the following routes:
<br><br>
**/student_records**
<br><br>
Using **POST** request to this route sutent acacdemic_year details will be inserted into the database, academic year of the student should be passed in request params and json data for student record should be passed in the request body, details will be inserted only if it passed the validation.
<br><br>
Using **GET** request to this route and passing the academic_year details at request params all the student records for that academic year will be retrived and sent as response.
<br><br>
**/student_records/pagination**
<br><br>
Using this route by passing page_no in request params pagination can be performed for student record collection
**/student_records/<string:student_record_id>**
<br><br>
Using  **GET** request to this route by passing student id in request URL and academic_year in request params specifc student detail will be retrived and sent as response from the database.
<br><br>
Using **PUT** request to this route by passing student id in request URL , academic_year in request params ,update information in request body record will be update in database only if validation satisfied for that data.
<br><br>
Usiing **DELETE** request to this route by passing student id in request URL and academic_year in request params student with given id for that academic year will be deleted from the database.
<br><br>
**/student_records/insert_mark/<string:student_record_id>**
<br><br>
Using **PUT** request to this route by passing student id in request URL,academic_year ,exam_type in request params and mark details in request body exam details for the specifed exam_type will be inserte into database using update operation.
<br><br>
**/studnet_records/calculate_rank**
<br><br>
Using **PUT** request to this route by passing academic_year,standard,exam_type in request params  rank will be updated for the given exam_type for the students belongs to given standard and academic year only if their overall status if pass.
<br><br>
**Sample record format for student record collection**
```
{"student_records":[
    {
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
```

