from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Subject
from django.http import HttpResponse
from django.core.paginator import Paginator
import openpyxl
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.core.exceptions import ValidationError


def index(request):
    return render(request, 'index.html')
# --- Student Views ---
#  Detail for students 
# Show student detail
def student_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    subjects = Subject.objects.filter(student=student)  # Fetch subjects for this student
    
    total_marks = 0
    for subject in subjects:
        # Sum marks from each subject
        total_marks += (subject.subject1_marks + subject.subject2_marks +
                        subject.subject3_marks + subject.subject4_marks +
                        subject.subject5_marks + subject.subject6_marks)
    
    return render(request, 'student/student_detail.html', {'student': student, 'subjects': subjects, 'total_marks': total_marks})

# List all students
def student_list(request):
    query = request.GET.get('q', '')  # Get the search query from the URL
    students = Student.objects.all()

    if query:
        students = students.filter(name__icontains=query)  # Filter students by name (case-insensitive)

    paginator = Paginator(students, 3)  # Show 10 students per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'student/student_list.html', {'page_obj': page_obj, 'query': query})

# Create a new student
def create_student(request):
    if request.method == "POST":
        name = request.POST.get('name')
        dob_str = request.POST.get('dob')
        nrc = request.POST.get('nrc')
        father_name = request.POST.get('father_name')
        mother_name = request.POST.get('mother_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        grade = request.POST.get('grade')
        country = request.POST.get('country')
        student_year = request.POST.get('year')  # Get the year for the student

        subject1_marks = request.POST.get('subject1_marks')
        subject2_marks = request.POST.get('subject2_marks')
        subject3_marks = request.POST.get('subject3_marks')
        subject4_marks = request.POST.get('subject4_marks')
        subject5_marks = request.POST.get('subject5_marks')
        subject6_marks = request.POST.get('subject6_marks')

        try:
            dob = timezone.datetime.strptime(dob_str, '%Y-%m-%d').date()
            student = Student.objects.create(
                name=name,
                dob=dob,
                nrc=nrc,
                father_name=father_name,
                mother_name=mother_name,
                phone=phone,
                address=address,
                grade=grade,
                country=country,
                year_id=student_year,  # Set the year for the student
            )

            # Create Subject marks for the student
            Subject.objects.create(
                student=student,
                year=student_year,
                subject1_marks=subject1_marks,
                subject2_marks=subject2_marks,
                subject3_marks=subject3_marks,
                subject4_marks=subject4_marks,
                subject5_marks=subject5_marks,
                subject6_marks=subject6_marks,
            )

            return redirect('student_list')  # After creation, redirect to student list
        except (ValueError, ValidationError) as e:
            error_message = "Invalid data: " + str(e)
            return render(request, 'student/create_student.html', {'error_message': error_message})

    return render(request, 'student/create_student.html')  # Render a form for student creation

def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    existing_subjects = Subject.objects.filter(student=student).order_by('year') # Fetch existing subjects, ordered by year

    if request.method == "POST":
        # Handle the main student data update
        student.name = request.POST.get('name')
        dob_str = request.POST.get('dob')
        student.nrc = request.POST.get('nrc')
        student.father_name = request.POST.get('father_name')
        student.mother_name = request.POST.get('mother_name')
        student.phone = request.POST.get('phone')
        student.address = request.POST.get('address')
        student.grade = request.POST.get('grade')
        student.country = request.POST.get('country')

        # Handle the new subject data
        new_subject_year = request.POST.get('new_subject_year')
        new_subject1_marks = request.POST.get('new_subject1_marks')
        new_subject2_marks = request.POST.get('new_subject2_marks')
        new_subject3_marks = request.POST.get('new_subject3_marks')
        new_subject4_marks = request.POST.get('new_subject4_marks')
        new_subject5_marks = request.POST.get('new_subject5_marks')
        new_subject6_marks = request.POST.get('new_subject6_marks')

        try:
            student.dob = timezone.datetime.strptime(dob_str, '%Y-%m-%d').date()
            student.save()

            # Create a new Subject entry if the new subject form was submitted
            if new_subject_year and new_subject1_marks and new_subject2_marks and new_subject3_marks and new_subject4_marks and new_subject5_marks and new_subject6_marks:
                Subject.objects.create(
                    student=student,
                    year=new_subject_year,
                    subject1_marks=new_subject1_marks,
                    subject2_marks=new_subject2_marks,
                    subject3_marks=new_subject3_marks,
                    subject4_marks=new_subject4_marks,
                    subject5_marks=new_subject5_marks,
                    subject6_marks=new_subject6_marks,
                )

            return redirect('student_list')
        except (ValueError, ValidationError) as e:
            error_message = "Invalid data: " + str(e)
            return render(request, 'student/edit_student.html',
                          {'student': student, 'existing_subjects': existing_subjects, 'error_message': error_message})

    return render(request, 'student/edit_student.html', {'student': student, 'existing_subjects': existing_subjects})
# Delete a student
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    return redirect('student_list')  # After deletion, redirect to student list


# --- Subject Views ---

# List all subjects
def subject_list(request):
    query = request.GET.get('q', '')  # Get the search query from the URL
    subjects = Subject.objects.all()

    if query:
        subjects = subjects.filter(student__name__icontains=query)  # Filter subjects by student name

    paginator = Paginator(subjects, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'subject/subject_list.html', {'page_obj': page_obj, 'query': query})

# Create a new subject
def create_subject(request):
    if request.method == "POST":
        student_id = request.POST.get('student_id')
        year = request.POST.get('year')
        subject1_marks = request.POST.get('subject1_marks')
        subject2_marks = request.POST.get('subject2_marks')
        subject3_marks = request.POST.get('subject3_marks')
        subject4_marks = request.POST.get('subject4_marks')
        subject5_marks = request.POST.get('subject5_marks')
        subject6_marks = request.POST.get('subject6_marks')

        student = get_object_or_404(Student, id=student_id)
        subject = Subject(student=student, year=year, subject1_marks=subject1_marks,
                          subject2_marks=subject2_marks, subject3_marks=subject3_marks,
                          subject4_marks=subject4_marks, subject5_marks=subject5_marks,
                          subject6_marks=subject6_marks)
        subject.save()
        return redirect('subject_list')  # After creation, redirect to subject list
    
    students = Student.objects.all()  # To show students in the create subject form
    return render(request, 'subject/create_subject.html', {'students': students})

# Edit an existing subject
def edit_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    
    if request.method == "POST":
        subject.year = request.POST.get('year')
        subject.subject1_marks = request.POST.get('subject1_marks')
        subject.subject2_marks = request.POST.get('subject2_marks')
        subject.subject3_marks = request.POST.get('subject3_marks')
        subject.subject4_marks = request.POST.get('subject4_marks')
        subject.subject5_marks = request.POST.get('subject5_marks')
        subject.subject6_marks = request.POST.get('subject6_marks')
        subject.save()
        return redirect('subject_list')  # After edit, redirect to subject list
    
    return render(request, 'subject/edit_subject.html', {'subject': subject})  # Show subject data in form

# Delete a subject
def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    subject.delete()
    return redirect('subject_list')  # After deletion, redirect to subject list

# --- Export Students to XLSX ---
def export_students(request):
    # Get all students
    students = Student.objects.all()

    # Create a workbook and a worksheet
    wb = Workbook()
    ws = wb.active
    ws.title = "Students"

    # Define the headers
    headers = ['ID', 'Name', 'DOB', 'NRC', 'Father Name', 'Mother Name', 'Phone', 'Address', 'Grade', 'Country']
    ws.append(headers)

    # Add student data to the Excel sheet
    for student in students:
        ws.append([student.id, student.name, student.dob, student.nrc, student.father_name,
                   student.mother_name, student.phone, student.address, student.grade, student.country])

    # Set the column widths
    for col in range(1, len(headers) + 1):
        column = get_column_letter(col)
        max_length = 0
        for row in ws.iter_rows(min_col=col, max_col=col):
            for cell in row:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
        adjusted_width = (max_length + 2)
        ws.column_dimensions[column].width = adjusted_width

    # Return the file as an HTTP response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=students.xlsx'
    wb.save(response)
    return response


# --- Import Students from XLSX ---
def import_students(request):
    if request.method == "POST" and request.FILES["excel_file"]:
        excel_file = request.FILES["excel_file"]
        fs = FileSystemStorage()
        file_path = fs.save(excel_file.name, excel_file)
        file_url = fs.url(file_path)

        # Open the uploaded Excel file
        wb = openpyxl.load_workbook(file_path)
        ws = wb.active

        # Iterate through the rows and insert the data into the database
        for row in ws.iter_rows(min_row=2, values_only=True):
            student_data = {
                'id': row[0],
                'name': row[1],
                'dob': row[2],
                'nrc': row[3],
                'father_name': row[4],
                'mother_name': row[5],
                'phone': row[6],
                'address': row[7],
                'grade': row[8],
                'country': row[9],
            }
            # Create or update the student data in the database
            Student.objects.update_or_create(id=student_data['id'], defaults=student_data)

        # Provide a success message
        messages.success(request, "Students imported successfully!")
        return redirect('student_list')

    return render(request, 'student/import_students.html')

# Import subjects from XLSX
def import_subjects(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        wb = openpyxl.load_workbook(file)
        ws = wb.active

        for row in ws.iter_rows(min_row=2, values_only=True):
            student_name, year, subject, subject1_marks, subject2_marks, subject3_marks, subject4_marks, subject5_marks, subject6_marks, total_marks = row
            
            # Fetch the student based on the name (assuming the name is unique, else modify to use another identifier)
            try:
                student = Student.objects.get(name=student_name)
            except Student.DoesNotExist:
                messages.error(request, f"Student {student_name} not found in the database.")
                continue  # Skip the current row if the student does not exist

            # Create a new Subject record
            Subject.objects.create(
                student=student,
                year=year,
                subject1_marks=subject1_marks,
                subject2_marks=subject2_marks,
                subject3_marks=subject3_marks,
                subject4_marks=subject4_marks,
                subject5_marks=subject5_marks,
                subject6_marks=subject6_marks
            )
        
        messages.success(request, 'Subjects imported successfully!')
    
    return render(request, 'subject/import_subject.html')


# Export Subjects to XLSX
def export_subjects(request):
    subjects = Subject.objects.select_related('student')  # Fetch related student data efficiently

    # Create a workbook and add a worksheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Subjects"

    # Add column headers
    headers = ["Student Name", "Year", "Subject", "Marks 1", "Marks 2", "Marks 3", "Marks 4", "Marks 5", "Marks 6", "Total Marks"]
    for col_num, header in enumerate(headers, 1):
        ws[get_column_letter(col_num) + '1'] = header

    # Add subject data rows
    for row_num, subject in enumerate(subjects, 2):
        ws[get_column_letter(1) + str(row_num)] = subject.student.name  # Add student name
        ws[get_column_letter(2) + str(row_num)] = subject.year
        ws[get_column_letter(3) + str(row_num)] = f"Subject {row_num - 1}"
        ws[get_column_letter(4) + str(row_num)] = subject.subject1_marks
        ws[get_column_letter(5) + str(row_num)] = subject.subject2_marks
        ws[get_column_letter(6) + str(row_num)] = subject.subject3_marks
        ws[get_column_letter(7) + str(row_num)] = subject.subject4_marks
        ws[get_column_letter(8) + str(row_num)] = subject.subject5_marks
        ws[get_column_letter(9) + str(row_num)] = subject.subject6_marks
        ws[get_column_letter(10) + str(row_num)] = subject.total_marks

    # Response with the XLSX file
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = "attachment; filename=subjects.xlsx"
    wb.save(response)
    return response