import streamlit as st
import student_report_chatbot_gemini as c
import time


def stream_data(response):
    for word in response.split():
        if word == "*":
            yield "\n" + word
        else:
            yield word + " "
        time.sleep(0.05)

def display_user_prompt(user_input):
        
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
    return user_input

st.image("./image/assessli_1.jpg",width = 50,use_column_width= "auto")
st.title("Student Report Assistant")

with st.form("my_form"):

   selected_student = st.sidebar.selectbox("Select Student",options=["Sharanya","Manasvi"], placeholder="Choose Student",)
   with st.sidebar:
    submitted = st.form_submit_button("Submit")
   if submitted:
       c.get_json(selected_student)

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User-provided prompt
if chat_query := st.chat_input("Say something"):
     
     prompt =display_user_prompt(chat_query)
    

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("..."):
            response = c.chat_response(prompt)
            # st.write_stream(stream_data(response))
            # st.write(response) 
            # response = generate_llama2_response(prompt)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)
