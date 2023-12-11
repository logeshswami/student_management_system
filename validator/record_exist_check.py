import requests

def check_record(collection,id,academic_year=""):  
    url= f"http://localhost:5000/{collection}/{id}" 
    if collection =="student_records": 
        response = requests.get(url,params={"academic_year":academic_year})
    else:
        response = requests.get(url)
    
    data = response.text
    print(data)
    if data !="record not found":
        return True
    
    else:
      return False

