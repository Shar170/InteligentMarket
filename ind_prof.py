import streamlit as st
import intely_task



def run():

    st.write("Поиск задач:")

    science_types = ['Химия','Физика','Медицина','Разработка','Машиностроение','Социалогия']

    target = st.multiselect(options=science_types, label='Целевые научные разделы(инж.центр):')
    tab1, tab2 = st.tabs(['Задачи', 'Хакатоны'])
    with tab1:
        for indx,task  in intely_task.tasks.iterrows():
            #task = intely_task.tasks[indx]
            if True in [(category in target) for category in task.categories] or len(target) == 0:
                intely_task.print(task,add_butt=True, indx=indx)
    with tab2:
        for indx, tender in intely_task.tenders.iterrows():
            #task = intely_task.tasks.iloc[indx]
            if True in [(category in target) for category in tender.categories] or len(target) == 0:
               intely_task.print_tender(tender,add_butt=False, indx=indx)