# Определяем имя виртуальной среды
VENV = srdEnv

# Определяем путь к Python и pip в виртуальной среде
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

pkgList:
	$(PIP) freeze > requirements.txt\

# Цель по умолчанию
all: makeVenv install run

# Создание виртуальной среды
makeVenv:
	python3 -m venv $(VENV)

# Установка зависимостей
install:
	$(PIP) install -r requirements.txt

# Запуск скрипта
run:
	$(PYTHON) main.py

# Очистка виртуальной среды
clean:
	rm -rf $(VENV)