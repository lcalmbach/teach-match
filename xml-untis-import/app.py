import pandas as pd
import xml.etree.ElementTree as ET

# Parse the XML file
tree = ET.parse('./untis.xml')
root = tree.getroot()

# Define namespaces
ns = {'ns': 'https://untis.at/untis/XmlInterface'}


def extract_all():
    # Extract teachers
    teachers = []
    for teacher in root.findall('ns:teachers/ns:teacher', ns):
        teacher_id = teacher.get('id')
        surname = teacher.find('ns:surname', ns).text
        teachers.append({'id': teacher_id, 'name': surname})

    # Extract subjects
    subjects = []
    for subject in root.findall('ns:subjects/ns:subject', ns):
        subject_id = subject.get('id')
        subject_name = subject.find('ns:longname', ns).text
        subjects.append({'id': subject_id, 'name': subject_name})

    # Extract time periods
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

    # Extract lessons
    lessons = []
    for lesson in root.findall('ns:lessons/ns:lesson', ns):
        lesson_teacher = lesson.get('teacherid')
        lesson_subject = lesson.get('subjectid')
        lesson_classes = ', '.join([cls.get('classid') for cls in lesson.findall('ns:lessonclasses/ns:lessonclass', ns)])
        
        # Extract the assigned day and period from the lesson times
        for time in lesson.findall('ns:lessontimes/ns:lessontime', ns):
            assigned_day = time.get('day')
            assigned_period = time.get('period')
            
            # Add a new lesson record for each day-period combination
            lessons.append({
                'lesson_teacher': lesson_teacher,
                'lesson_subject': lesson_subject,
                'lesson_classes': lesson_classes,
                'assigned_day': assigned_day,
                'assigned_period': assigned_period
            })

    # Convert the lessons to a DataFrame
    df_lessons = pd.DataFrame(lessons)

    # Create DataFrames for the other sections (already parsed)
    df_teachers = pd.DataFrame(teachers)
    df_subjects = pd.DataFrame(subjects)
    df_timeperiods = pd.DataFrame(timeperiods)

    # Display the lessons table
    # import ace_tools as tools; tools.display_dataframe_to_user(name="Lesson Plan", dataframe=df_lessons)

    # Save to CSV for further usage
    df_lessons.to_csv('lessons.csv', index=False)
    df_teachers.to_csv('teachers.csv', index=False)
    df_subjects.to_csv('subjects.csv', index=False)
    df_timeperiods.to_csv('timeperiods.csv', index=False)

extract_all()