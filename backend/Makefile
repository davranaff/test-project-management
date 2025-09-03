BACKEND=backend

migrate:
	docker compose exec $(BACKEND) python manage.py migrate

makemigrations:
	docker compose exec $(BACKEND) python manage.py makemigrations

superuser:
	docker compose exec -it $(BACKEND) python manage.py createsuperuser

shell:
	docker compose exec -it $(BACKEND) python manage.py shell

logs:
	docker compose logs -f $(BACKEND)

up:
	docker compose up --build -d

down:
	docker compose down
