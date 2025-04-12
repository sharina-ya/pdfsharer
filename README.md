- запуск: daphne pdfsharer.asgi:application --bind 0.0.0.0 --port 8000
1) локальная(только из моего пк): http://127.0.0.1:8000/
2) щмщ:http://192.168.95.246:8000/


чтобы работал веб сокет надо пкм на psfsharer -> mask directory as -> sources rout

работа с докером
1) открыть докер
2) проверить что WSL 2 включена
3) перейти в PowerShell в приложение
4) docker run -d -p 6379:6379 redis
5) docker ps
6) docker exec -it <ID_КОНТЕЙНЕРА> redis-cli
7) ping
8) получить PONG - значит все правильно
9) в пайчарме: daphne pdfsharer.asgi:application --bind 0.0.0.0 --port 8000
