import streamlit as st
import intely_task

import ind_prof
import enginer_center
import manufacture

st.set_page_config(
        page_title="Inteligent Market",
        page_icon=":brain:",
        layout="wide",
    )
st.title("Маркетплейс разумов")

import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)


authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login('Login', 'sidebar')

st.session_state["authentication_status"] = authentication_status
st.session_state["name"] = name
st.session_state["username"] = username


if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'sidebar')
    st.sidebar.write(f'Welcome *{st.session_state["name"]}*')


    params = st.experimental_get_query_params()
    st.sidebar.markdown('[👀 Просмотр профиля](http://localhost:8501/?user=1)')
    st.sidebar.markdown('[✍ Изменить профиль](http://localhost:8501/?edit_user=1)')

    if 'task' in params.keys():
        st.write('Вы выбрали задачу: ')
        indx = int(params["task"][0])
        task = intely_task.tasks.iloc[indx]
        intely_task.print(task, indx=indx)
        place = st.empty()
        approv = False
        if username in task['approved_workers']:
            place.file_uploader(label='Архив с решение', type=['.zip', '.rar', '.tar', '.7z'])
        elif username in task['waiting_workers']:
            place.write("Ожидается разрешение на выполнение...")
        else:
            approv = place.button('📧 Запросить разрешение на выполнение!')
        if approv:
            intely_task.add_worker(username,indx)
            place.write("Ожидается разрешение на выполнение...")
        col_b1, col_b2 = st.columns([9,1])
        with col_b2:
            st.markdown(f'[Главная](http://localhost:8501/)')
    elif 'tender' in params.keys():
        st.write('Вы выбрали хакатон: ')
        indx = int(params["tender"][0])
        intely_task.print_tender(intely_task.tenders.iloc[indx], indx=indx, add_resolve=True)
        col_b1, col_b2 = st.columns([9,1])
        with col_b2:
            st.markdown(f'[Главная](http://localhost:8501/)')
    elif 'eng_center' in params.keys():
        st.write('Вы выбрали инжениринговый центр: ')
        indx = params["eng_center"][0]
        enginer_center.print_by_username(indx)
        col_b1, col_b2 = st.columns([9,1])
        with col_b2:
            st.markdown(f'[Главная](http://localhost:8501/)')
    elif 'manufacture' in params.keys():
        st.write('Вы выбрали инжениринговый центр: ')
        indx = params["manufacture"][0]
        manufacture.print_by_username(indx)
        col_b1, col_b2 = st.columns([9,1])
        with col_b2:
            st.markdown(f'[Главная](http://localhost:8501/)')
    else:
        if config['credentials']['usernames'][username]['role'] == 'eng_centr':
            enginer_center.run(username)
        elif config['credentials']['usernames'][username]['role'] == 'manufactory':
            manufacture.run(name, username)
        elif config['credentials']['usernames'][username]['role'] == 'ind_prof':
            ind_prof.run()

elif st.session_state["authentication_status"] == False:
    st.sidebar.error('Username/password is incorrect')
elif st.session_state["authentication_status"] == None:
    st.sidebar.warning('Please enter your username and password')
    try:
        if authenticator.register_user('Register user', location= 'sidebar', preauthorization=False):
            st.success('User registered successfully')
            with open('./config.yaml', 'w') as file:
                yaml.dump(config, file, default_flow_style=False)
    except Exception as e:
        st.error(e)
