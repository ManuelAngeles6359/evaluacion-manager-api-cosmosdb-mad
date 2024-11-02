from azure.cosmos import CosmosClient, exceptions, PartitionKey

COSMOS_ENDPOINT = 'https://acdbmadnosql.documents.azure.com:443/'
COSMOS_KEY = 'RYX5l6UbJhgYcOwVbMPqd4HlLTfGrDkdPwSOKkEjwn8RLTGzNOu9r1656gGMp56QG6lHRRWn4oypACDbk3MXZg=='

DATABASE_NAME = 'GestorProyectosDB'
CONTAINER_NAME_USUARIOS = 'Usuarios'
CONTAINER_NAME_PROYECTOS = 'Proyectos'

# Inicializar el cliente de Cosmos DB
client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)

# Crear o obtener la base de datos
try:
    database = client.create_database_if_not_exists(id=DATABASE_NAME)
except exceptions.CosmosResourceExistsError:
    database = client.get_database_client(DATABASE_NAME)

# Crear o obtener el contenedor de usuarios
try:
    container_usuarios = database.create_container_if_not_exists(
        id=CONTAINER_NAME_USUARIOS,
        partition_key={'paths': ['/id'], 'kind': 'Hash'},
        offer_throughput=400
    )
except exceptions.CosmosResourceExistsError:
    container_usuarios = database.get_container_client(CONTAINER_NAME_USUARIOS)


# Crear o obtener el contenedor de proyectos
try:
    container_proyectos = database.create_container_if_not_exists(
        id=CONTAINER_NAME_PROYECTOS,
        partition_key={'paths': ['/id'], 'kind': 'Hash'},
        offer_throughput=400
    )
except exceptions.CosmosResourceExistsError:
    container_proyectos = database.get_container_client(CONTAINER_NAME_PROYECTOS)