import streamlit as st
import pandas as pd
import ast
import intely_task
import datetime
import intely_task

import enginer_center
user_file = 'manufacture.csv'

user_df = pd.read_csv(user_file)
user_df = user_df[['name','username','description','categories','projects','work_history']]
user_df['categories'] = user_df['categories'].apply(lambda x: ast.literal_eval(x))

def print(manufacture, add_butt=True):
    st.markdown('### ' + manufacture['name'])

    st.markdown(f'> Описание: {manufacture.description}')
    st.markdown(f"> {manufacture.work_history}")
    if add_butt:
        st.markdown(f'[Подробнее...](http://localhost:8501/?manufacture={manufacture.username})', unsafe_allow_html=True)
    st.markdown(f'Категории: ```{"```, ```".join(manufacture.categories)}```')
    st.write('_'*50)

def print_by_username(username, add_butt=False):
    try:
        manufacture = user_df[user_df.username == username].iloc[0]
        print(manufacture)
    except:
        st.error("Произвоство не может быть отображено")


def run(author: str, username, user_df=user_df):
    params = st.experimental_get_query_params()

    user = user_df[user_df.username == username].iloc[0]

    if 'user' in params.keys():
        st.write("Просмотр профиля:")
        print(user, add_butt=False)
    elif 'edit_user' in params.keys():
        st.write("Редактирование профиля:")

        with st.form(key='user_edit'):
            new_user = {
                'name' : st.text_input('Наименование',value= ''),
                'username': username,
                'description' : st.text_input('Описание',value= ''),
                'categories' :  st.multiselect('Направления', options=intely_task.science_types),
                'projects' : [],
                'work_history' :st.text_input('Общее резюмирование работ',value= '')
            }
            submit = st.form_submit_button('Сохранить')
            if submit:
                user_df = user_df.append(new_user, ignore_index=True,)
                user_df.to_csv(user_file)
    else:
        tab0, tab01, tab1, tab2, tab3, tab4 = st.tabs(["👩‍🎓Партнёры","💼Мои проекты","🌍Создать задачу", "🧠Задачи", '🔆Создать хакатон', '👨‍👨‍👦‍👦Хакатоны'])
        with tab01:
            st.write("Список ваших проектов")
        with tab0:
            for i, row in enginer_center.user_df.iterrows():
                st.header(row['name'])
        with tab1: #creating
            with st.form("task_creating"):
                st.write("Создание задачи")
    
                #,name, categories, author, description, money
                task_name = st.text_input('Название задачи')
                task_description = st.text_input('Описание задачи')
                task_categories = st.multiselect('Категории задачи', options=intely_task.science_types)
                task_author = author
                task_money = st.number_input('Сумма вознаграждения', min_value=100)
                #intely_task.task(task_name,task_categories,task_author,task_description,task_money)
                task = {'task_name':task_name,
                        'categories':task_categories,
                        'author':task_author,
                        'description':task_description,
                        'money':task_money}
                # Every form must have a submit button.
                st.multiselect("Исполнитель", options=enginer_center.user_df)
                view = st.selectbox('Видимость задачи:',['Всем пользователям','Только партнёрам'])
                submitted = st.form_submit_button("Submit")
                if submitted:
                    if task_name != "" and task_description != "" and task_money > 0 and len(task_categories) > 0:
                        intely_task.tasks = intely_task.tasks.append(task, ignore_index=True,)
                        intely_task.tasks.to_csv(intely_task.tasks_file)
                        st.success('Задача успешно создана!')
                    else:
                        st.warning('Поля не заполнены, или заполнены не корректно!')

        with tab2: #list of tasks
            show_other = st.checkbox("Показать чужие задачи", value=False)
            for indx, task in intely_task.tasks.iterrows():
                #task = intely_task.tasks.iloc[indx]
                if task.author == author or show_other:
                    type = 'owner' if task.author == author else 'user'
                    intely_task.print(task,add_butt=type, indx=indx)
        with tab3: #tender creating
            with st.form("tender_creating"):
                st.write("Создание конкурса")
    
                #,name, categories, author, description, money
                tender_name = st.text_input('Название задачи')
                tender_description = st.text_input('Описание задачи')
                tender_categories = st.multiselect('Категории задачи', options=intely_task.science_types)
                tender_author = author
                tender_money = st.number_input('Сумма вознаграждения', min_value=100,max_value=999999999)
                tender_tasks = st.multiselect('Конкурсные задачи', options=intely_task.tasks[intely_task.tasks['author'] == author])
                tender_start = st.date_input('Дата запуска')
                tender_end = st.date_input('Дата окончания')

                #temp_tender = tender(name=tender_name, tasks=[], tender_categories,tender_author,tender_description,tender_money)
                # Every form must have a submit button.
                submitted = st.form_submit_button("Создать хакатон!")
                if submitted:
                    intely_task.tenders = intely_task.tenders.append(
                        {
                            'tender_name':tender_name,
                            'categories':tender_categories,
                            'author':tender_author,
                            'description':tender_description,
                            'money':tender_money,
                            'tasks':tender_tasks,
                            'start_dt':tender_start,
                            'end_dt':tender_end
                        },
                        ignore_index=True
                    )
                    intely_task.tenders.to_csv(intely_task.tenders_file)
                    intely_task.print(task,indx=0)
        with tab4: #tenders list
            for indx, tender in intely_task.tenders.iterrows():
                #task = intely_task.tasks.iloc[indx]
                if tender.author == author:
                    intely_task.print_tender(tender,add_submit_butt=False, indx=indx)