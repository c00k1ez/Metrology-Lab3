# Как этим пользоваться

Добро пожаловать, путник!

Земля тебе пухом, если приходится смотреть это. 

Итак, как этим чудом пользоваться:

**Шаг первый**: создайте папку ```data``` в корне проекта и положите туда 4 своих файла с измерениями (ну или просто в корень проекта, не принципиально).

**Шаг второй**: установите нужные зависимости из файла ```requirements.txt``` следующией командой:

```pip[3] install -r requirements.txt```

Сразу поясню - важное условие: ```python>=3.6``` . В некоторых системах у питона (соответственно и у pip) может быть разный алиас - либо ```python```, либо ```python3``` (для pip аналогично), поэтому я буду писать ```python[3]``` и  ```pip[3]```.

**Шаг третий**: запустите следующую команду для файлов **первых двух** выборок.

```python[3] delete_misses.py --file_name <путь_до_файла.txt> --norm_data [--use_dip_test]```

Аргумент в ```[]``` не обязателен, плюс он полноценно и не работает :-)

Вообще DIP test - проверка распределния на унимодальность, если интересно - можете загуглить.

Этот скрипт:

* считает статистики по сырой выборке;
* рисует гистограмму по сырой выборке;
* удаляет промахи по правилу трех сигм (да, да, по идее оно работает только для нормального распределения, по как-то плевать, т.к предложеный тест Граббса для таких больших выборок не рассчитан);
* выводит статистику по новой выборке;
* рисует гистограмму подчищенной выборки для выбранной гипотезы;
* выводит минимальное, максимальное, рассчетное значение хи-квадрат;
* если есть флаг ```--norm_data``` (а он **должен быть** для первых двух файлов), нормализует данные по формуле (x - min(x)) / (max(x) - min(x)).

**Шаг четвертый**: для оставшихся двух файлов запустите команду:

```python[3] delete_misses.py --file_name <путь_до_файла.txt> [--use_dip_test]```

Если у вас в каком-то из файлов хи-квадрат попадает в диапазон, делайте пункры по лабе.

Если нет - удачи :-)

Файлы для KS теста: ```<путь_до_первого_файла.txt.new.norm>``` и ```<путь_до_второго_файла.txt.new.norm>```.