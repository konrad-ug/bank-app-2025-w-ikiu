[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/IwJY4g24)
# Bank-app

## Author:
name: Wiktoria

surname: Chełmińska

group: 1

## How to start the app

Upewnij się, że masz aktywne środowisko wirtualne i zainstalowane biblioteki:

```python
pip install -r requirements.txt
```

Uruchom serwer Flask:

Windows (PowerShell):

```python
$env:FLASK_APP = "app/api.py"
$env:PYTHONPATH = "."
flask run
```

Linux/Mac/Bash:

```python
export FLASK_APP=app/api.py
export PYTHONPATH=.
flask run
```

## How to execute tests

Unit Tests (Testy Jednostkowe):

Nie wymagają uruchomionego serwera.


```python
python -m pytest tests/unit
```


API Tests (Testy Integracyjne):

Wymagają uruchomionego serwera (flask run w tle).

```python
python -m pytest tests/api
```

Performance Tests (Testy Wydajnościowe):

Sprawdzają czas odpowiedzi endpointów. Wymagają uruchomionego serwera.

```python
python -m pytest tests/perf
```


BDD Tests (Scenariusze Gherkin):

Testy behawioralne. Wymagają uruchomionego serwera.

```python
behave
```
