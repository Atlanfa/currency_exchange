Инструкция по запуску
После скачивания файлов приложения  из GitHub на сервер, нужно убедиться что на сервер установлены python нужной версии(у меня это 3.9) после этого  выполнить в терминале команду pip install -r requirements.txt. После этого командой screen -S currency_exchange_bot python currency_exchange_bot.py запустить программу в отдельном скрине и нажать Ctrl + A , Ctrl + D для того что бы выйти из скрина. Все программа запущена и работает.
Для проверки бота можна использовать следуюшие команды:

/list
/exchange 10 USD to CAD
/history USD/CAD
