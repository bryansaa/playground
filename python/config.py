#! /usr/bin/env python
from dotenv import load_dotenv
import os

WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(WORKING_DIR, '.env'))

# Put your name here
NAME = "Amelia"
DESC = "This is a simple web app. It showcases some functions with Python Flask. It is built with Flask and " \
       "Bootstrap CSS"
SECRET_KEY = os.getenv('SECRET_KEY')
DB_FILE_NAME = 'data.json'
DB_FILE_FULL_PATH = os.path.join(WORKING_DIR, DB_FILE_NAME)

@app.route('/birthday', methods=['GET', 'POST'])
def birthday():
    from datetime import datetime
    celebrate = False
    message = ""

    # Month name mapping and big-month list already exist earlier in code
    month_map = {
        1: "January", 2: "February", 3: "March", 4: "April",
        5: "May", 6: "June", 7: "July", 8: "August",
        9: "September", 10: "October", 11: "November", 12: "December"
    }
    big_month = [1, 3, 5, 7, 8, 10, 12]

    if request.method == 'POST':
        name = request.form.get('name')
        month = request.form.get('month')
        day = request.form.get('day')

        # Validate numeric input
        try:
            month = int(month)
            day = int(day)
        except:
            flash("Invalid month or day", "error")
            return render_template('birthday.html')

        # Validate month range
        if month < 1 or month > 12:
            flash("Invalid month or day", "error")
            return render_template('birthday.html')

        # Validate days in each month
        if month in big_month:
            max_day = 31
        elif month == 2:
            max_day = 29
        else:
            max_day = 30

        if day < 1 or day > max_day:
            flash("Invalid month or day", "error")
            return render_template('birthday.html')

        # Today's date
        today = datetime.now()
        current_year = today.year
        today_doy = today.timetuple().tm_yday

        # Build birthday date for this year
        try:
            birthday_this_year = datetime(current_year, month, day)
        except:
            flash("Invalid date", "error")
            return render_template('birthday.html')

        birthday_doy = birthday_this_year.timetuple().tm_yday

        # Case 1 — Birthday is today
        if birthday_doy == today_doy:
            celebrate = True
            message = (
                f"Dear {name}, your birthday in {current_year} is on "
                f"{month_map[month]} {day}, which is TODAY! HAPPY BIRTHDAY!"
            )
            return render_template('birthday.html', message=message, celebrate=celebrate)

        # Case 2 — Future birthday
        if birthday_doy > today_doy:
            days_until = birthday_doy - today_doy
            message = (
                f"Dear {name}, your birthday in {current_year} is on "
                f"{month_map[month]} {day}, and there are {days_until} days "
                f"until your birthday!"
            )
            return render_template('birthday.html', message=message)

        # Case 3 — Birthday already passed this year
        if birthday_doy < today_doy:
            days_since = today_doy - birthday_doy
            message = (
                f"Dear {name}, your birthday in {current_year} is on "
                f"{month_map[month]} {day}, and {days_since} days have passed "
                f"since your birthday."
            )
            return render_template('birthday.html', message=message)

    return render_template('birthday.html')
