#!/bin/sh
docker-compose -p functional-tests -f tests/functional/docker-compose.yaml up -d --build functional-tests

echo "WAIT DOCKER functional-tests!!!"
exit_code=$(docker wait functional-tests)

echo "STATUS CODE!!!"
echo ${exit_code}

if [ $exit_code != "0" ]
then
    docker logs -f -n 150 functional-tests
fi

exit ${exit_code}
