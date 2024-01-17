## python-lcomp ##

Библиотека для работы с АЦП/ЦАП фирмы [ЛКАРД]

### Установка для Linux: ###

-   Распаковать драйвер [lcomp_linux.tgz]
-   Сделать `make`
-   Скопировать получившийся файл `liblcomp.so` в папку `lcomp/libs` библиотеки **python-lcomp**
-   Скопировать папку `addon` из библиотеки **python-lcomp** в папку распакованного драйвера `lcomp_linux.tgz` рядом с папкой `include`
-   Сделать `make`
-   Скопировать получившийся файл `libwlcomp.so` в папку `lcomp/libs` библиотеки **python-lcomp**
-   Установить библиотеку **python-lcomp**

### Установка для Windows: ###

-   Скопировать библиотеки `lcomp.dll`, `lcomp64.dll`, `wlcomp.dll` и `wlcomp64.dll` из установленного драйвера [lcomp] (по умолчанию в папке `C:\Program Files (x86)\LCard\LIBRARY\BIN`) в папку `lcomp/libs` библиотеки **python-lcomp**
-   Установить библиотеку **python-lcomp**

[ЛКАРД]: https://www.lcard.ru/products/external/about
[lcomp_linux.tgz]: https://www.lcard.ru/download/lcomp_linux.tgz
[lcomp]: https://www.lcard.ru/download/lcomp.exe
