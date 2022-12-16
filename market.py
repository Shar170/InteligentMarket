import streamlit as st
import intely_task
#import auth_module as am

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

    if 'task' in params.keys():
        st.write('Вы выбрали задачу: ')
        indx = int(params["task"][0])
        intely_task.print(intely_task.tasks.iloc[indx], indx=indx)
        st.file_uploader(label='Архив с решение', type=['.zip', '.rar', '.tar', '.7z'])
        col_b1, col_b2 = st.columns([9,1])
        with col_b2:
            st.markdown(f'[Главная](http://localhost:8501/)')
    elif 'tender' in params.keys():
        st.write('Вы выбрали задачу: ')
        indx = int(params["tender"][0])
        intely_task.print_tender(intely_task.tenders.iloc[indx], indx=indx, add_resolve=True)
        col_b1, col_b2 = st.columns([9,1])
        with col_b2:
            st.markdown(f'[Главная](http://localhost:8501/)')
    else:
        if config['credentials']['usernames'][username]['role'] == 'eng_centr':
            import enginer_center
            enginer_center.run(username)
        elif config['credentials']['usernames'][username]['role'] == 'manufactory':
            import manufacture
            manufacture.run(name, username)
        elif config['credentials']['usernames'][username]['role'] == 'ind_prof':
            import ind_prof
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
