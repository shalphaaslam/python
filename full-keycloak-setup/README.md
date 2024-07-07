## This is the keycloak configuration setup for the version 24.0.2(latest)

Folder - jspolicy

1. There is wicloudpolicy.js custom script that defines the installation customer attribute against the resource name validation
2. create jar of the script to be deployed in keycloak using command below
    "jar cvf policy.jar META-INF wicloudpolicy.js"
    Ensure the structure having META-INF and keycloak-script.json in it along with iwicloudpolicy.js in the jar
3. copy the created jar to the folder called "policy" and that is configured in Dockerfile to be picked up while deploying the jar

Folder - keycloak-data

1. This folder has the realm configuration of wicloud in json which is passed to keycloak in runtime using docker-compose.yml file
we can edit it to add, update the configuration of realm 

Note: keycloak Latest version is used 24.0.2 – Url should not include /auth
For example: http://localhost:8080/admin/master/console/

## To execute and up the keycloak at http://localhost:8080/:
1. Make sure to create keycloak schema under wicloud
2. cd into the folder /full-keycloak-setup, do sudo docker-compose build
3. do sudo docker-compose up
4. keycloak should be up and created its tables in the keycloak schema created above.


## To verify whether keycloak uses configured DB:
1. check the schema keycloak is created already in the DB configured in docker-compose.yml. if not, create a schema keycloak under wicloud
2. After running keycloak, exec "docker exec -it 9c82f7c44a97 /bin/bash"
3. In bash, exec "/opt/keycloak/bin/kc.sh show-config" 
It should show the DB configuration imported from docker-compose.yaml. If its "dev-file" instead, then its using inmemory H2 DB.

## Authorization Services Enablement

### To discover Authorization urls for the keycloak :
curl http://192.168.160.1:8080/realms/master/.well-known/openid-configuration

## Setup steps:
1. create userProfile attribute in realm settings and enable uma in realm settings(verify that service_account tab has uma_protection). this user attribute can be multi-valued. however, in that case, changes required in our ,custom javascript policy.
2. add value to the attribute for the user and make it mandatory
3. Ensure authorization enabled for the client(resource-server) and in Authorization tab, create resources ins1 with uma enabled
4. create policy with the newly listed one that is deployed by us previously
5. create permission for resourceType and policy created before and save
6. Ensure to add mapper for the user attribute “resourceType” created, so its reflected in user attributes(add in clientscope, under dedicated     scope and by configuration, user attribute)
7. Now, evaluate the policy in evaluate tab
8. enable full scope in client scope – decidated scopes (optional but not reqd for authorization to run specifically)
   
       
## Keycloak Authorization services test using curl

#1. Make sure UMA is enabled for resource-server(which is client "account" and in the realm settings)

#2. Next, get access token by standard auth flow only to be used in next step. I used postman to get it.
  
#3. To get authorization claim in token which rpt(the access token with permissions is called a Requesting Party Token or RPT for short), u need to first get access token and then call like below:
curl -X POST \
  http://172.26.0.1:8080/realms/master/protocol/openid-connect/token \
  -H "Authorization: Bearer  [access-token]" \
  --data "grant_type=urn:ietf:params:oauth:grant-type:uma-ticket" \
  --data "audience=account"
  
 #4. To evaluate permission
 curl -X POST \
  http://172.26.0.1:8080/realms/master/protocol/openid-connect/token \
  -H "Authorization: Bearer [access-token]" \
  --data "grant_type=urn:ietf:params:oauth:grant-type:uma-ticket" \
  --data "audience=account" \
  --data "permission=ins1" 
  
 when you mentioned mulitple installation, a rpt token provided but when only one permission claim with resource provided if user has it, it gets authenticated or access denied response comes.
 
 #5. Accessing resources - CRUD[This needs uma_protection role which is only available to resource-server(account) and not user]
 First login with client credential:
curl -X POST \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d 'grant_type=client_credentials&client_id=account&client_secret=NEuQmakWzsV7v0R7rcBA2zYKEfnBgah4' \
    "http://172.26.0.1:8080/realms/master/protocol/openid-connect/token"
 
 and then list the resources like curl below 
curl -X GET http://172.26.0.1:8080/auth/realms/wicloud/authz/protection/resource_set \
    -H "Authorization: [access-token]"

output:
["accf926c-4160-478b-a3a8-c9cc26334bff","53cce1b6-f90a-4620-a70f-b8b470c4c098","832439c9-ce49-4f9f-afb7-1c2915d655ce"]

## To access protection APIs to create, update, delete resources in keycloak: 
Examples:
1. Fetch the access token using client credentials only (since it only has UMA protection role and not applicable to user)
2. exec to create resource having user as owner:
curl -X POST \
  http://172.26.0.1:8080/realms/master/authz/protection/resource_set \
  -H 'Authorization: Bearer [access-token]' \
  -H 'Content-Type: application/json' \
  -d '{
     "name":"admin Resource",
     "owner": "admin",
     "ownerManagedAccess": true
  }'

3. exec to create resource having resource-server as owner:(resource_scopes are optional)
  curl -X POST \
  http://172.26.0.1:8080/auth/realms/master/authz/protection/resource_set \
  -H 'Authorization: Bearer [access-token]' \
  -H 'Content-Type: application/json' \
  -d '{
     "name":"wicloud-installation121",
     "type":"installation",
     "icon_uri":"http://www.example.com/icons/sharesocial.png",
     "resource_scopes":[
         "read-public",
         "post-updates",
         "read-private",
         "http://www.example.com/scopes/all"
      ]
  }'