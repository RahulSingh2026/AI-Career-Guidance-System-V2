import streamlit as st
import pandas as pd

from model import train_model

from database import (
    create_tables,
    register_student,
    login_student,
    get_student,
    save_assessment,
    get_assessment_history
)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Career Guide",
    page_icon="🎓",
    layout="wide"
)


# --------------------------------------------------
# DATABASE INITIALIZATION
# --------------------------------------------------

create_tables()


# --------------------------------------------------
# MACHINE LEARNING MODEL
# --------------------------------------------------

model = train_model()


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "student_id" not in st.session_state:
    st.session_state.student_id = None

if "student_name" not in st.session_state:
    st.session_state.student_name = None


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

.main-title {
    font-size: 38px;
    font-weight: 700;
}

.subtitle {
    font-size: 18px;
    color: #666666;
}

.card {
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #dddddd;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)


# ==================================================
# LOGIN / SIGNUP PAGE
# ==================================================

if not st.session_state.logged_in:

    st.title("🎓 AI Career Guide")

    st.write(
        "AI-Based Career Guidance and Recommendation System"
    )

    st.write(
        "Create your account and discover careers based on your skills."
    )

    st.divider()

    login_tab, signup_tab = st.tabs(
        ["🔐 Login", "📝 Create Account"]
    )

    # --------------------------------------------------
    # LOGIN
    # --------------------------------------------------

    with login_tab:

        st.subheader("Welcome Back!")

        email = st.text_input(
            "Email",
            key="login_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button(
            "Login",
            type="primary",
            use_container_width=True
        ):

            if not email or not password:

                st.warning(
                    "Please enter email and password."
                )

            else:

                student = login_student(
                    email,
                    password
                )

                if student:

                    st.session_state.logged_in = True
                    st.session_state.student_id = student[0]
                    st.session_state.student_name = student[1]

                    st.success(
                        "Login successful!"
                    )

                    st.rerun()

                else:

                    st.error(
                        "Invalid email or password."
                    )

    # --------------------------------------------------
    # SIGNUP
    # --------------------------------------------------

    with signup_tab:

        st.subheader("Create Your Account")

        name = st.text_input(
            "Full Name",
            key="signup_name"
        )

        email = st.text_input(
            "Email Address",
            key="signup_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="signup_password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            key="confirm_password"
        )

        college = st.text_input(
            "College Name",
            key="signup_college"
        )

        course = st.selectbox(
            "Course",
            [
                "BCA",
                "B.Tech",
                "MCA",
                "M.Tech",
                "B.Sc",
                "Other"
            ]
        )

        year = st.selectbox(
            "Year",
            [
                "1st Year",
                "2nd Year",
                "3rd Year",
                "4th Year",
                "Other"
            ]
        )

        if st.button(
            "Create Account",
            type="primary",
            use_container_width=True
        ):

            if not name or not email or not password:

                st.warning(
                    "Please fill all required fields."
                )

            elif password != confirm_password:

                st.error(
                    "Passwords do not match."
                )

            elif len(password) < 6:

                st.error(
                    "Password must contain at least 6 characters."
                )

            else:

                success, message = register_student(
                    name,
                    email,
                    password,
                    college,
                    course,
                    year
                )

                if success:

                    st.success(message)

                    st.info(
                        "Now go to the Login tab and login."
                    )

                else:

                    st.error(message)


# ==================================================
# MAIN APPLICATION
# ==================================================

else:

    # --------------------------------------------------
    # GET CURRENT STUDENT
    # --------------------------------------------------

    student = get_student(
        st.session_state.student_id
    )

    if student is None:

        st.session_state.logged_in = False
        st.rerun()


    # --------------------------------------------------
    # SIDEBAR
    # --------------------------------------------------

    with st.sidebar:

        st.title("🎓 AI Career Guide")

        st.write(
            f"Hello, **{student[1]}!** 👋"
        )

        st.divider()

        page = st.radio(
            "Navigation",
            [
                "🏠 Dashboard",
                "👤 My Profile",
                "🎯 Career Assessment",
                "📊 Career Results",
                "📚 Learning Roadmap",
                "📜 Assessment History"
            ]
        )

        st.divider()

        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):

            st.session_state.logged_in = False
            st.session_state.student_id = None
            st.session_state.student_name = None

            st.rerun()


    # ==================================================
    # DASHBOARD
    # ==================================================

    if page == "🏠 Dashboard":

        st.markdown(
            '<div class="main-title">AI Career Dashboard</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="subtitle">Welcome back, {student[1]}! '
            'Your personalized career guidance starts here.</div>',
            unsafe_allow_html=True
        )

        st.divider()

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "🎓 Course",
                student[4]
            )

        with col2:

            st.metric(
                "📅 Year",
                student[5]
            )

        with col3:

            history = get_assessment_history(
                st.session_state.student_id
            )

            st.metric(
                "📊 Assessments",
                len(history)
            )

        st.divider()

        st.subheader("🚀 What can you do?")

        col1, col2 = st.columns(2)

        with col1:

            st.info(
                """
                ### 🎯 Career Assessment

                Enter your skills and interests to
                get a personalized career recommendation.
                """
            )

        with col2:

            st.info(
                """
                ### 📚 Learning Roadmap

                Get a step-by-step roadmap and
                skills to learn for your career.
                """
            )

        st.subheader("🤖 How the system works")

        st.write(
            "Student Skills → Machine Learning → "
            "Career Prediction → Skill Analysis → "
            "Learning Roadmap"
        )


    # ==================================================
    # PROFILE
    # ==================================================

    elif page == "👤 My Profile":

        st.title("👤 My Profile")

        st.subheader("Student Information")

        col1, col2 = st.columns(2)

        with col1:

            st.write("**Name:**", student[1])
            st.write("**Email:**", student[2])
            st.write("**College:**", student[3])

        with col2:

            st.write("**Course:**", student[4])
            st.write("**Year:**", student[5])


    # ==================================================
    # CAREER ASSESSMENT
    # ==================================================

    elif page == "🎯 Career Assessment":

        st.title("🎯 Career Assessment")

        st.write(
            "Rate your current skills from 1 to 10."
        )

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            python = st.slider(
                "🐍 Python Skill",
                1,
                10,
                5
            )

            mathematics = st.slider(
                "📐 Mathematics Skill",
                1,
                10,
                5
            )

            data_analysis = st.slider(
                "📊 Data Analysis Skill",
                1,
                10,
                5
            )

        with col2:

            communication = st.slider(
                "💬 Communication Skill",
                1,
                10,
                5
            )

            problem_solving = st.slider(
                "🧠 Problem Solving Skill",
                1,
                10,
                5
            )

            web_development = st.slider(
                "🌐 Web Development Skill",
                1,
                10,
                5
            )

        st.divider()

        interest = st.selectbox(
            "🎯 Select your main career interest",
            [
                "Data Science",
                "Software Development",
                "Web Development",
                "Artificial Intelligence",
                "Cyber Security"
            ]
        )

        st.divider()

        if st.button(
            "🤖 Analyze My Career",
            type="primary",
            use_container_width=True
        ):

            # ------------------------------------------
            # RULE BASED SCORES
            # ------------------------------------------

            data_science_score = (
                python
                + mathematics
                + problem_solving
                + data_analysis
            )

            software_score = (
                python
                + problem_solving
                + communication
            )

            web_score = (
                web_development
                + python
                + communication
            )

            ai_score = (
                python
                + mathematics
                + problem_solving
                + data_analysis
            )

            cyber_score = (
                python
                + problem_solving
                + mathematics
            )

            data_science_percentage = (
                data_science_score / 40
            ) * 100

            software_percentage = (
                software_score / 30
            ) * 100

            web_percentage = (
                web_score / 30
            ) * 100

            ai_percentage = (
                ai_score / 40
            ) * 100

            cyber_percentage = (
                cyber_score / 30
            ) * 100

            career_scores = {

                "Data Scientist":
                    data_science_percentage,

                "Software Developer":
                    software_percentage,

                "Web Developer":
                    web_percentage,

                "AI/ML Engineer":
                    ai_percentage,

                "Cyber Security Analyst":
                    cyber_percentage
            }

            best_career = max(
                career_scores,
                key=career_scores.get
            )

            best_score = career_scores[
                best_career
            ]

            # ------------------------------------------
            # ML PREDICTION
            # ------------------------------------------

            student_data = pd.DataFrame(
                [[
                    python,
                    mathematics,
                    data_analysis,
                    communication,
                    web_development
                ]],
                columns=[
                    "Python",
                    "Mathematics",
                    "Data_Analysis",
                    "Communication",
                    "Web_Development"
                ]
            )

            prediction = model.predict(
                student_data
            )

            ml_prediction = prediction[0]

            probabilities = model.predict_proba(
                student_data
            )

            confidence = (
                probabilities.max() * 100
            )

            # ------------------------------------------
            # SAVE ASSESSMENT
            # ------------------------------------------

            save_assessment(

                st.session_state.student_id,

                python,
                mathematics,
                data_analysis,
                communication,
                problem_solving,
                web_development,

                interest,

                best_career,
                best_score,

                ml_prediction
            )

            # ------------------------------------------
            # SAVE RESULT IN SESSION
            # ------------------------------------------

            st.session_state.last_career = best_career
            st.session_state.last_score = best_score
            st.session_state.last_prediction = ml_prediction
            st.session_state.last_confidence = confidence

            st.success(
                "Your career assessment has been completed!"
            )

            st.divider()

            st.subheader(
                "🎯 Career Recommendation"
            )

            st.success(
                f"Recommended Career: {best_career}"
            )

            st.info(
                f"Skill Match Score: {best_score:.1f}%"
            )

            st.subheader(
                "🤖 AI/ML Prediction"
            )

            st.success(
                f"AI/ML Predicted Career: {ml_prediction}"
            )

            st.info(
                f"Decision Tree Model Confidence: "
                f"{confidence:.1f}%"
            )

            st.caption(
                "Note: This confidence is based on the "
                "current small training dataset and should "
                "not be treated as real-world certainty."
            )


    # ==================================================
    # CAREER RESULTS
    # ==================================================

    elif page == "📊 Career Results":

        st.title("📊 Career Results")

        if "last_career" not in st.session_state:

            st.info(
                "Please complete a Career Assessment first."
            )

        else:

            career = st.session_state.last_career
            score = st.session_state.last_score
            prediction = st.session_state.last_prediction
            confidence = st.session_state.last_confidence

            st.subheader(
                "🎯 Recommended Career"
            )

            st.success(
                career
            )

            st.metric(
                "Career Match Score",
                f"{score:.1f}%"
            )

            st.divider()

            st.subheader(
                "🤖 Machine Learning Result"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.info(
                    f"ML Prediction\n\n{prediction}"
                )

            with col2:

                st.info(
                    f"Model Confidence\n\n{confidence:.1f}%"
                )

            st.caption(
                "The ML result is based on the Decision Tree "
                "trained on the project's sample dataset."
            )


    # ==================================================
    # LEARNING ROADMAP
    # ==================================================

    elif page == "📚 Learning Roadmap":

        st.title("📚 Learning Roadmap")

        if "last_prediction" not in st.session_state:

            st.info(
                "Please complete a Career Assessment first."
            )

        else:

            predicted_career = (
                st.session_state.last_prediction
            )

            learning_skills = {

                "Data Scientist": [
                    "Python",
                    "Statistics",
                    "SQL",
                    "Pandas",
                    "Machine Learning"
                ],

                "Software Developer": [
                    "Programming",
                    "Data Structures",
                    "Algorithms",
                    "Git",
                    "Problem Solving"
                ],

                "Web Developer": [
                    "HTML",
                    "CSS",
                    "JavaScript",
                    "React",
                    "Web Design"
                ],

                "AI/ML Engineer": [
                    "Python",
                    "Mathematics",
                    "Machine Learning",
                    "Deep Learning",
                    "TensorFlow / PyTorch"
                ],

                "Cyber Security Analyst": [
                    "Computer Networking",
                    "Linux",
                    "Cyber Security Fundamentals",
                    "Ethical Hacking",
                    "Security Tools"
                ]
            }

            learning_path = {

                "Data Scientist": [
                    "Learn Python",
                    "Learn Statistics",
                    "Learn SQL",
                    "Learn Pandas and NumPy",
                    "Learn Machine Learning",
                    "Build Data Science Projects"
                ],

                "Software Developer": [
                    "Learn Programming",
                    "Learn Data Structures",
                    "Learn Algorithms",
                    "Learn Git and GitHub",
                    "Practice Problem Solving",
                    "Build Software Projects"
                ],

                "Web Developer": [
                    "Learn HTML",
                    "Learn CSS",
                    "Learn JavaScript",
                    "Learn React",
                    "Learn Web Development Tools",
                    "Build Web Projects"
                ],

                "AI/ML Engineer": [
                    "Learn Python",
                    "Learn Mathematics",
                    "Learn Machine Learning",
                    "Learn Deep Learning",
                    "Learn TensorFlow or PyTorch",
                    "Build AI Projects"
                ],

                "Cyber Security Analyst": [
                    "Learn Computer Networking",
                    "Learn Linux",
                    "Learn Cyber Security Fundamentals",
                    "Learn Ethical Hacking",
                    "Practice Security Tools",
                    "Build Cyber Security Projects"
                ]
            }

            st.subheader(
                f"🎯 Roadmap for {predicted_career}"
            )

            st.write(
                "### 📖 Skills to Learn"
            )

            for skill in learning_skills[
                predicted_career
            ]:

                st.write(
                    "✅",
                    skill
                )

            st.divider()

            st.write(
                "### 🛣️ Your Learning Path"
            )

            for i, step in enumerate(
                learning_path[predicted_career],
                start=1
            ):

                st.write(
                    f"**Step {i}:** {step}"
                )


    # ==================================================
    # ASSESSMENT HISTORY
    # ==================================================

    elif page == "📜 Assessment History":

        st.title("📜 Assessment History")

        history = get_assessment_history(
            st.session_state.student_id
        )

        if not history:

            st.info(
                "You have not completed any assessment yet."
            )

        else:

            st.write(
                "Your previous career assessments:"
            )

            for index, item in enumerate(
                history,
                start=1
            ):

                interest = item[0]
                recommended = item[1]
                score = item[2]
                ml_prediction = item[3]

                with st.expander(
                    f"Assessment {index}"
                ):

                    st.write(
                        "**Interest:**",
                        interest
                    )

                    st.write(
                        "**Recommended Career:**",
                        recommended
                    )

                    st.write(
                        "**Match Score:**",
                        f"{score:.1f}%"
                    )

                    st.write(
                        "**ML Prediction:**",
                        ml_prediction
                    )