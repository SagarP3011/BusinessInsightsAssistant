import streamlit as st
from backend.query_engine import QueryEngine
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

engine = QueryEngine()

if "query_history" not in st.session_state:
    st.session_state["query_history"] = []
if "responses" not in st.session_state:
    st.session_state["responses"] = {}


st.title(" Business Insight Assistant")
st.subheader("Ask any business-related question and get AI-powered insights!")


if st.session_state["query_history"]:
    selected_query = st.selectbox(" View Past Queries:", st.session_state["query_history"], index=None, placeholder="Select to view...")
    if selected_query:
        st.write(" Previous Insight:")
        st.write(st.session_state["responses"][selected_query])


user_query = st.text_area(" Enter your business question:", "")

if st.button(" Generate Insights"):
    if user_query.strip():
        with st.spinner(" Generating insights..."):
            response = engine.generate_gemini_response(user_query)
        st.success(" Insights Generated!")

       
        st.session_state["query_history"].append(user_query)
        st.session_state["responses"][user_query] = response

        
        st.write(response)
    else:
        st.warning(" Please enter a question.")

def create_pdf(response_text):
    pdf_buffer = BytesIO()
    pdf_canvas = canvas.Canvas(pdf_buffer, pagesize=letter)
    pdf_canvas.setFont("Helvetica", 12)

  
    text_lines = response_text.split("\n")
    y_position = 750 
    for line in text_lines:
        pdf_canvas.drawString(50, y_position, line)
        y_position -= 20  
        if y_position < 50: 
            pdf_canvas.showPage()
            y_position = 750

    pdf_canvas.save()
    pdf_buffer.seek(0)
    return pdf_buffer


if st.session_state["query_history"]:
    selected_download_query = st.selectbox(" Select a Query to Download:", st.session_state["query_history"], index=None, placeholder="Select...")
    if selected_download_query:
        pdf_file = create_pdf(st.session_state["responses"][selected_download_query])
        st.download_button(
            label=" Download Insights as PDF",
            data=pdf_file,
            file_name=f"{selected_download_query.replace(' ', '_')}_insights.pdf",
            mime="application/pdf"
        )

if st.button(" Clear All Queries"):
    st.session_state["query_history"] = []
    st.session_state["responses"] = {}
    st.experimental_rerun()
