import os
import json
import pymysql
import pandas as pd
from connection import get_connection
import xml.etree.ElementTree as ET



connection = get_connection('assignment_3')

# Read CSV using pandas
course = pd.read_csv('csv/course.csv')
enrollment = pd.read_csv('csv/enrollment.csv')
student = pd.read_csv('csv/student.csv')
#define xml and json locations
json_data_location = 'data.json'
xml_data_location = 'data.xml'


# Insert data into MySQL
with connection.cursor() as cursor:
    for index, row in student.iterrows():
        print(row)
        cursor.execute(
            "INSERT INTO Student (student_id, name, age) VALUES (%s, %s, %s)",
            (row['student_id'], row['name'], row['age'])
        )
    for index, row in course.iterrows():
        cursor.execute(
            "INSERT INTO Course (course_id, course_name, credits) VALUES (%s, %s, %s)",
            (row['course_id'], row['course_name'], row['credits'])
        )
    for index, row in enrollment.iterrows():
        cursor.execute(
            "INSERT INTO Enrollment (student_id, course_id) VALUES (%s, %s)",
            (row['student_id'], row['course_id'])
        )

    # Commit the transaction
    connection.commit()

# Helper function to get or create a category
def get_or_create_author(cursor, data):

    author_id, author_name, nationality = data

    cursor.execute(f"SELECT {author_id} FROM Author WHERE author_id = %s", (author_id,))
    result = cursor.fetchone()
    if result:
        return result[0]  # get the exist id by query
    else:
        cursor.execute("INSERT INTO Author (author_id, name, nationality) VALUES (%s, %s, %s)", (author_id, author_name, nationality,))
        return cursor.lastrowid  # get the id [generate by database]

def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    with connection.cursor() as cursor:
        # return a list from findall
        for product in root.findall('book'):
            book_id = product.find('book_id').text
            title = product.find('title').text
            publication_year = int(product.find('publication_year').text)
            cursor.execute("INSERT INTO Book (book_id, title, publication_year) VALUES (%s, %s, %s)", (book_id, title, publication_year))

            for author in product.findall('authors/author'):
                author_id = author.find('author_id').text
                author_name = author.find('name').text
                nationality = author.find('nationality').text

                data = author_id, author_name, nationality
                
                s = get_or_create_author(cursor, data)
                cursor.execute("INSERT INTO Book_Author (book_id, author_id) VALUES (%s, %s)", (book_id, author_id))

        connection.commit()

parse_xml(xml_data_location)


# Helper function to get or create a category
def get_or_create_employee(data, cursor):

    employee_id, name, position = data

    cursor.execute("SELECT employee_id FROM Employee WHERE employee_id = %s", (employee_id, ))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        cursor.execute("INSERT INTO Employee (employee_id, name, position) VALUES (%s, %s, %s)", (employee_id, name, position,))
        return cursor.lastrowid


def parse_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    with connection.cursor() as cursor:
        for item in data:
            cursor.execute("INSERT INTO Project (project_id, project_name, deadline) VALUES (%s, %s, %s)", (item['project_id'], item['project_name'], item['deadline']))
            project_id = item['project_id']

            for emp in item['employees']:
                employee_id = emp['employee_id']
                data = emp['employee_id'], emp['name'], emp['position']
                category_id = get_or_create_employee(data, cursor)
                cursor.execute("INSERT INTO Project_Employee (project_id, employee_id) VALUES (%s, %s)", (project_id, employee_id))
        connection.commit()


parse_json(json_data_location)


connection.close()


print("Data inserted successfully.")