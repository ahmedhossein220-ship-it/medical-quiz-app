import streamlit as st
import json
import random

st.set_page_config(
    page_title="MCQ Quiz Master",
    layout="centered"
)

# ==========================
# CUSTOM STYLE
# ==========================

st.markdown("""
<style>
div[role="radiogroup"] label {
    font-size: 19px !important;
}

div[data-testid="stMarkdownContainer"] p {
    font-size: 17px;
}
</style>
""", unsafe_allow_html=True)

# ==========================
# SUBJECTS & QUIZZES
# ==========================

SUBJECTS = {

    "Physiology": {

        "CVS": "quizzes/questions.json",
        "Blood": "quizzes/blood.json",
        "Respiration": "quizzes/respa.json",
        "Practical": "quizzes/practical.json",
        "Autonomic": "quizzes/autonomic.json",
        "Nerve & Muscle": "quizzes/nervemuscle.json",
    },

    "Anatomy": {

        "Embryology": "quizzes/embryo.json",
        "Upper Limb": "quizzes/upperlimb.json",
        "Lower Limb": "quizzes/lowerlimb.json",
    },
    
    "Histology": {

        "Intro Cytology": "quizzes/IntroCytology.json",
        "Epithelium": "quizzes/histoEpithelium.json",
        "Cartilage & Bone": "quizzes/histoCartilageBone.json",
        "Blood": "quizzes/histoBlood.json",
        "Vascular": "quizzes/histoVascular.json",
        "Muscle": "quizzes/histoMuscle.json",
        "Nervous": "quizzes/histoNervous.json",
        "Respiratory": "quizzes/histoRespiratory.json",
        "Lymphoid": "quizzes/histoLymphoid.json",
    }
}


def load_questions(file_path):

    with open(file_path, "r", encoding="utf-8") as f:
        questions = json.load(f)

    random.shuffle(questions)

    return questions


st.title("📚 MCQ Quiz Master")

# ==========================
# INITIALIZE STATE
# ==========================

defaults = {
    "started": False,
    "show_feedback": False,
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value

# ==========================
# MENU
# ==========================

if not st.session_state.started:

    subject = st.selectbox(
        "Choose Subject",
        list(SUBJECTS.keys())
    )

    quiz_name = st.selectbox(
        "Choose Topic",
        list(SUBJECTS[subject].keys())
    )

    if st.button("Start Quiz"):

        questions = load_questions(
            SUBJECTS[subject][quiz_name]
        )

        st.session_state.started = True
        st.session_state.quiz_name = quiz_name
        st.session_state.questions = questions

        st.session_state.total_questions = len(questions)

        st.session_state.current_index = 0
        st.session_state.correct = 0
        st.session_state.streak = 0
        st.session_state.round_no = 1
        st.session_state.wrong_pool = []

        st.session_state.show_feedback = False

        st.rerun()

# ==========================
# QUIZ
# ==========================

else:

    questions = st.session_state.questions
    index = st.session_state.current_index
    total = len(questions)

    # --------------------------
    # END OF ROUND
    # --------------------------

    if index >= total:

        wrong_count = len(
            st.session_state.wrong_pool
        )

        if wrong_count > 0:

            st.success(
                f"Round {st.session_state.round_no} completed!"
            )

            st.warning(
                f"{wrong_count} incorrect questions will be repeated."
            )

            if st.button("Start Next Round"):

                random.shuffle(
                    st.session_state.wrong_pool
                )

                st.session_state.questions = (
                    st.session_state.wrong_pool.copy()
                )

                st.session_state.current_index = 0
                st.session_state.wrong_pool = []
                st.session_state.round_no += 1
                st.session_state.show_feedback = False

                st.rerun()

        else:

            percent = round(
                (
                    st.session_state.correct
                    / st.session_state.total_questions
                ) * 100,
                1
            )

            st.balloons()

            st.success(
                "🎉 Quiz Completed!"
            )

            st.write(
                f"✅ Correct Answers: {st.session_state.correct}"
            )

            st.write(
                f"📊 Success Rate: {percent}%"
            )

            st.write(
                f"🔄 Rounds Needed: {st.session_state.round_no}"
            )

            if st.button("Back To Menu"):

                st.session_state.clear()

                st.rerun()

        st.stop()

    # --------------------------
    # HEADER
    # --------------------------

    st.subheader(
        f"{st.session_state.quiz_name} | Round {st.session_state.round_no}"
    )

    st.write(
        f"🔥 Current Streak: {st.session_state.streak}"
    )

    st.progress(index / total)

    st.write(
        f"Question {index + 1} of {total}"
    )

    q = questions[index]

    # --------------------------
    # QUESTION
    # --------------------------

    st.markdown(
        f"### {q['q']}"
    )

    # --------------------------
    # FEEDBACK MODE
    # --------------------------

    if st.session_state.show_feedback:

        st.radio(
            "Answer",
            q["o"],
            index=st.session_state.selected_option_index,
            disabled=True,
            key=f"review_{index}"
        )

        if st.session_state.last_correct:

            st.success(
                "✅ Correct!"
            )

        else:

            st.error(
                "❌ Incorrect!"
            )

        st.markdown(
            f"""
**Your Answer:** {st.session_state.selected_letter}

**Correct Answer:** {st.session_state.correct_answer}
"""
        )

        if st.button(
            "Next Question"
        ):

            st.session_state.current_index += 1
            st.session_state.show_feedback = False

            st.rerun()

    # --------------------------
    # QUESTION MODE
    # --------------------------

    else:

        answer = st.radio(
            "Choose your answer:",
            q["o"],
            key=f"q_{index}"
        )

        if st.button(
            "Submit Answer"
        ):

            selected_letter = answer[0]
            correct_letter = q["a"]

            st.session_state.selected_letter = (
                selected_letter
            )

            st.session_state.correct_answer = (
                correct_letter
            )

            st.session_state.selected_option_index = (
                q["o"].index(answer)
            )

            if selected_letter == correct_letter:

                st.session_state.correct += 1
                st.session_state.streak += 1
                st.session_state.last_correct = True

            else:

                st.session_state.streak = 0
                st.session_state.last_correct = False

                st.session_state.wrong_pool.append(
                    q
                )

            st.session_state.show_feedback = True

            st.rerun()