# Технотрек 2018
## 1 семестр
В этом репозитории лежат файлы и коды, 
созданные в рамких программы "Технотрек" на 1 семестре.
### Запуск
Здесь есть несколько программ, и для каждой из них - отдельная 
инструкция для запуска. Для начала:
```bash
git clone https://github.com/alekseik1/tt-1sem-backend
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```
Поддерживается запуск через _Docker_:
```bash
docker run -p 5000:5000 tt-test
```
#### Двусвязный список
Запуск тестов производится командой:
```bash
python -m unittest tests/test_DoubleLinkedList.py
```
Сами файлы лежат в папке `app/double_linked_list.py`
