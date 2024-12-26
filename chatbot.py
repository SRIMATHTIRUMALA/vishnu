import streamlit as st
import pandas as pd
from datetime import datetime
import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from googletrans import Translator

# Initialize translator
translator = Translator()

# Sample data for students (username as name, password as roll number)
students = {
    "Pathan Rafi Khan": "24DSC01",
    "Landa Leela Krishna": "24DSC02",
    "Peruri Veera Satya Kanaka Teja": "24DSC03",
    "Muppidi Naga Kavita": "24DSC04",
    "Mundru Jyothiriya Sindhya": "24DSC05",
    "Pinnamaneni Navya Sai Sree": "24DSC06",
    "Penumallu Rama Tulasi": "24DSC07",
    "Mupparthi Suji Anantha Naga Lakshmi": "24DSC08",
    "Morla Neelima": "24DSC09",
    "Srimathtirumala Sai Vishnu": "24DSC10",
    "Nukala Pallavi Sai": "24DSC11",
    "Sidagam Sweety Swarupa": "24DSC12",
    "Poludasu Praveen": "24DSC13",
    "Seelam Revanth Sai Kumar": "24DSC14",
    "Peruri Prathyusha": "24DSC15",
    "Avula Kusuma Priya": "24DSC16",
    "Sankhavarapu Likhitha": "24DSC17",
    "Yanagandala Srinivas": "24DSC18",
    "Gajula Yamini Naga Sai Aishwarya": "24DSC19",
    "Gandham Mani Saketh": "24DSC20",
    "Kommu Sankeerthana": "24DSC21",
    "Mohammad Aman Shafiqua": "24DSC22",
    "Naraharisetti Sowmya Rani": "24DSC23",
    "Basamsetti Tanuja": "24DSC24",
    "Kanuganti Hima Bindu": "24DSC25",
    "Kandibanda Nithin Guptha": "24DSC26",
    "Gogulapati Bala Prasanna": "24DSC27",
    "Talasila Hema Sri": "24DSC28",
    "Chityala Vishnuvardhan Reddy": "24DSC29",
    "Dharmavarapu Mahalakshmi": "24DSC30",
    "Dasari Vijaya Nandini": "24DSC31",
    "Sreekakulapu Jones Daniel": "24DSC32",
    "Badarla Mounika": "24DSC33",
    "Edubilli Venkatesh": "24DSC34",
    "Kandula Vishnu": "24DSC35",
    "Dabbugottu Pranathi": "24DSC36"
}

# Faculty login (fixed username and password)
faculty_username = "faculty"
faculty_password = "faculty123"

# Initialize attendance CSV file
ATTENDANCE_FILE = "attendance.csv"
if not os.path.exists(ATTENDANCE_FILE):
    # If the file doesn't exist, create it with appropriate columns
    df = pd.DataFrame(columns=["Roll Number", "Name", "Date", "Attendance"])
    df.to_csv(ATTENDANCE_FILE, index=False)

# Create directory for uploaded PDFs if it doesn't exist
if not os.path.exists("uploaded_pdfs"):
    os.makedirs("uploaded_pdfs")

# Function to mark attendance
def mark_attendance(roll_number):
    if roll_number in students.values():
        # Get the student name associated with the roll number
        name = [name for name, roll in students.items() if roll == roll_number][0]
        date = datetime.now().strftime("%Y-%m-%d")
        df = pd.read_csv(ATTENDANCE_FILE)

        # Check if attendance already marked for the given date
        if any((df["Roll Number"] == roll_number) & (df["Date"] == date)):
            return f"Attendance for {name} on {date} has already been marked."
        else:
            # Add the attendance record
            new_row = {"Roll Number": roll_number, "Name": name, "Date": date, "Attendance": "Present"}
            df = df.append(new_row, ignore_index=True)
            df.to_csv(ATTENDANCE_FILE, index=False)  # Save back to CSV
            return f"Attendance marked for {name} on {date}"
    else:
        return "Invalid Roll Number"

# Function to check attendance
def check_attendance(roll_number):
    df = pd.read_csv(ATTENDANCE_FILE)
    records = df[df["Roll Number"] == roll_number]
    if not records.empty:
        return records
    return "No attendance records found."

