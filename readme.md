
# Amazon Rating Prediction API & MLOps Pipeline

Этот проект представляет собой сервис машинного обучения для предсказания рейтинга товаров Amazon (от 1 до 5 звезд) на основе текстовых отзывов. 


## Запуск сервиса

```bash
docker compose up -d
```

*Интерактивная документация Swagger доступна по адресу `http://localhost:8000/docs`.*



---

## Развертывание инфраструктуры

Для локальной разработки, переобучения модели и прогона CI/CD пайплайнов в проекте предусмотрен файл инфраструктуры `docker-compose.infra.yml`.

### 1. Первичная настройка доступов

Перед первым запуском инфраструктуры вы можете задать собственные логин и пароль для S3-хранилища (MinIO).

1. Откройте файл `docker-compose.infra.yml`.
2. В блоке сервиса `minio` найдите переменные окружения и измените их на свои:
   ```yaml
   environment:
     MINIO_ROOT_USER: YOUR_LOGIN      
     MINIO_ROOT_PASSWORD: YOUR_PASSWORD 
   ```

### 2. Запуск сервисов
Поднимите CI/CD сервер (Jenkins) и локальное S3-хранилище (MinIO):

```bash
docker-compose -f docker-compose.infra.yml up -d
```

### 3. Авторизация в Jenkins
При первом запуске Jenkins генерирует временный пароль администратора. Чтобы его узнать, выполните команду в терминале:
```bash
docker exec local_jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```
Скопируйте полученный пароль, перейдите по адресу **`http://localhost:8080`** и вставьте его для завершения установки Jenkins.

### 4. Привязка DVC к локальному S3 (MinIO)
Чтобы ваш локальный DVC мог скачивать и загружать модели в поднятый MinIO, ему нужно передать логин и пароль, которые вы задали в Шаге 1.

```bash
dvc remote modify --local myminio access_key_id ваш_логин
dvc remote modify --local myminio secret_access_key ваш_пароль
dvc remote modify --local myminio endpointurl http://localhost:9000
```
