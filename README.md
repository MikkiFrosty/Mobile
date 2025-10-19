# Mobile Wikipedia — демо-проект по автоматизации (Mobile)
> Тестируемое приложение: Wikipedia (Android)

<p align="center">
  <img src="images/mobile_wiki_banner.png" alt="Wikipedia Mobile banner" width="900">
</p>

## Содержание
> ➠ [Технологический стек](#технологический-стек)  
> ➠ [Покрытый функционал](#покрытый-функционал)  
> ➠ [Jenkins](#jenkins)  
> ➠ [BrowserStack](#browserstack)  
> ➠ [Запуск из терминала](#запуск-из-терминала)  
> ➠ [Allure Report](#allure-report)  
> ➠ [Пример видео прохождения тестов](#пример-видео-прохождения-тестов)

## Технологический стек

<p  align="center">
<img src="images/logos/python-original.svg" width="50" title="Python"> <img src="images/logos/pytest.png" width="50" title="Pytest"> <img src="images/logos/intellij_pycharm.png" width="50" title="PyCharm"> <img src="images/logos/selene.png" width="50" title="Selene"> <img src="images/logos/selenium.png" width="50" title="Selenium"> <img src="images/logos/selenoid.png" width="50" title="Selenoid"> <img src="images/logos/jenkins.png" width="50" title="Jenkins"> <img src="images/logos/allure_report.png" width="50" title="Allure Report"> <img src="images/logos/github.png" width="50" title="GitHub">
</p>

Автотесты написаны на <code>Python + Pytest</code> с использованием <code>Appium</code> для автоматизации мобильного приложения.  
Запуски выполняются в <code>BrowserStack App Automate</code> (реальные устройства) и локально (эмулятор).  
Сборки идут через <code>Jenkins</code>, отчётность — <code>Allure Report</code>.

## Покрытый функционал
> Мобильные тесты приложения **Wikipedia Android**

- [x] **Онбординг:** `test_onboarding_flow` — проверка экранов и переходов  
- [x] **Поиск и открытие статьи:** `test_open_first_article` — выдача по запросу и переход к первой статье  
- [x] **Подсказки поиска:** `test_wiki_search_suggest` — отображение suggest-вариантов при вводе

## Jenkins
> (пример ссылки на пайплайн) `https://jenkins.autotests.cloud/job/Mobile%20Test%20QA%20GURU/`

<p align="center">
  <img src="images/jenkins_runs.png" alt="Jenkins: список запусков" width="900">
</p>
<p align="center"><em>Параметризованные сборки и ссылка на Allure после прогона</em></p>

### Параметризованный запуск (пример)
В <code>Build with Parameters</code> можно задать: тип устройства (реальное/эмулятор), версию Android и региональные настройки.  
После выполнения сборки ссылка на Allure прикрепляется к задаче.

## BrowserStack

Тесты запускаются на реальных устройствах в <code>BrowserStack App Automate</code>.  
Для каждого теста доступны видео, скриншоты и логи устройства.

## Запуск из терминала

Локально:
```bash
python -m venv .venv && source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest -m "mobile" -q
```

Локальная генерация отчёта:
```bash
allure serve allure-results
```

## Allure Report
> (пример ссылки на отчёт) `https://jenkins.autotests.cloud/job/Mobile%20Test%20QA%20GURU/55/allure/`

<p align="center">
  <img src="images/allure_overview.png" alt="Allure Report: успешные тесты" width="800">
</p>

## Пример видео прохождения тестов

<p align="center">
  <img src="images/mobile_wiki_tests.gif" alt="Mobile Wikipedia autotests run" width="500">
</p>
