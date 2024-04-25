from openai import OpenAI
import streamlit as st
from streamlit_chat import message
import random

API_KEY = st.secrets.openai_token

st.title('PyGPT')
st.subheader('Seu assistente pessoal de Python.')

if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": "Você é um especialista na linguagem Python. Breve e direto, sempre atende com educação às dúvidas dos alunos."}
        ]
    
container = st.empty()
container.write(f"Prompt de sistema: {st.session_state['messages'][0]['content']}")

def conversation(this_question, creativity):
    this_message = {"role": "user", "content": this_question}
    st.session_state['messages'].append(this_message)
    client = OpenAI(api_key=API_KEY)

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=creativity,
        messages=st.session_state['messages'],
    )
    # print(completion.choices[0].message.content)
    answer = completion.choices[0].message.content
    # print(answer)
    st.session_state['messages'].append({"role": "assistant", "content": answer})

with st.form(key='basic'):
    creativity = st.slider('Nível de criatividade', 0.0, 1.0)
    question = st.text_area('Qual sua dúvida?')
    submit_button = st.form_submit_button("Enviar")
    if submit_button:
        conversation(question, creativity)
        question = ''

tab1, tab2 = st.tabs(["Coversa", "Código"])
with tab1:
    for i in st.session_state['messages']:
        if i['role'] == 'system' or i['content'] == '':
            pass
        elif i['role'] == 'user':
            message(is_user=True, message=i['content'], key=random.randint(0, 999))
        else:
            message(is_user=False, message=i['content'], key=random.randint(0, 999))

with tab2:
    for i in st.session_state['messages']:
        if i['role'] == 'system' or i['content'] == '':
            pass
        elif i['role'] == 'user':
            st.markdown(f"Usuário: {i['content']}")
        else:
            st.markdown(f"Assistente: {i['content']}")

print(st.session_state['messages'])
