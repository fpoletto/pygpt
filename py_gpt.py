import openai
import streamlit as st
from streamlit_chat import message
import random

openai.api_key = st.secrets.openai_token

st.title('PyGPT')
st.subheader('Seu assistente pessoal de Python.')

if 'system_prompt' not in st.session_state:
    st.session_state['system_prompt'] = [{"role": "system",
                                          "content": "Você é um experiente assistente de programação em "
                                                     "Python. Faça o possível para tirar as dúvidas do "
                                                     "usuário. Não deixe passar nenhum detalhe."}]
container = st.empty()
container.write(f"Prompt de sistema: {st.session_state['system_prompt'][0]['content']}")

def conversation(this_question):
    global creativity
    st.session_state['system_prompt'].append({"role": "user", "content": this_question})
    used_tokens = len(str(st.session_state['system_prompt']))
    available_tokens = 4096 - used_tokens
    response = openai.ChatCompletion.create(model='gpt-3.5-turbo',
                                            messages=st.session_state['system_prompt'],
                                            temperature=creativity,
                                            max_tokens=available_tokens,
                                            n=1)

    response_text = response['choices'][0]['message']['content']
    st.session_state['system_prompt'].append({"role": "assistant", "content": response_text})

with st.form(key='basic'):
    creativity = st.slider('Nível de criatividade', 0.0, 1.0)
    question = st.text_input('Qual sua dúvida?')
    st.form_submit_button("Enviar", on_click=conversation(question))
    question = ''

tab1, tab2 = st.tabs(["Coversa", "Código"])
with tab1:
    for i in st.session_state['system_prompt']:
        if i['role'] == 'system' or i['content'] == '':
            pass
        elif i['role'] == 'user':
            message(is_user=True, message=i['content'], key=random.randint(0, 999))
        else:
            message(is_user=False, message=i['content'], key=random.randint(0, 999))

with tab2:
    for i in st.session_state['system_prompt']:
        if i['role'] == 'system' or i['content'] == '':
            pass
        elif i['role'] == 'user':
            st.markdown(f"Usuário: {i['content']}")
        else:
            st.markdown(f"Assistente: {i['content']}")

print(st.session_state['system_prompt'])
