import streamlit as st
import json
from pathlib import Path

# -------------------------
# Page Configuration
# -------------------------
st.set_page_config(
    page_title="School Management System",
    page_icon="🏫",
    layout="wide"
)

# -------------------------
# Custom CSS
# -------------------------
st.markdown("""
<style>

.main {
    background-color: #f5f7fb;
}

.title {
    font-size:40px;
    font-weight:bold;
    color:#2E86C1;
}

.card {
    padding:20px;
    border-radius:15px;
    background:white;
    box-shadow:0px 5px 20px rgba(0,0,0,0.08);
}

.stButton>button{
    width:100%;
    border-radius:10px;
    height:3em;
    background:#2E86C1;
    color:white;
    font-weight:bold;
}

.stButton>button:hover{
    background:#1B4F72;
    color:white;
}

</style>
""", unsafe_allow_html=True)

DATABASE = "school_data.json"

# -------------------------
# Load Database
# -------------------------
data = {
    "Students": [],
    "Faculty": []
}

if Path(DATABASE).exists():
    with open(DATABASE, "r") as f:
        content = f.read()
        if content:
            data = json.loads(content)

def save():
    with open(DATABASE, "w") as f:
        json.dump(data, f, indent=4)

def validate_email(email):
    return "@" in email and "." in email

# -------------------------
# Sidebar
# -------------------------
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135755.png", width=100)
st.sidebar.title("🏫 School Management")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Register Student",
        "Register Faculty",
        "Add Student Grades",
        "Student Details",
        "Faculty Details"
    ]
)

# -------------------------
# Dashboard
# -------------------------
if menu == "Dashboard":

    st.markdown("<p class='title'>🏫 School Management Dashboard</p>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    c1.metric("👨‍🎓 Students", len(data["Students"]))
    c2.metric("👩‍🏫 Faculty", len(data["Faculty"]))

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("Students")

        if data["Students"]:
            st.dataframe(data["Students"], use_container_width=True)
        else:
            st.info("No students registered.")

    with right:
        st.subheader("Faculty")

        if data["Faculty"]:
            st.dataframe(data["Faculty"], use_container_width=True)
        else:
            st.info("No faculty registered.")

# -------------------------
# Register Student
# -------------------------
elif menu == "Register Student":

    st.header("👨‍🎓 Register Student")

    with st.form("student"):

        name = st.text_input("Student Name")
        age = st.number_input("Age", 1, 100)
        email = st.text_input("Email")
        roll = st.text_input("Roll Number")

        submit = st.form_submit_button("Register Student")

    if submit:

        if not validate_email(email):
            st.error("Invalid Email")

        elif any(i["roll_no"] == roll for i in data["Students"]):
            st.error("Roll Number already exists!")

        else:

            data["Students"].append({
                "name": name,
                "age": age,
                "email": email,
                "roll_no": roll,
                "grades": {}
            })

            save()

            st.success("Student Registered Successfully!")

# -------------------------
# Register Faculty
# -------------------------
elif menu == "Register Faculty":

    st.header("👩‍🏫 Register Faculty")

    with st.form("faculty"):

        name = st.text_input("Faculty Name")
        age = st.number_input("Age", 1, 100)
        email = st.text_input("Email")
        fid = st.text_input("Faculty ID")
        subject = st.text_input("Subject")

        submit = st.form_submit_button("Register Faculty")

    if submit:

        if not validate_email(email):
            st.error("Invalid Email")

        elif any(i["ID"] == fid for i in data["Faculty"]):
            st.error("Faculty ID already exists!")

        else:

            data["Faculty"].append({
                "name": name,
                "age": age,
                "email": email,
                "ID": fid,
                "Subject": subject
            })

            save()

            st.success("Faculty Registered Successfully!")

# -------------------------
# Add Grades
# -------------------------
elif menu == "Add Student Grades":

    st.header("📚 Add Student Grades")

    roll = st.text_input("Roll Number")
    subject = st.text_input("Subject")
    marks = st.number_input("Marks", 0.0, 100.0)

    if st.button("Add Grade"):

        found = False

        for s in data["Students"]:
            if s["roll_no"] == roll:
                s["grades"][subject] = marks
                found = True
                break

        if found:
            save()
            st.success("Marks Added Successfully")
        else:
            st.error("Student Not Found")

# -------------------------
# Student Details
# -------------------------
elif menu == "Student Details":

    st.header("👨‍🎓 Student Details")

    roll = st.text_input("Enter Roll Number")

    if st.button("Search Student"):

        found = False

        for s in data["Students"]:

            if s["roll_no"] == roll:

                found = True

                grades = s["grades"]

                avg = sum(grades.values()) / len(grades) if grades else 0

                st.success("Student Found")

                c1, c2 = st.columns(2)

                c1.write("### Name")
                c1.info(s["name"])

                c2.write("### Roll No")
                c2.info(s["roll_no"])

                st.write("### Email")
                st.info(s["email"])

                st.write("### Grades")

                if grades:
                    st.table(grades)
                else:
                    st.warning("No grades available")

                st.metric("Average", f"{avg:.2f}%")

        if not found:
            st.error("Student Not Found")

# -------------------------
# Faculty Details
# -------------------------
elif menu == "Faculty Details":

    st.header("👩‍🏫 Faculty Details")

    fid = st.text_input("Faculty ID")

    if st.button("Search Faculty"):

        found = False

        for f in data["Faculty"]:

            if f["ID"] == fid:

                found = True

                st.success("Faculty Found")

                c1, c2 = st.columns(2)

                c1.metric("Name", f["name"])
                c2.metric("ID", f["ID"])

                st.write("### Subject")
                st.info(f["Subject"])

                st.write("### Age")
                st.info(f["age"])

                st.write("### Email")
                st.info(f["email"])

        if not found:
            st.error("Faculty Not Found")