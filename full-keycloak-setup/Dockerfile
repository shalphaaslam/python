# Use the latest Keycloak image as the base
# works fine for Keycloak version 24.0.2
FROM quay.io/keycloak/keycloak:latest as builder

# Copy the JavaScript policy JAR file to the providers directory
COPY ./policy /opt/keycloak/providers/
COPY ./keycloak-data/ /opt/keycloak/data/import/
RUN /opt/keycloak/bin/kc.sh build

# Copy the realm configuration JSON file
COPY ./keycloak-data/master.json /tmp/realm-master.json

# Enable health and metrics support
ENV KC_HEALTH_ENABLED=true
ENV KC_METRICS_ENABLED=true

# Configure a database vendor
ENV KC_DB_SCHEMA=keycloak
ENV KC_DB=postgres
ENV KC_DB_USERNAME=wicloud
ENV KC_DB_NAME=wicloud
ENV KC_DB_PASSWORD=4rts2-fgbtr-asvrs-4663g
# ENV KC_HOSTNAME=ilcs-cloud-db
ENV KC_DB_URL=jdbc:postgresql://ilcs-cloud-db:5432/wicloud

WORKDIR /opt/keycloak

# for demonstration purposes only, please make sure to use proper certificates in production instead
RUN keytool -genkeypair -storepass password -storetype PKCS12 -keyalg RSA -keysize 2048 -dname "CN=server" -alias server -ext "SAN:c=DNS:localhost,IP:127.0.0.1" -keystore conf/server.keystore
RUN /opt/keycloak/bin/kc.sh build

FROM quay.io/keycloak/keycloak:latest
COPY --from=builder /opt/keycloak/ /opt/keycloak/

RUN /opt/keycloak/bin/kc.sh show-config

ENTRYPOINT ["/opt/keycloak/bin/kc.sh"]