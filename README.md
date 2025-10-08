![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-1.4+-D71F00?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3.0+-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=jsonwebtokens&logoColor=white)


# 🎧 MyLibrary API

Учебный проект на **FastAPI + SQLModel**, созданный для практики работы с современными веб-технологиями.

---

## 🚀 О проекте

**MyLibrary** — это REST API для управления музыкальной библиотекой.  
Можно добавлять треки, жанры, пользователей и управлять ими через роли.  
Проект полностью написан с нуля — без генераторов или шаблонов, с ручной настройкой роутеров, зависимостей и авторизации.

---

## 💡 Личный комментарий

Мне понравилось разрабатывать на **FastAPI** — тут действительно ощущается, что всё под контролем.  
В отличие от Django, где многое "происходит само", здесь вся ответственность на тебе.  
Проектировать структуру поначалу было сложно, но это и есть самое интересное.

В этом проекте я **впервые подключил базу данных** к коду и реализовал **JWT авторизацию** — то, что не совсем получилось у меня в прошлом проекте на DRF.  
Особенно понравилось **работать с типами данных** — аннотации Python кажутся чем-то свежим и современным, и, думаю, за этим будущее.

Работа с моделями в SQLModel показалась менее интуитивной, чем в Django ORM,  
но теперь я понимаю её устройство и могу гибко управлять схемой и связями.

---

## 🧩 Возможности

- 🔑 Регистрация и авторизация пользователей (JWT)
- 👥 Роли пользователей (user / admin)
- 🎵 CRUD для треков и жанров
- 🔍 Фильтрация и пагинация списка
- 🧱 Валидация данных через Pydantic
- 🕒 Отслеживание даты создания объектов

---

## 🛠️ Технологии

- **Python 3.11+**
- **FastAPI**
- **SQLModel**
- **SQLAlchemy**
- **SQLite**
- **Passlib (argon2)**
- **PyJWT**

---

## ▶️ Запуск проекта

```bash
# Клонировать репозиторий
git clone https://github.com/kuramagod/MyLibrary.git
cd MyLibrary

# Создать и активировать виртуальное окружение
python -m venv venv
venv\Scripts\activate  # для Windows
source venv/bin/activate  # для Linux/Mac

# Установить зависимости
pip install -r requirements.txt

# Запустить сервер
uvicorn main:app --reload
# или
fastapi dev main.py
```
После запуска проект будет доступен по адресу:
👉 http://127.0.0.1:8000

---

## 📘 Документация API

Swagger UI — [/docs](http://127.0.0.1:8000/docs)  
ReDoc — [/redoc](http://127.0.0.1:8000/redoc)  

---

## ⚙️ Структура проекта

```bash
mylibrary/
├── routers/             # Эндпоинты API
├── config.py            # Конфигурация проекта
├── database.py          # Подключение к БД
├── dependencies.py      # Авторизация и вспомогательные функции
├── main.py              # Точка входа FastAPI
└── models.py            # SQLModel модели
```

---

## 🧠 Что я изучил

- Создание REST API с FastAPI
- Работа с SQLModel и миграциями
- JWT авторизация
- Валидация данных и типизация
- Проектирование структуры приложения

---

## 📄 Лицензия

Проект создан для учебных целей и открыт для всех желающих разобраться в FastAPI.

---
