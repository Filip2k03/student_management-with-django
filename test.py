from collections import defaultdict

# Input QueryDict (representing form data)
data = {
    'csrfmiddlewaretoken': ['d9j5mGzmkz9w9HjsELkd0Ju0SHIVHB3rzKwUK8Cr4q9GlRuhDJa4Wf1XYOF7di2b', 'd9j5mGzmkz9w9HjsELkd0Ju0SHIVHB3rzKwUK8Cr4q9GlRuhDJa4Wf1XYOF7di2b'],
    'name': ['Kyaw Kyaw '],
    'dob': ['2019-11-29'],
    'nrc': ['12/magata(n)918788'],
    'father_name': ['aye aye mg'],
    'mother_name': ['mimi'],
    'phone': ['234567891'],
    'address': ['O'],
    'grade': ['B'],
    'country': ['Thailand'],
    '7': ['7'],
    'subjects[2021][year]': ['2021'],
    'subjects[7][subject1_marks]': ['100.0'],
    'subjects[7][subject2_marks]': ['87.0'],
    'subjects[7][subject3_marks]': ['90.0'],
    'subjects[7][subject4_marks]': ['78.0'],
    'subjects[7][subject5_marks]': ['90.0'],
    'subjects[7][subject6_marks]': ['100.0'],
    '21': ['21'],
    'subjects[2022][year]': ['2022'],
    'subjects[21][subject1_marks]': ['0.0'],
    'subjects[21][subject2_marks]': ['0.0'],
    'subjects[21][subject3_marks]': ['0.0'],
    'subjects[21][subject4_marks]': ['0.0'],
    'subjects[21][subject5_marks]': ['0.0'],
    'subjects[21][subject6_marks]': ['0.0'],
    '3': ['3'],
    'subjects[2023][year]': ['2023'],
    'subjects[3][subject1_marks]': ['100.0'],
    'subjects[3][subject2_marks]': ['90.0'],
    'subjects[3][subject3_marks]': ['90.0'],
    'subjects[3][subject4_marks]': ['90.0'],
    'subjects[3][subject5_marks]': ['90.0'],
    'subjects[3][subject6_marks]': ['90.0']
}

new_data = {
    "csrfmiddlewaretoken": data["csrfmiddlewaretoken"][0],
    "name": data["name"][0],
    "dob": data["dob"][0],
    "nrc": data["nrc"][0],
    "father_name": data["father_name"][0],
    "mother_name": data["mother_name"][0],
    "phone": data["phone"][0],
    "address": data["address"][0],
    "grade": data["grade"][0],
    "country": data["country"][0],
    "subjects": [],
}


subject_years = [
    key.split("[")[1].split("]")[0]
    for key in data.keys()
    if "subjects[" in key and "year" in key
]

for year in subject_years:
    subject = {
        "subject_id": int(data.get(f"{year}", ["0"])[0]),
        "year": int(year),
    }

    for i in range(1, 7):
        subject[f"subject{i}_marks"] = float(
            data.get(f"subjects[{year}][subject{i}_marks]", [0.0])[0]
        )

    new_data["subjects"].append(subject)

print(new_data)
 