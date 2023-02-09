## Getting Starting

Bring up the stack with docker compose, ensure the db is created and then create a system admin account

```shell
docker-compose up
flask provision-db
flask create-admin system@system.com passwd system
```

## UI Client

The UI client is located in the `client` directory. It was built using React and TypeScript. To run the client in
development mode:

```shell
cd client
npm run start
```

This will start the npm server on `localhost:3000`. The project is configured to port-forward to `127.0.0.1:5000` which
is the flask server.
