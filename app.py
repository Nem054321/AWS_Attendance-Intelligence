from flask import Flask, render_template, request
import boto3

app = Flask(__name__)

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-west-1')  #'us-west-1' is our AWS region
attendance_table = dynamodb.Table('AttendanceRecords')  #'AttendanceRecords' = our DB 

@app.route('/', methods=['GET', 'POST'])
def show_attendance():
    date = request.form.get('date')
    student_name = request.form.get('student_name')
    class_section = request.form.get('class_section')

    filters = {}
    if date:
        filters['date'] = {'AttributeValueList': [date], 'ComparisonOperator': 'EQ'}
    if student_name:
        filters['student_name'] = {'AttributeValueList': [student_name], 'ComparisonOperator': 'EQ'}
    if class_section:
        filters['class_section'] = {'AttributeValueList': [class_section], 'ComparisonOperator': 'EQ'}

    if filters:
        response = attendance_table.scan(ScanFilter=filters)
    else:
        response = attendance_table.scan()

    attendance_data = response.get('Items', [])
    return render_template('attendance.html', attendance_data=attendance_data)

if __name__ == '__main__':
    app.run(debug=True)

