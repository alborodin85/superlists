Обеспечение работы нового сайта
===============================
## Необходимые пакеты
* nginx
* Python 3.9, 3.10
* virtualenv + pip
* Git

Например, в ubuntu:
sudo apt-get install nginx git python3 python3-venv

## Конфигурация виртуального узла nginx
* см. nginx.template.conf
* заменить SITENAME, например, на superlist-staging.it5.su

## Служба systemd
* см. gunicorn-systemd.template.service
* заменить SITENAME, например, на superlist-staging.it5.su

## Структура папок
Если допустить, что есть учетная запись пользователя в /home/username
/home/username
    sites
        SITENAME
            database
            source
            static
            virtualenv
