from flask import Flask, render_template, request
import boto3
from boto3.dynamodb.conditions import Key, Attr

app = Flask(__name__)

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-west-1')  # 'us-west-1' is our AWS region
attendance_table = dynamodb.Table('AttendanceRecords')  # 'AttendanceRecords' = our DB

@app.route('/', methods=['GET', 'POST'])
def show_attendance():
    date = request.form.get('date')
    student_name = request.form.get('student_name')
    class_section = request.form.get('class_section')

    filter_expression = None
    if date:
        filter_expression = Attr('date').eq(date)
    if student_name:
        if filter_expression:
            filter_expression &= Attr('student_name').eq(student_name)
        else:
            filter_expression = Attr('student_name').eq(student_name)
    if class_section:
        if filter_expression:
            filter_expression &= Attr('class_section').eq(class_section)
        else:
            filter_expression = Attr('class_section').eq(class_section)

    try:
        if filter_expression:
            response = attendance_table.scan(FilterExpression=filter_expression)
        else:
            response = attendance_table.scan()
        attendance_data = response.get('Items', [])
    except Exception as e:
        print(f"Error scanning DynamoDB: {e}")
        attendance_data = []

    return render_template('attendance.html', attendance_data=attendance_data)

if __name__ == '__main__':
    app.run(debug=True)

