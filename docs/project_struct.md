# Project struct

## Концепция

Реализовать MVP для отправки и получения сообщений из docker-контейнера с frontend.

## Используемый стек технологий

- Python 3.10
    - SqlAlchemy
    - FastAPI
    - SocketIO
    - Celery
    - AioPika
- Java Script
    - React
- PostgreSQL
- Redis
- RabbitMQ
- Nginx
- Docker
    - Compose

## Основные компоненты системы

**Frontend** - клиентское приложение.

**BFF** - пользовательский API открытый в интернет.

**Оркестратор** - занимается управлением контейнерами, в которых работают пользователи.

**Worker** - cron задачи на очистку ресурсов.

## Схема взаимодействия

```mermaid
flowchart LR
    nginx["Nginx"]
    front["Frontend"]
    bff["Back for front"]
    orch["Orchestrator"]
    worker["Worker"]
    rabb[("RabbitMQ")]
    post[("PostgreSQL")]
    docker[("Docker")]
    redis[("Redis")]

    nginx <--> front
    nginx <--> bff
    bff --> post
    bff --> rabb
    rabb --> bff
    rabb --> orch
    orch --> rabb
    orch --> docker
    worker --> redis
    worker --> post
    worker --> rabb
```
