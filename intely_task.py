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
tasks = tasks[['task_name', 'categories', 'author', 'description', 'money']]

tenders_file = 'tenders.csv'
tenders = pd.read_csv(tenders_file)
tenders['categories'] = tenders['categories'].apply(
    lambda x: ast.literal_eval(x))
tenders['tasks'] = tenders['tasks'].apply(lambda x: ast.literal_eval(x))
tenders = tenders[['tender_name', 'categories', 'author',
                   'description', 'money', 'tasks', 'start_dt', 'end_dt']]


class task():
    """Intelegent task from manufacture to engineering center """

    def __init__(self, name, categories, author, description, money):
        self.name = name
        self.categories = categories
        self.author = author
        self.description = description
        self.money = money

    def print(self, indx: int, add_butt=False):
        st.markdown('### ' + self.name)
        col1, col2 = st.columns([1, 3])
        with col1:
            st.write('Категории:', ','.join(self.categories))
            st.write('Автор:', self.author)
        with col2:
            st.write('Описание:\n', self.description)
            st.markdown(f"Вознаграждение ```{self.money}```")
            if add_butt:
                st.markdown(
                    f'[Принять задачу](http://localhost:8501/?task={indx})', unsafe_allow_html=True)
        st.write('_'*50)


def print(task, indx: int, add_butt=False):
    st.markdown('### ' + task.task_name)
    col1, col2 = st.columns([1, 3])
    with col1:
        st.write('Категории:', ','.join(task.categories))
        st.write('Автор:', task.author)
    with col2:
        st.write('Описание:\n', task.description)
        st.markdown(f"Вознаграждение ```{task.money}```")
        if add_butt:
            st.markdown(
                f'[Принять задачу](http://localhost:8501/?task={indx})', unsafe_allow_html=True)
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


"""
[
    task('Разработка шасси', ['Машиностроение'], 'РосАвиаПолёт', 'Требуется разработать шасси из углепластика для самолётов средней категории размерности', 10000),
    task('Разработка кабины', ['Машиностроение'], 'РосАвиаПолёт', 'Требуется разработать кабину из углепластика для самолётов средней категории размерности', 5000),
    task('Разработка углепластика', ['Химия'], 'РосАвиаПолёт', 'Требуется разработать лёгкий высокопрочный углепластик для самолётов', 7000),
    task('Разработка системы жизнеобеспечения', ['Медицина'], 'РосАвиаПолёт', 'Требуется разработать систему жизнеобеспечения для самолётов средней категории размерности', 9000),
    task('Разработка системы АВИА навигации', ['Разработка'], 'МосГорПолёт', 'Требуется разработать систему жизнеобеспечения для самолётов средней категории размерности', 50000),
]

"""
