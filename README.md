# Django LR Server

This container fetches the latest prices for a given list of cryptocurrencies periodically from the DefiLlama price API and stores them in an SQLite database. A GraphQL API is provided to query the prices and add new cryptocurrencies to the database. The price update task can easily be configured to run at different intervals.

**_The admin username/pw is admin/admin._**

### Prerequisities

In order to run this container you'll need Docker and Docker Compose installed.

Docker:

- [Windows](https://docs.docker.com/windows/started)
- [OS X](https://docs.docker.com/mac/started/)
- [Linux](https://docs.docker.com/linux/started/)

Docker Compose:

- https://docs.docker.com/compose/install/.

### Usage

#### Starting the Project

To start the project, navigate to the directory containing the `docker-compose.yml` file and run:

```shell
docker-compose up
```

To open a shell inside the running Docker container, run:

```shell
docker exec -it django_lr_server bash
```

#### Environment Variables

- `CELERY_BROKER` - Redis broker URL (default: redis://redis:6379/0)
- `CELERY_BACKEND` - Redis backend URL (default: redis://redis:6379/0)

#### Volumes

- `/app` - Application code

#### Useful File Locations

- `/app/price_app/config.py` - Specify the cryptocurrencies to periodically fetch prices for and the cron interval used for the price update Celery Beat task.

- `/app/price_app/tasks.py` - Celery tasks
- `/app/lr_server/settings.py` - Django settings

## Built With

- Python 3.10
- Django 5.1.3
- Celery 5.4.0
- django-redis 5.4.0
- django-graphene 3.2.2
- django-celery-beat 2.7.0

## License

This project has no license.
