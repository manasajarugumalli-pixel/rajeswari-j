import streamlit as st
import json
import os
from datetime import date

# -----------------------------
# Page settings
# -----------------------------
st.set_page_config(
    page_title="Student Attendance Tracker",
    page_icon="🎓",
    layout="wide"
)

# -----------------------------
# File names
# -----------------------------
STUDENT_FILE = "students.json"
ATTENDANCE_FILE = "attendance.json"


# -----------------------------
# Load JSON file
# -----------------------------
def load_data(filename):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            return json.load(file)
    return []


# -----------------------------
# Save JSON file
# -----------------------------
def save_data(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


# -----------------------------
# Load data
# -----------------------------
students = load_data(STUDENT_FILE)
attendance = load_data(ATTENDANCE_FILE)


# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>

.main {
    background-color: #f5f7fb;
}

.title {
    text-align: center;
    color: #2c3e50;
    font-size: 36px;
    font-weight: bold;
}

.subtitle {
    text-align: center;
    color: #555555;
    font-size: 18px;
}

.card {
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    background-color: white;
    border: 1px solid #dddddd;
}

.present {
    color: green;
    font-size: 30px;
    font-weight: bold;
}

.absent {
    color: red;
    font-size: 30px;
    font-weight: bold;
}

.percentage {
    color: #1565c0;
    font-size: 30px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------
# Title
# -----------------------------
st.markdown(
    '<div class="title">🎓 Student Attendance Tracker</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Manage students and track attendance easily</div>',
    unsafe_allow_html=True
)

st.write("")


# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("📚 Menu")

menu = st.sidebar.radio(
    "Select Option",
    [
        "Dashboard",
        "Add Student",
        "Mark Attendance",
        "View Attendance"
    ]
)


# =========================================================
# DASHBOARD
# =========================================================

if menu == "Dashboard":

    st.header("📊 Attendance Dashboard")

    total_students = len(students)

    present_count = 0
    absent_count = 0

    for record in attendance:

        if record["status"] == "Present":
            present_count += 1

        elif record["status"] == "Absent":
            absent_count += 1

    total_attendance = present_count + absent_count

    if total_attendance > 0:
        percentage = (present_count / total_attendance) * 100
    else:
        percentage = 0

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "👨‍🎓 Total Students",
            total_students
        )

    with col2:
        st.metric(
            "✅ Present",
            present_count
        )

    with col3:
        st.metric(
            "❌ Absent",
            absent_count
        )

    with col4:
        st.metric(
            "📊 Attendance %",
            f"{percentage:.2f}%"
        )

    st.write("")

    st.subheader("📈 Attendance Overview")

    st.write("✅ Present:", present_count)
    st.write("❌ Absent:", absent_count)
    st.write(
        "📊 Overall Attendance Percentage:",
        f"{percentage:.2f}%"
    )


# =========================================================
# ADD STUDENT
# =========================================================

elif menu == "Add Student":

    st.header("➕ Add Student")

    with st.form("student_form"):

        name = st.text_input("Student Name")

        roll_no = st.text_input("Roll Number")

        course = st.text_input("Course")

        submitted = st.form_submit_button("Add Student")

        if submitted:

            if name.strip() == "" or roll_no.strip() == "":
                st.error("Please enter student name and roll number.")

            else:

                # Check duplicate roll number
                exists = False

                for student in students:

                    if student["roll_no"] == roll_no:
                        exists = True
                        break

                if exists:

                    st.warning("Roll number already exists.")

                else:

                    new_student = {
                        "name": name,
                        "roll_no": roll_no,
                        "course": course
                    }

                    students.append(new_student)

                    save_data(
                        STUDENT_FILE,
                        students
                    )

                    st.success(
                        "Student added successfully! 🎉"
                    )


# =========================================================
# MARK ATTENDANCE
# =========================================================

elif menu == "Mark Attendance":

    st.header("📝 Mark Attendance")

    if len(students) == 0:

        st.warning(
            "No students found. Please add a student first."
        )

    else:

        student_names = []

        for student in students:
            student_names.append(
                student["name"]
                + " - "
                + student["roll_no"]
            )

        selected_student = st.selectbox(
            "Select Student",
            student_names
        )

        attendance_date = st.date_input(
            "Select Date",
            date.today()
        )

        status = st.selectbox(
            "Attendance Status",
            [
                "Present",
                "Absent"
            ]
        )

        if st.button("Save Attendance"):

            selected_roll = selected_student.split(" - ")[-1]

            new_record = {
                "roll_no": selected_roll,
                "date": str(attendance_date),
                "status": status
            }

            attendance.append(new_record)

            save_data(
                ATTENDANCE_FILE,
                attendance
            )

            st.success(
                "Attendance saved successfully! ✅"
            )


# =========================================================
# VIEW ATTENDANCE
# =========================================================

elif menu == "View Attendance":

    st.header("📋 Attendance Report")

    if len(students) == 0:

        st.warning("No students available.")

    else:

        for student in students:

            roll_no = student["roll_no"]

            present = 0
            absent = 0

            for record in attendance:

                if record["roll_no"] == roll_no:

                    if record["status"] == "Present":
                        present += 1

                    elif record["status"] == "Absent":
                        absent += 1

            total = present + absent

            if total > 0:
                percentage = (present / total) * 100
            else:
                percentage = 0

            st.subheader(
                "👨‍🎓 "
                + student["name"]
                + " ("
                + roll_no
                + ")"
            )

            st.write(
                "📚 Course:",
                student["course"]
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                st.write("✅ Present:", present)

            with col2:
                st.write("❌ Absent:", absent)

            with col3:
                st.write(
                    "📊 Attendance:",
                    f"{percentage:.2f}%"
                )

            st.divider()




          
