### Полная инструкция по установке проекта с использованием `venv`, `poetry`, и скачиванием с GitHub

#### 1. Установка Git

Для того чтобы скачать проект с GitHub, необходимо установить Git.

- **Linux** (Ubuntu/Debian):
    ```bash
    sudo apt update
    sudo apt install git
    ```

- **Windows**:
    1. Скачайте [установщик Git](https://git-scm.com/download/win).
    2. Запустите установщик и следуйте инструкциям.

После установки Git проверьте, что он работает, выполнив команду:

```bash
git --version
```

#### 2. Скачивание проекта с GitHub

1. Клонируйте репозиторий проекта с GitHub:
    ```bash
    git clone https://github.com/Mozheykin/GroupBotScheduler.git
    ```

2. Перейдите в папку с проектом:
    ```bash
    cd GroupBotScheduler
    ```

#### 3. Установка pyenv и Python 3.12

Следуйте шагам по установке pyenv и Python 3.12, как указано выше.

#### 4. Создание виртуального окружения с `venv`

1. Создайте виртуальное окружение с `venv`:
    ```bash
    python3 -m venv venv
    ```

2. Активируйте виртуальное окружение:

   - На **Linux**:
     ```bash
     source venv/bin/activate
     ```

   - На **Windows**:
     ```bash
     venv\Scripts\activate
     ```

#### 5. Установка зависимостей через `pip` и `poetry`

1. Установите зависимости через `pip`:
    ```bash
    pip install -r requirements.txt
    ```

2. Установите зависимости через Poetry:
    ```bash
    poetry install
    ```

#### 6. Создание файла `.env`

1. Создайте файл `.env` в корне проекта:
    ```bash
    touch .env
    ```

2. Добавьте в него токен бота:
    ```
    BOT_TOKEN=your_telegram_bot_token
    ```

#### 7. Запуск проекта

1. Активируйте виртуальное окружение (если оно не активно):
    ```bash
    source venv/bin/activate  # Linux
    venv\Scripts\activate     # Windows
    ```

2. Запустите проект:
    ```bash
    python main.py
    ```