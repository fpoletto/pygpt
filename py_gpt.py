from openai import OpenAI
import streamlit as st
from streamlit_chat import message
import random

API_KEY = st.secrets.openai_token

st.title('Aprender Python')
st.subheader('Um lugar legal para você tirar suas dúvidas sobre o Python.')

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
    answer = completion.choices[0].message.content
    st.session_state['messages'].append({"role": "assistant", "content": answer})

with st.form(key='basic'):
    creativity = st.slider('Nível de criatividade', 0.0, 1.0)
    question = st.text_area('Qual sua dúvida?')
    submit_button = st.form_submit_button("Enviar")
    if submit_button:
        conversation(question, creativity)
        question = ''

tab1, tab2, tab3 = st.tabs(["Coversa", "Código", "Utilidades"])
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
with tab3:
    with st.expander('Assistente de programação com ChatGPT'):
        st.code("""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
    
    def code():
        #ESCREVA SEU CÓDIGO TODO DENTRO DESSA FUNÇÃO
        #OU
        #import SEU_SCRIPT
        #SEU_SCRIPT()
    
    if __name__ == '__main__':
        try:
            code()
    
        except Exception as E:
            try:
                from openai import OpenAI
                import json
                import time
    
                ID = INSIRA_ID_DO_ASSISTENTE
                API_KEY = INSIRA_SUA_CHAVE_AQUI
                client = OpenAI(api_key=API_KEY)
    
                chat = client.beta.threads.create(
                messages=[
                    {"role": "user", "content": f\"""Eu tentei rodar um script, mas recebi uma mensagem de erro.
                        Tente me explicar como resolver esse problema. Use exemplos. Dê alternativas.
                        Consulte a documentação dos módulos, se for preciso.
                        Código: {str(code)}
                        Erro recebido: {E}\"""}
                        ],
                    )
    
                run = client.beta.threads.runs.create(thread_id=chat.id, assistant_id=ID)
                print(f'Erro encontrado: {E}')
                print('Buscando solução.', end='')
    
                while run.status != 'completed':
                    run = client.beta.threads.runs.retrieve(thread_id=chat.id, run_id=run.id)
                    print(f'.', end='')
                    time.sleep(.5)
                else:
                    print('')
                
                message_response = client.beta.threads.messages.list(thread_id=chat.id)
                messages =  message_response.data
                this_msg = messages[0]
                print(this_msg.content[0].text.value)
    
            except Exception as E:
                print(E)
        """)
