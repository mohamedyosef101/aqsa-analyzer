# get what we need
import streamlit as st
from streamlit_chat import message
import google.generativeai as palm
import apis

# start with the api
from apis import palm_api_key
palm_api_key = palm_api_key



# Work with Streamlit

# the layout Variables
st.set_page_config(page_title="AQSA Version-1") 


# HERO

# the header
st.markdown('<h1 style="text-align:center; position:relative; top:20%;">بسم الله الرحمن الرحيم</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; position:relative; top:30%;">Version-1</p>', unsafe_allow_html=True)

st.markdown("""<div style="position:relative; margin: auto; text-align: center;">
              <img src="https://github.com/mohamedyosef101/mohamedyosef101/assets/118842452/de6eec9a-ee85-4ff2-9e48-37e4108aad17" width=256>
            </div>""", unsafe_allow_html=True)



if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "أهلا بيك، ازاي اقدر اساعدك؟"}]

with st.form("chat_input", clear_on_submit=True):
    a, b = st.columns([4, 1])

    user_prompt = a.text_input(
        label="اكتب رسالتك:",
        placeholder="ماذا تريد أن تعرف ...",
        label_visibility="collapsed",
    )

    b.form_submit_button("إرسال", use_container_width=True)

for msg in st.session_state.messages:
    message(msg["content"], is_user=msg["role"] == "user")  # display message on the screen

if user_prompt and palm_api_key:

    palm.configure(api_key=palm_api_key)  # set API key

    st.session_state.messages.append({"role": "user", "content": user_prompt})
    
    message(user_prompt, is_user=True)

    response = palm.chat(context="Act as a Bussiness Expert whose job is to help people improve their business.", messages=[user_prompt])  # get response from Google's PaLM API

    msg = {"role": "assistant", "content": response.last}  # we are using dictionary to store message and its role. It will be useful later when we want to display chat history on the screen, to show user input at the left and AI's right side of the screen.

    st.session_state.messages.append(msg)  # add message to the chat history

    message(msg["content"])  # display message on the screen