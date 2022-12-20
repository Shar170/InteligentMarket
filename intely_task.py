import streamlit as st
import pandas as pd
import ast

science_types = ['Химия', 'Физика', 'Медицина',
                 'Разработка', 'Машиностроение', 'Социалогия']

professions = []
with open('professions.txt', encoding='utf-8') as file:
    professions = [line.rstrip() for line in file]

competions = []
with open('competions.txt', encoding='utf-8') as file:
    competions = [line.rstrip() for line in file]

tasks_file = 'tasks.csv'
tasks = pd.read_csv(tasks_file)
tasks['categories'] = tasks['categories'].apply(lambda x: ast.literal_eval(x))
tasks['approved_workers'] = tasks['approved_workers'].apply(lambda x: ast.literal_eval(x))
tasks['waiting_workers'] = tasks['waiting_workers'].apply(lambda x: ast.literal_eval(x))
tasks = tasks[['task_name', 'categories', 'author', 'description', 'money','approved_workers','waiting_workers']]

tenders_file = 'tenders.csv'
tenders = pd.read_csv(tenders_file)
tenders['categories'] = tenders['categories'].apply(
    lambda x: ast.literal_eval(x))
tenders['tasks'] = tenders['tasks'].apply(lambda x: ast.literal_eval(x))
tenders = tenders[['tender_name', 'categories', 'author',
                   'description', 'money', 'tasks', 'start_dt', 'end_dt']]

def print(task, indx: int, add_butt='none'):
    """@add_butt: none, user, owner, approving"""
    st.markdown('### ' + task.task_name)
    col1, col2 = st.columns([1, 3])
    with col1:
        st.write('Категории:', ','.join(task.categories))
        st.write('Автор:', task.author)
    with col2:
        st.write('Описание:\n', task.description)
        st.markdown(f"Вознаграждение ```{task.money}```")
        if add_butt == 'user':
            st.markdown(
                f'[Принять задачу](http://localhost:8501/?task={indx})', unsafe_allow_html=True)
    if add_butt == 'owner':
        if len(task.waiting_workers) > 0:
            st.multiselect(key=f'{task.task_name} #{indx}',label='Передать на исполнение:', options=task.waiting_workers,default=task.approved_workers)   
        else:
            st.write("💔 Задача ожидает исполнителя")  
    st.write('_'*50)


def print_tender(tender, indx: int, add_submit_butt=False, add_resolve=False):
    st.markdown('### ' + tender.tender_name)
    col1, col2 = st.columns([1, 3])
    with col1:
        st.write('Категории:', ', '.join(tender.categories))
        st.write('Автор:', tender.author)
    with col2:
        st.write('Описание:\n', tender.description)
        st.write('Задачи:', ', '.join(tender.tasks))
        st.markdown(f"Вознаграждение ```{tender.money}```")
    st.markdown(
        f"Дата проведения: {tender.start_dt} - {tender.end_dt}        {f'[✅Принять участие](http://localhost:8501/?tender={indx})' if add_submit_butt else ''}", unsafe_allow_html=True)
    #if add_butt : st.markdown(f'[Принять задачу](http://localhost:8501/?task={indx})', unsafe_allow_html=True)

    if add_resolve:
        col1, col2 = st.columns([1, 1])
        with col1:
            current_task = st.selectbox('Решаемая задача:', tender.tasks)
        with col2:
            st.file_uploader(label='Архив с решение', type=[
                             '.zip', '.rar', '.tar', '.7z'])
    st.write('_'*50)

def add_worker(username:str,indx:int, tasks=tasks):
    workers = tasks['waiting_workers'].iloc[indx]
    if username not in workers:
        workers.append(username)
        tasks.at[indx, 'waiting_workers'] = workers
        tasks.to_csv(tasks_file)

def approve_worker(username:str,indx:int, tasks=tasks):
    workers = tasks['approved_workers'].iloc[indx]
    if username not in workers:
        workers.append(username)
        tasks.at[indx, 'approved_workers'] = workers
        tasks.to_csv(tasks_file)