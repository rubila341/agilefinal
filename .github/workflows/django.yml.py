name: Django CI

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      mysql:
        image: mysql:5.7
        env:
          MYSQL_ROOT_PASSWORD: root
          MYSQL_DATABASE: DJANGO_AGILE_APP_04_10
          MYSQL_USER: root
        ports:
          - 3306:3306
        options: >-
          --health-cmd "mysqladmin ping -h localhost -u root --password=root"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
    - name: Checkout code
      uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest

    - name: Run tests with pytest
      env:
        SECRET_KEY: ${{ secrets.SECRET_KEY }}
        DB_NAME: DJANGO_AGILE_APP_04_10
        DB_USER: root
        DB_PASSWORD: root
        DB_HOST: localhost
        DB_PORT: 3306
        ALLOWED_HOSTS: 127.0.0.1,localhost
        DJANGO_SETTINGS_MODULE: 'agile_app.settings'
      run: |
        pytest apps/test/test_users_api.py  # Запуск тестов в файле test_users_api.py
