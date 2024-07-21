# python
# This project has Flask app with Keycloak. This POC tries to set up a keycloak server and client flask app to access keycloak in docker

Under # test folder -> you can run keycloak with a separate postgres DB using the docker-compose file in it both within same docker network.

Under # keycloak-setup folder, you can run keycloak server with configurable database. Ensure the timescaledb that is configured is up and running. check the docker network of the db and set it in the network of keycloak, so both keycloak and db are in same docker network. Also ensure to create/check keycloak schema present in configured DB.

Also keycloak-data has json that helps to configure keycloak settings automatically. its disabled in docker-compose by default. feel free to enable and try with any keycloak configuration.

# app.py
This is flask app to access keycloak. try to change the url, client informations which are hardcoded in it for test purposes.

# check.py
This is quick test script for keycloak connectivity

# docker-compose - flask
This will be launched in separate docker network but can access keycloak via configuration in app.py

