import streamlit as st
import intely_task
import pandas as pd
import ast 
import manufacture

user_file = 'engineering_centers.csv'

def print(eng_center, add_butt=True):
    st.markdown('### ' + eng_center['name'])
    col1, col2 = st.columns([1, 3])

    st.markdown(f'> Описание: {eng_center.description}')
    st.markdown(f"> {eng_center.work_history}")
    if add_butt:
        st.markdown(f'[Подробнее...](http://localhost:8501/?eng_center={eng_center.username})', unsafe_allow_html=True)
    st.markdown(f'Категории: ```{"```, ```".join(eng_center.categories)}```')
    st.markdown(f'Направления: ```{"```, ```".join(eng_center.professions)}```')
    st.write('_'*50)

def run(username):
    params = st.experimental_get_query_params()
    user_df = pd.read_csv(user_file)
    user_df = user_df[['name','username','description','professions','categories','projects','work_history']]
    user_df['categories'] = user_df['categories'].apply(lambda x: ast.literal_eval(x))
    user_df['professions'] = user_df['professions'].apply(lambda x: ast.literal_eval(x))

    user = user_df[user_df.username == username].iloc[0]

    if 'user' in params.keys():
        st.write("Просмотр профиля:")
        st.write(user.to_dict())
    elif 'edit_user' in params.keys():
        st.write("Редактирование профиля:")
        
        with st.form(key='user_edit'):
            new_user = {
                'name' : st.text_input('Наименование',value= user['name']),
                'username': username,
                'description' : st.text_input('Описание',value= user['description']),
                'professions' : st.multiselect('Специалисты', options=intely_task.professions),
                'categories' :  st.multiselect('Направления', options=intely_task.science_types),
                'projects' : [],
                'work_history' :st.text_input('Общее резюмирование работ',value= user['work_history'])
            }
            submit = st.form_submit_button('Сохранить')
            if submit:
                user_df = user_df.append(new_user, ignore_index=True,)
                user_df.to_csv(user_file)

    else:
        st.sidebar.markdown('[✍ Изменить профиль](http://localhost:8501/?edit_user=1)')
        st.write("Поиск задач:")
        science_types = ['Химия','Физика','Медицина','Разработка','Машиностроение','Социалогия']

        target = st.multiselect(options=science_types, label='Целевые научные разделы(инж.центр):')
        tab1, tab2, tab3, tab4 = st.tabs(['🧠Задачи', '👨‍👨‍👦‍👦Хакатоны', '🦾Инжениринговые центры','🏭Предприятия'])
        with tab1:
            for indx,task  in intely_task.tasks.iterrows():
                #task = intely_task.tasks[indx]
                if True in [(category in target) for category in task.categories] or len(target) == 0:
                    intely_task.print(task,add_butt=True, indx=indx)
        with tab2:
            for indx, tender in intely_task.tenders.iterrows():
                #task = intely_task.tasks.iloc[indx]
                if True in [(category in target) for category in tender.categories] or len(target) == 0:
                    intely_task.print_tender(tender,add_submit_butt=True, indx=indx)
        with tab3:
            for indx, user in user_df.iterrows():
                #task = intely_task.tasks.iloc[indx]
                if True in [(category in target) for category in user.categories] or len(target) == 0:
                    print(user,add_butt=True)
        with tab4:
            manufactures = pd.read_csv ('manufacture.csv')
            manufactures['categories'] = manufactures['categories'].apply(lambda x: ast.literal_eval(x))
            for indx, user in manufactures.iterrows():
                #task = intely_task.tasks.iloc[indx]
                if True in [(category in target) for category in user.categories] or len(target) == 0:
                    manufacture.print(user,add_butt=True)
