import openai
import streamlit as st
from streamlit_chat import message

openai.api_key = st.secrets["OPENAI_API_KEY"]

prompt = """
You need to engage in conversation with the student, keeping in mind the prompt 'I am an English teacher teaching third-grade students at an elementary school in Korea.
Today, I've decided to have a conversation about clothes with my Korean third-grade students.
I'll start with the questions, and when the students respond, I should continue the conversation with appropriate reactions.
Keep in mind that they are 9 years old, so I shouldn't ask overly difficult questions or expect complicated answers.
If a student says something inappropriate, I should let them know it's not acceptable.
I should also avoid saying anything inappropriate myself.
If a student's grammar is incorrect, I need to identify the error and provide an example sentence with the correct grammar in context.'. 
The student will answer the question 'What are you wearing now?' and you should continue the conversation by asking about clothes in context with their response.
"""

user_message = """
The answer to "What are you wearing now?" could be
"""
def generate_response(prompt,user_message):
    completions = openai.chat.completions.create(
        model = "gpt-4-0125-preview",
        stop=None,
        temperature=1.0,
        top_p = 1, 
        messages = [
             {'role':'system', 'content' :'What are you wearing now?'},
             {'role' :'user', 'content':user_message},
             {'role':'system', 'content':prompt},
            # {'role':'assistant', 'content':prompt}
        ]
    )

    # response = openai.completions.create(
    #     model = "gpt-4-0125-preview",
    #     prompt = prompt,
    # )

    message = completions.choices[0].message.content
    return message

st.header("GPT TEST - EDUCLOUD DIGITALHUMAN TFT")

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

with st.form('form', clear_on_submit=True):
    user_input = st.text_input("Student : ", "", key='input')
    submitted = st.form_submit_button('send')

st.subheader("What are you wearing now?")

if submitted and user_input:
    output = generate_response(prompt,user_input)
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        message(st.session_state['generated'][i], key=str(i))
