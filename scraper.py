from flask import Flask, jsonify

from dataFetchFunctions import CAMarksWebScrapper
from dataExceptions import InvalidUsernameOrPasswordException, ScrappingError, NoSemResultsAvailable, NoCAMarksAvailable, AttendanceUpdateInProcessException, NoTimeTableDataException


def convert_ca_marks_to_dict(ca_marks):
    return [
        {
            "courseCode": mark.courseCode,
            "courseTitle": mark.courseTitle,
            "ca1": mark.ca1,
            "ca2": mark.ca2,
            "ca3": mark.ca3,
            "bestOfCA": mark.bestOfCA,
            "at1": mark.at1,
            "at2": mark.at2,
            "ap": mark.ap,
            "total": mark.total,
        }
        for mark in ca_marks
    ]




app = Flask(__name__)

@app.route('/marks/<username>/<password>')
def get_marks(username,password):
    try:
        awc = CAMarksWebScrapper(user_name=username, password=password)
        ca1,ca2=awc.fetch_ca_marks()
        ca1_dict = convert_ca_marks_to_dict(ca1)
        ca2_dict = convert_ca_marks_to_dict(ca2)
        
        return jsonify({"status": "success", "ca_marks_1": ca1_dict, "ca_marks_2": ca2_dict})
    except InvalidUsernameOrPasswordException as e:
        return jsonify({"message":e.message}),401
    except ScrappingError as e:
        return jsonify({"message":e.message}),500
    except NoCAMarksAvailable as e:
        return jsonify({"message":e.message}),404
    
@app.route('/attendance/<username>/<password>')
def get_attendance(username,password):
    try:
        awc = CAMarksWebScrapper(user_name=username, password=password)
        return jsonify(awc.fetch_attendance())
    except InvalidUsernameOrPasswordException as e:
        return jsonify({"message":e.message}),401
    except ScrappingError as e:
        return jsonify({"message":e.message}),500
    except AttendanceUpdateInProcessException as e:
        return jsonify({"message":e.message}),202
    
@app.route('/timetable/<username>/<password>')
def get_timetable(username,password):
    try:
        awc = CAMarksWebScrapper(user_name=username, password=password)
        return jsonify(awc.fetch_time_table())
    except InvalidUsernameOrPasswordException as e:
        return jsonify({"message":e.message}),401
    except ScrappingError as e:
        return jsonify({"message":e.message}),500
    except NoTimeTableDataException as e:
        return jsonify({"message":e.message}),404
    

if __name__ == "__main__":
    app.run(debug=True)
