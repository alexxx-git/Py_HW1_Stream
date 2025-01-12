import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from analysis import detect_anomalies, calculate_moving_average, seasonal_statistics
from utils import load_data
from weather_api import get_current_temperature, is_temperature_normal

# Заголовок приложения
st.title('Анализ температуры')

# Боковое меню для ввода данных
with st.sidebar:
    # Опция загрузки исторических данных
    load_data_option = st.checkbox('Загрузить исторические данные')

    # Переменная для хранения данных
    data = None

    if load_data_option:
        # Загрузка файла с историческими данными
        uploaded_file = st.file_uploader("Загрузите CSV файл с историческими данными", type=["csv"])

        if uploaded_file is not None:
            # Если файл загружен, используем его для анализа
            data = load_data(uploaded_file)
            st.write("Данные успешно загружены!")
        else:
            st.warning("Пожалуйста, загрузите файл для продолжения анализа.")
    else:
        # Если данные не загружаются, используем стандартный CSV
        data = load_data('data/temperature_data.csv')

    # Ввод API-ключа
    api_key = st.text_input('Введите свой ключ API OpenWeatherMap:')

    # Список городов из данных
    if data is not None:
        cities = data['city'].unique()
        # Выбор города
        city_name = st.selectbox('Выберите город', cities)
    else:
        city_name = None
        st.warning("Выберите или загрузите данные для анализа.")

# Основная функция для выполнения анализа
if data is not None and city_name is not None:
    # Фильтрация данных для выбранного города
    city_data = data[data['city'] == city_name]

    # Текущая температура
    st.subheader('Текущая температура')
    current_temp = get_current_temperature(city_name, api_key)

    # Проверка на успешность запроса
    if isinstance(current_temp, dict) and current_temp.get("cod") == 401:
        st.error(f"Неверный ключ API: {current_temp['message']}")
    elif isinstance(current_temp, dict) and current_temp.get("cod") != 200:
        st.error(f"Ошибка запроса: {current_temp.get('message', 'Неизвестная ошибка')}")
    else:
        # Проверка на корректность данных температуры
        if 'main' in current_temp and 'temp' in current_temp['main']:
            current_temp_value = current_temp['main']['temp']
            st.write(f"Текущая температура в {city_name}: {current_temp_value}°C")
            normal = is_temperature_normal(city_name, current_temp_value, city_data)
            st.write(f"Температура {'нормальная' if normal else 'аномальная'} для текущего сезона.")

    # Вычисление описательной статистики
    desc_stats = city_data['temperature'].describe()

    # Отображение таблицы с описательной статистикой
    st.subheader('Описательная статистика')
    st.write(desc_stats)

    # Анализ исторических данных
    season_stats = seasonal_statistics(city_data)
    anomalies = detect_anomalies(city_data, season_stats)
    city_data = calculate_moving_average(city_data)

    # Визуализация временных рядов и скользящего среднего
    st.subheader('Временные ряды с скользящим средним')
    fig1, ax1 = plt.subplots(figsize=(15, 6))
    ax1.plot(city_data['timestamp'], city_data['temperature'], label='Temperature', color='blue')
    ax1.plot(city_data['timestamp'], city_data['moving_average'], label='30-Day Moving Average', color='orange')
    ax1.set_title(f'Временные ряды температуры и скользящее среднее для {city_name}')
    ax1.legend()
    st.pyplot(fig1)

    # Визуализация аномалий
    st.subheader('Аномалии температуры')
    fig2, ax2 = plt.subplots(figsize=(15, 6))
    ax2.plot(city_data['timestamp'], city_data['temperature'], label='Temperature', color='blue')
    ax2.scatter(anomalies['timestamp'], anomalies['temperature'], color='red', label='Anomalies')
    ax2.set_title(f'Аномалии температуры для {city_name}')
    ax2.legend()
    st.pyplot(fig2)

    # Визуализация стандартного отклонения по сезонам
    st.subheader('Стандартное отклонение температуры по сезонам')
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    season_stats['std'].plot(kind='bar', ax=ax3, color='purple')
    ax3.set_title(f'Стандартное отклонение температуры по сезонам для {city_name}')
    ax3.set_ylabel('Стандартное отклонение')
    st.pyplot(fig3)

    # Таблица средней температуры и стандартного отклонения
    st.subheader('Средняя температура и стандартное отклонение по сезонам')
    st.write(season_stats[['mean', 'std']])

    # Визуализация гистограммы температур
    st.subheader('Распределение температур')
    fig4, ax4 = plt.subplots(figsize=(10, 6))
    ax4.hist(city_data['temperature'], bins=30, color='skyblue', edgecolor='black')
    ax4.set_title(f'Гистограмма температур для {city_name}')
    ax4.set_xlabel('Температура (°C)')
    ax4.set_ylabel('Частота')
    st.pyplot(fig4)

    # Визуализация коробчатой диаграммы (boxplot)
    st.subheader('Коробчатая диаграмма температур')
    fig5, ax5 = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=city_data['temperature'], ax=ax5, color='orange')
    ax5.set_title(f'Коробчатая диаграмма температур для {city_name}')
    st.pyplot(fig5)
else:
    st.warning("Пожалуйста, выберите или загрузите данные для анализа.")
