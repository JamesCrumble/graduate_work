dc_prod:
	docker-compose -p search_service_prod down
	docker-compose -p search_service_prod down --volumes
	docker-compose -p search_service_prod up -d --build

dc_prod_kill:
	docker-compose -p search_service_prod down
	docker-compose -p search_service_prod down --volumes

dc_dev:
	docker-compose -f docker-compose-dev.yml down
	docker-compose -f docker-compose-dev.yml down --volumes
	docker-compose -f docker-compose-dev.yml up

functional_tests:
	docker-compose -p functional-tests -f ./tests/functional/docker-compose.yaml run --build --rm functional-tests || (docker logs —tail 150 functional-tests && exit 1;)

functional_tests_remove_artifacts:
	docker-compose -p functional-tests down
