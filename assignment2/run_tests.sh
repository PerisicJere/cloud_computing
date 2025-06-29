#!/bin/bash

docker build -f Dockerfile.test -t flask-api-tests .

if [ $? -ne 0 ]; then
    echo "Failed to build test Docker image"
    exit 1
fi

echo "Running tests..."
docker run --rm flask-api-tests

TEST_EXIT_CODE=$?

if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "All tests passed!"
else
    echo "Tests failed!"
fi

exit $TEST_EXIT_CODE