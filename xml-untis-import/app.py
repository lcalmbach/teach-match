import pandas as pd
import xml.etree.ElementTree as ET

input_file = './untis.xml'
output_file = './untis_utf8.xml'

# Open the file with ISO-8859-1 encoding and save it as UTF-8
with open(input_file, 'r', encoding='iso-8859-1') as file:
    content = file.read()

with open(output_file, 'w', encoding='utf-8') as file:
    file.write(content)

# Parse the XML file
with open(output_file, 'r') as file:
    tree = ET.parse(file)

# Get the root of the XML tree
root = tree.getroot()
# Define namespaces
ns = {'ns': 'https://untis.at/untis/XmlInterface'}


def extract_teachers():
    # Extract teachers
    teachers = []
    for teacher in root.findall('ns:teachers/ns:teacher', ns):
        teacher_id = teacher.get('id')
        surname = teacher.find('ns:surname', ns).text
        payroll_number_node = teacher.find('ns:payrollnumber', ns)
        teacher_department_node = teacher.find('ns:teacher_department', ns)

        # Safely handle missing nodes
        payroll_number = payroll_number_node.text if payroll_number_node is not None else None
        teacher_department = teacher_department_node.get('id') if teacher_department_node is not None else None
        print(f"Teacher ID: {teacher_id}, Surname: {surname}, Payroll: {payroll_number}, Department: {teacher_department}")
        teachers.append({
            'id': teacher_id,
            'name': surname,
            'payroll_number': payroll_number,
            'teacher_department': teacher_department
        })
    return teachers

def extract_subjects():
    subjects = []
    for subject in root.findall('ns:subjects/ns:subject', ns):
        subject_id = subject.get('id')
        subject_name = subject.find('ns:longname', ns).text
        subjects.append({'id': subject_id, 'name': subject_name})

def extract_timeperiods():
    timeperiods = []
    for period in root.findall('ns:timeperiods/ns:timeperiod', ns):
        period_id = period.get('id')
        day = period.find('ns:day', ns).text
        starttime = period.find('ns:starttime', ns).text
        endtime = period.find('ns:endtime', ns).text
        timeperiods.append({
            'id': period_id, 
            'day': day, 
            'start': starttime, 
            'end': endtime
        })

def extract_lessons():
    lessons = []
    for lesson in root.findall('ns:lessons/ns:lesson', ns):
        lesson_id = lesson.get('id')  # Get the lesson ID

        # Safely handle missing <lesson_teacher>
        lesson_teacher_element = lesson.find('ns:lesson_teacher', ns)
        if lesson_teacher_element is not None:
            lesson_teacher = lesson_teacher_element.get('id')
        else:
            lesson_teacher = None  # Or a default value, e.g., "Unknown"

        # Safely handle <lesson_subject>
        lesson_subject_element = lesson.find('ns:lesson_subject', ns)
        if lesson_subject_element is not None:
            lesson_subject = lesson_subject_element.get('id')
        else:
            lesson_subject = None

        # Extract lesson classes safely
        lesson_classes_element = lesson.find('ns:lesson_classes', ns)
        if lesson_classes_element is not None:
            lesson_classes = lesson_classes_element.get('id')
        else:
            lesson_classes = None

        # Extract other attributes
        teacher_value = lesson.find('ns:teacher_value', ns).text if lesson.find('ns:teacher_value', ns) is not None else ''
        effective_begin_date = lesson.find('ns:effectivebegindate', ns).text if lesson.find('ns:effectivebegindate', ns) is not None else ''
        effective_end_date = lesson.find('ns:effectiveenddate', ns).text if lesson.find('ns:effectiveenddate', ns) is not None else ''

        # Extract times
        for time in lesson.findall('ns:times/ns:time', ns):
            assigned_day = time.find('ns:assigned_day', ns).text if time.find('ns:assigned_day', ns) is not None else ''
            assigned_period = time.find('ns:assigned_period', ns).text if time.find('ns:assigned_period', ns) is not None else ''
            assigned_starttime = time.find('ns:assigned_starttime', ns).text if time.find('ns:assigned_starttime', ns) is not None else ''
            assigned_endtime = time.find('ns:assigned_endtime', ns).text if time.find('ns:assigned_endtime', ns) is not None else ''

            # Append a record for each time entry
            lessons.append({
                'lesson_id': lesson_id,
                'lesson_teacher': lesson_teacher,
                'lesson_subject': lesson_subject,
                'lesson_classes': lesson_classes,
                'teacher_value': teacher_value,
                'effective_begin_date': effective_begin_date,
                'effective_end_date': effective_end_date,
                'assigned_day': assigned_day,
                'assigned_period': assigned_period,
                'assigned_starttime': assigned_starttime,
                'assigned_endtime': assigned_endtime,
            })

def main():
    lessons = extract_lessons()
    df_lessons = pd.DataFrame(lessons)
    teachers = extract_teachers()
    df_teachers = pd.DataFrame(teachers)
    subjects = extract_subjects()
    df_subjects = pd.DataFrame(subjects)
    timeperiods = extract_timeperiods()
    df_timeperiods = pd.DataFrame(timeperiods)
    
    df_lessons.to_csv('lessons.csv', index=False, sep=';', encoding='utf-8')
    df_teachers.to_csv('teachers.csv', index=False, sep=';', encoding='utf-8')
    df_subjects.to_csv('subjects.csv', index=False, sep=';', encoding='utf-8')
    df_timeperiods.to_csv('timeperiods.csv', index=False, sep=';', encoding='utf-8')

if __name__ == '__main__':
    main()