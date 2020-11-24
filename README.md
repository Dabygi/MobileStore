![Окошко из приложения](https://github.com/Dabygi/MobileStore/blob/master/mobile-store-online.png?raw=true)
# MobileStore - репозиторий интернет-магазина электроники на Django 3.

Установка (для пользователей операционных систем семейства MacOs/Linux):

1. Открыть терминал или консоль и перейти в нужную Вам директорию
2. Прописать команду git clone git@github.com:Dabygi/MobileStore.git

3. Если Вы используете https, то: https://github.com/Dabygi/MobileStore.git

4. Прописать следующие команды:

  - python3 -m venv ДиректорияВиртуальногоОкружения
  - source ДиректорияВиртуальногоОкружения/bin/activate
  - Перейти в директорию MobileStore
  - pip install -r requirements.txt
  - python manage.py migrate


5. Запустить сервер - python manage.py runserver

6. Не забудьте создать директорию media, куда будут сохраняться изображения для товара
