1.  Арефьев Вениамин Адреевич, 205 группа
2.  python 3.9+ (можно понизить до 3.8, заскоментировав 218 строку и закоментировав 219, то тогда некоторые ошибки будут обрабатываться неправильно)
    networkx - парсинг, хранение и запись графов. 
    matplotlib - визуализация графов (установит также дочерние зависимости)
3.  sudo pip install matplotlib
    sudo pip install networkx
4.  python main.py -h
    Данная строка выведет:
    
    usage: main.py [-h] [-t T] [-k {1,2}] [-st {0,1}] [-sp {0,1}]

    optional arguments:
      -h, --help            show this help message and exit
      -t T, -topology T     This is filename of topology
      -k {1,2}, -criteria {1,2}
                            This is number of criteria, should we use k1(1) or k2+k1(2)
      -st {0,1}, -save_top {0,1}
                            Save built spanning tree to new_<name>.gml
      -sp {0,1}, -save_pic {0,1}
                            Save built SDN to <name>.png
    Обязательно указание файла через флаг -t (with extension ".gml" or ".graphml" (is not case sensivity)) 
    Если не указан критерий, то выбирается k2. По умолчанию ни картинка, ни новая топология не сохраняется.
    При неправильном вводе каких-либо флагов программа выводит сообщение об ошибке и завершается с кодом 0(если работает строка под номером 218)
    Во входных данных обязаны быть указаны геоданные(Longitude & Latitude), возрастающие id(start =  0), и не повторяющиеся рёбра
5.  На сайте(http://www.topology-zoo.org/dataset.html) порой не совпадают топологии в различных форматах и очень часто присутствуют пустые вершины и кратные рёбра, столкнулся с данными проблемой при тестировании.
6.  Тестирование всех случаев проводилось на WSl 2 Ubuntu 20.04.2 LTS.  