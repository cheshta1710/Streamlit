import streamlit as st
import speech_recognition as sr
import pyttsx3

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening... Speak a number between 0 and 100")
        audio = recognizer.listen(source)
        try:
            value = recognizer.recognize_google(audio)
            return int(value)
        except:
            return None

def calculate_grade(marks):
    total = sum(marks)
    percentage = total / len(marks)
    if percentage >= 90:
        grade = "A+"
    elif percentage >= 80:
        grade = "A"
    elif percentage >= 70:
        grade = "B"
    elif percentage >= 60:
        grade = "C"
    else:
        grade = "D"
    return total, percentage, grade

st.title("🎓 Student Grade Calculator")

name = st.text_input("Enter Student Name")

marks = []

for i in range(3):
    col1, col2 = st.columns([2, 1])
    with col1:
        mark = st.number_input(f"Enter marks for Subject {i+1}", min_value=0, max_value=100, key=f"mark_{i}")
    with col2:
        if st.button(f"🎤 Speak Subject {i+1}", key=f"voice_{i}"):
            voice_mark = get_voice_input()
            if voice_mark is not None and 0 <= voice_mark <= 100:
                st.success(f"Voice Input: {voice_mark}")
            else:
                st.warning("Could not recognize a valid number.")
            st.rerun()
    marks.append(st.session_state.get(f"mark_{i}", 0))

if st.button("Calculate Grade"):
    total, percentage, grade = calculate_grade(marks)
    result = f"{name} scored {total} marks with {percentage:.2f}% and got grade {grade}"
    st.success(result)
    speak(result)
