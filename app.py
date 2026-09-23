import streamlit as st
from utils.pdf_reader import extract_text_from_pdf
from tools.document_tool import StudyMaterialTool
from tools.memory_tool import StudentMemoryTool
from crew.study_crew import create_study_crew
from crew.tutor_crew import create_tutor_crew

st.set_page_config(page_title="StudyBuddy", page_icon=None, layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background:#f7f8fc; color:#172033; }
.block-container { max-width:1180px; padding:2rem 2.5rem 4rem; }
[data-testid="stSidebar"] { background:#ffffff; border-right:1px solid #e7e9f0; }
.brand { font-family:'Space Grotesk',sans-serif; font-size:25px; font-weight:700; letter-spacing:-.6px; margin-bottom:2rem; }
.brand span { color:#5b5ce2; }
.hero { background:linear-gradient(135deg,#ffffff 0%,#f1f2ff 100%); border:1px solid #e7e9f0; border-radius:24px; padding:34px; margin-bottom:22px; }
.hero h1 { font-family:'Space Grotesk',sans-serif; font-size:42px; letter-spacing:-1.5px; margin:0 0 10px; }
.hero p { color:#667085; font-size:17px; max-width:720px; line-height:1.6; }
.card { background:#fff; border:1px solid #e7e9f0; border-radius:18px; padding:22px; height:100%; box-shadow:0 5px 20px rgba(20,25,45,.03); }
.card h3 { font-family:'Space Grotesk',sans-serif; margin-top:0; }
.muted { color:#667085; }
.metric { font-family:'Space Grotesk',sans-serif; font-size:30px; font-weight:700; }
.stButton > button { border-radius:11px; min-height:44px; font-weight:600; border:1px solid #dfe2ea; }
.stButton > button[kind="primary"] { background:#5b5ce2; border-color:#5b5ce2; }
textarea, input { border-radius:11px !important; }
.section-title { font-family:'Space Grotesk',sans-serif; font-size:28px; font-weight:700; margin:10px 0 5px; }
.small-label { color:#667085; font-size:13px; font-weight:600; text-transform:uppercase; letter-spacing:.7px; }
div[data-testid="stFileUploader"] { background:#fff; border:1px dashed #cfd3df; border-radius:16px; padding:10px; }
</style>
""", unsafe_allow_html=True)

if "material" not in st.session_state: st.session_state.material = ""
if "study_pack" not in st.session_state: st.session_state.study_pack = ""
if "chat" not in st.session_state: st.session_state.chat = []
if "quiz" not in st.session_state: st.session_state.quiz = None
if "page" not in st.session_state: st.session_state.page = "Dashboard"
if "filename" not in st.session_state: st.session_state.filename = ""

def tools():
    doc = StudyMaterialTool()
    doc.material = st.session_state.material
    return doc, StudentMemoryTool()

with st.sidebar:
    st.markdown('<div class="brand">Study<span>Buddy</span></div>', unsafe_allow_html=True)
    for item in ["Dashboard", "Study Pack", "Tutor", "Quiz", "Learning Audit"]:
        if st.button(item, use_container_width=True, type="primary" if st.session_state.page == item else "secondary"):
            st.session_state.page = item
            st.rerun()
    st.markdown("---")
    st.markdown("**Your workspace**")
    if st.session_state.filename:
        st.caption(st.session_state.filename)
    else:
        st.caption("No material uploaded yet.")

if st.session_state.page == "Dashboard":
    st.markdown("""
    <div class="hero">
      <div class="small-label">Your personal study workspace</div>
      <h1>Study smarter, not longer.</h1>
      <p>Upload your lecture notes or PDF and StudyBuddy turns the material into a focused study plan, teaching notes, practice quiz, and learning audit.</p>
    </div>
    """, unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload your study material", type=["pdf"], label_visibility="visible")
    if uploaded:
        if st.session_state.filename != uploaded.name:
            text = extract_text_from_pdf(uploaded)
            st.session_state.material = text
            st.session_state.filename = uploaded.name
            st.session_state.study_pack = ""
            st.session_state.quiz = None
            st.session_state.chat = []
            st.success("Material loaded. Your study workspace is ready.")
    c1,c2,c3 = st.columns(3)
    with c1:
        st.markdown('<div class="card"><div class="small-label">01</div><h3>Understand</h3><p class="muted">Find the concepts that actually matter instead of producing another generic summary.</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="card"><div class="small-label">02</div><h3>Practice</h3><p class="muted">Learn with clear explanations and questions designed around your material.</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="card"><div class="small-label">03</div><h3>Improve</h3><p class="muted">Use your quiz performance to identify weak areas and decide what to study next.</p></div>', unsafe_allow_html=True)

elif st.session_state.page == "Study Pack":
    st.markdown('<div class="section-title">Your Study Pack</div><p class="muted">A structured roadmap built from your uploaded material.</p>', unsafe_allow_html=True)
    if not st.session_state.material:
        st.info("Upload a PDF from the Dashboard first.")
    else:
        if st.button("Build my study pack", type="primary"):
            doc, mem = tools()
            with st.spinner("StudyBuddy is structuring your material..."):
                st.session_state.study_pack = str(create_study_crew(doc, mem).kickoff())
        if st.session_state.study_pack:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(st.session_state.study_pack)
            st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "Tutor":
    st.markdown('<div class="section-title">Study with your tutor</div><p class="muted">Ask questions about the uploaded material.</p>', unsafe_allow_html=True)
    if not st.session_state.material:
        st.info("Upload a PDF from the Dashboard first.")
    else:
        for role, msg in st.session_state.chat:
            with st.chat_message(role):
                st.markdown(msg)
        question = st.chat_input("Ask something from your study material...")
        if question:
            st.session_state.chat.append(("user", question))
            doc, mem = tools()
            with st.spinner("Thinking..."):
                answer = str(create_tutor_crew(doc, mem, question).kickoff())
            st.session_state.chat.append(("assistant", answer))
            st.rerun()

elif st.session_state.page == "Quiz":
    st.markdown('<div class="section-title">Practice Quiz</div><p class="muted">Test whether you can apply what you studied.</p>', unsafe_allow_html=True)
    if not st.session_state.material:
        st.info("Upload a PDF from the Dashboard first.")
    else:
        if st.button("Generate 5-question quiz", type="primary"):
            doc, mem = tools()
            with st.spinner("Creating your quiz..."):
                st.session_state.quiz = str(create_study_crew(doc, mem).kickoff())
        if st.session_state.quiz:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(st.session_state.quiz)
            st.markdown('</div>', unsafe_allow_html=True)
            st.caption("For the MVP, the generated quiz is shown as a study worksheet. Interactive scoring can be added as the next module.")

elif st.session_state.page == "Learning Audit":
    st.markdown('<div class="section-title">Learning Audit</div><p class="muted">Turn practice results into your next study action.</p>', unsafe_allow_html=True)
    if not st.session_state.study_pack:
        st.info("Build your Study Pack first.")
    else:
        st.markdown('<div class="card"><h3>What to review next</h3><p class="muted">Use the quiz and tutor sessions to identify concepts you could not explain confidently. Focus your next session on those topics before moving forward.</p></div>', unsafe_allow_html=True)