# Function to handle questions dynamically
def handle_question(question, lang):
    question = question.lower()
    tokens = word_tokenize(question)
    tokens = [word for word in tokens if word.isalnum()]
    filtered_words = [word for word in tokens if word not in stopwords.words('english')]
   
    # Simple keyword matching for dynamic responses
    if "admission" in filtered_words or "timing" in filtered_words:
        return translate_text("Admission details are available on the college website.", lang)
    if "fee" in filtered_words or "structure" in filtered_words:
        return translate_text("the counciling seat total fee is 45,400  and for  management seat total fee is 50000", lang)
    if "examination" in filtered_words or "dates" in filtered_words:
        return translate_text("Examination dates will be posted on the college notice board.", lang)
    if "scholarships" in filtered_words or "apply" in filtered_words:
        return translate_text("Scholarship application details are available on the college website.", lang)
    if "course duration" in filtered_words or "years" in filtered_words:
        return translate_text("The course duration is 2 years.", lang)
    if "faculty" in filtered_words and "contact" in filtered_words:
        return translate_text("You can contact your faculty members via email or during their office hours.", lang)
    if "facilities" in filtered_words:
        return translate_text("The college offers a library, computer labs, sports facilities, and online resources.", lang)
    if "attendance policy" in filtered_words:
        return translate_text("Attendance is mandatory, and students must maintain at least 75% attendance to be eligible for exams.", lang)
    if "hostel" in filtered_words or "accommodation" in filtered_words:
        return translate_text("Yes, the college offers hostel facilities for both male and female students.", lang)
    if "holidays" in filtered_words or "vacations" in filtered_words:
        return translate_text("The list of college holidays will be posted on the academic calendar.", lang)
    if "grading system" in filtered_words:
        return translate_text("The grading system follows a CGPA system. Grades range from A+ to F, with corresponding points.", lang)
    return translate_text("Sorry, I don't have an answer for that question.", lang)

# Function to translate text
def translate_text(text, lang):
    try:
        if lang == "Telugu":
            return translator.translate(text, src='en', dest='te').text
        elif lang == "Hindi":
            return translator.translate(text, src='en', dest='hi').text
        return text
    except Exception as e:
        return f"Error in translation: {str(e)}"

# Streamlit Code for the App
st.title("PB Siddhartha College Chatbot")

# Language selection
language = st.sidebar.selectbox("Choose your language", ["English", "Telugu", "Hindi"])

# Login system
user_type = st.sidebar.selectbox("Who are you?", ["Student", "Faculty", "Parents"])

username = st.sidebar.text_input("Enter your username:")
password = st.sidebar.text_input("Enter your password:", type="password")
is_logged_in = st.sidebar.button("Login")

# Check for existing session
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_type = None
    st.session_state.username = None

if is_logged_in:
    if user_type == "Faculty" and username == faculty_username and password == faculty_password:
        st.session_state.logged_in = True
        st.session_state.user_type = "Faculty"
        st.session_state.username = username
    elif user_type == "Student" and username in students and password == students[username]:
        st.session_state.logged_in = True
        st.session_state.user_type = "Student"
        st.session_state.username = username
    elif user_type == "Parents":
        st.session_state.logged_in = True
        st.session_state.user_type = "Parents"
        st.session_state.username = username
    else:
        st.error("Invalid username or password!")

# If logged in, show the corresponding interface
if st.session_state.logged_in:
    if st.session_state.user_type == "Faculty":
        st.header(f"Welcome, {username}!")
        st.subheader("Faculty Options")
        if st.checkbox("Upload Study Material (PDF)"):

            uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
            if uploaded_file:
                # Save the uploaded file
                file_path = os.path.join("uploaded_pdfs", uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.read())
                st.success(f"{uploaded_file.name} uploaded successfully!")

        if st.checkbox("Check Student Attendance"):
            roll_number = st.text_input("Enter the Roll Number of the Student:")
            if st.button("Check Attendance"):
                result = check_attendance(roll_number)
                st.write(result)

    elif st.session_state.user_type == "Student":
        st.header(f"Welcome, {username}!")
        st.subheader("Student Options")
        if st.checkbox("Mark Attendance"):
            # Mark attendance for the logged-in student
            if st.button("Mark My Attendance"):
                roll_number = students[username]  # Use the roll number for the logged-in student
                result = mark_attendance(roll_number)
                st.write(result)

        if st.checkbox("View Uploaded Study Materials"):
            uploaded_files = os.listdir("uploaded_pdfs")
            if uploaded_files:
                for file in uploaded_files:
                    file_path = os.path.join("uploaded_pdfs", file)
                    with open(file_path, "rb") as pdf_file:
                        st.download_button(
                            label=f"Download {file}",
                            data=pdf_file,
                            file_name=file,
                            mime="application/pdf"
                        )
            else:
                st.write("No study materials available.")
               
        if st.checkbox("Check Attendance"):
            attendance_records = check_attendance(students[username])
            st.write(attendance_records)
   
    elif st.session_state.user_type == "Parents":
        st.header("Welcome, Parents!")
        # Parents options (ask questions about admissions, timings, etc.)
        question = st.text_input("Ask about admissions, timings, etc.:")
        if st.button("Submit"):
            if question:
                response = handle_question(question, language)
                st.write(response)
            else:
                st.write("Please ask a question.")
else:
    st.write("Please log in to access features.")
