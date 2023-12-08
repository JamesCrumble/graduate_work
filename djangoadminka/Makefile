dc_prod:
	docker-compose -p djangoadminka_prod down
	docker-compose -p djangoadminka_prod down --volumes
	docker-compose -p djangoadminka_prod up -d --build

dc_prod_kill:
	docker-compose -p djangoadminka_prod down
	docker-compose -p djangoadminka_prod down --volumes

init_dev:
	pip install -r src/requirements.txt
