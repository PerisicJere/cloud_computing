docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit
exit_code=$?
docker-compose -f docker-compose.test.yml down
exit $exit_code