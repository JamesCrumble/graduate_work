##################################################
# Inside auth project make refs                  #
##################################################

start_app:
	make -C src/ start_app

install_app:
	make -C src/ install_app

migrate:
	make -C src/ migrate

##################################################
# Prod building                                  #
##################################################

docker_prod:
	docker-compose -p auth_service_prod up -d --build

docker_prod_kill:
	docker-compose -p auth_service_prod down
	docker-compose -p auth_service_prod down --volumes

generate_prod_keys:
	openssl genrsa -out ./secrets/priv_key_prod.pem 2048
	openssl rsa -in ./secrets/priv_key_prod.pem -outform PEM -pubout -out ./secrets/pub_key_prod.pem
	cp ./secrets/pub_key_prod.pem ./../admin/secrets/
	cp ./secrets/pub_key_prod.pem ./../search/secrets/

delete_prod_keys:
	rm -f ./secrets/pub_key_prod.pem ./secrets/priv_key_prod.pem ./../admin/secrets/pub_key_prod.pem ./../search/secrets/pub_key_prod.pem

##################################################
# Dev docker control                             #
##################################################

docker_dev:
	docker-compose -p auth_service_dev down
	docker-compose -p auth_service_dev -f ./docker-compose-dev.yml build
	docker-compose -p auth_service_dev -f ./docker-compose-dev.yml up -d

docker_dev_kill:
	docker-compose -p auth_service_dev down
	docker-compose -p auth_service_dev down --volumes

init_dev:
	pip install -r src/requirements-dev.txt
	pip install -r src/requirements.txt
	pip install -r tests/functional/requirements.txt
	pre-commit install

dev_auth:
	cd ${PWD}/src && alembic upgrade head && python -m run

pre-commit:
	pre-commit run --all-files

generate_dev_keys:
	openssl genrsa -out ./secrets/priv_key_dev.pem 2048
	openssl rsa -in ./secrets/priv_key_dev.pem -outform PEM -pubout -out ./secrets/pub_key_dev.pem
	cp ./secrets/pub_key_dev.pem ./../admin/secrets/
	cp ./secrets/pub_key_dev.pem ./../search/secrets/

delete_dev_keys:
	rm -f ./secrets/pub_key_dev.pem ./secrets/priv_key_dev.pem ./../admin/secrets/pub_key_dev.pem ./../search/secrets/pub_key_dev.pem

##################################################
# TESTS DOCKER CONTROL                           #
##################################################

functional_tests:
	docker-compose -p functional-tests -f ./tests/functional/docker-compose.yml run --build --rm functional-tests || (docker logs —tail 150 functional-tests && exit 1;)

func_tests_up:
	docker-compose -p functional-tests -f tests/functional/docker-compose.yml up --build --exit-code-from functional-tests

tests_auth_build:
	docker-compose -p functional-tests -f tests/functional/docker-compose.yml up --build test-auth

functional_tests_remove_artifacts:
	docker-compose -p functional-tests down

run_tests_with_sh:
	chmod +x tests/build-test.sh
	tests/build-test.sh

run_tests_local:
	cd ${PWD}/tests/functional && python -m main
