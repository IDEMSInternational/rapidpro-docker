FROM amazon/dynamodb-local:3.1.0
RUN mkdir /home/dynamodblocal/data
HEALTHCHECK --interval=10s --timeout=5s CMD curl http://localhost:6000/
CMD ["-jar", "DynamoDBLocal.jar", "-sharedDb", "-dbPath", "/home/dynamodblocal/data", "-port", "6000"]
