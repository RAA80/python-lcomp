## python-lcomp ##

Библиотека для работы с АЦП/ЦАП фирмы [ЛКАРД](https://www.lcard.ru/products/external/about)

### Установка для Linux: ###

-   Распаковать драйвер **lcomp** для Linux
-   Сделать make
-   Скопировать получившийся файл **liblcomp.so** в папку **libs** библиотеки **python-lcomp**
-   Скопировать папку **addon** из библиотеки **python-lcomp** в папку драйвера **lcomp** рядом с папкой **include**
-   Сделать make
-   Скопировать получившийся файл **libwlcomp.so** в папку **libs** библиотеки **python-lcomp**
-   Установить библиотеку **python-lcomp**

### Установка для Windows: ###

-   Скопировать библиотеки **lcomp.dll**, **lcomp64.dll**, **wlcomp.dll** и **wlcomp64.dll** из установленного драйвера **lcomp** в папку **libs** библиотеки **python-lcomp**
-   Установить библиотеку **python-lcomp**
