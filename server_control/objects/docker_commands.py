import docker
import docker.errors
from Sophia.secret_store.config import *


class DockerApi:

    def __init__(self, name):
        self.name = name
        self.client = docker.from_env()
        self.server_names = [
           """ 'plex',
            'terraria',
            'mongo',
            'rabbit'"""
        ]

    def start_terraria(self):
        pass

    def start_plex(self):
        try:
            self.client.images.pull(repository='plexinc/pms-docker:latest')
            self.client.containers.run("plexinc/pms-docker",
                                       detach="True",
                                       name="plex",
                                       hostname="Mike",
                                       environment=[
                                           "TZ=America/New_York",
                                           "PLEX_CLAIM=claim-ACoXvQnkZ52j9bpLnu3L"
                                           "ADVERTISE_IP=" + docker_ip
                                       ],
                                       volumes=[docker_config_file + ':/config',
                                                docker_config_file + ':/media',
                                                docker_config_file + ':/transcode'],
                                       ports={
                                           '32400/tcp': 32400,
                                           '3005/tcp': 3005,
                                           '8324/tcp': 8324,
                                           '32469/tcp': 32469,
                                           '1900/udp': 1900,
                                           '32410/udp': 32410,
                                           '32412/udp': 32412,
                                           '32413/udp': 32413,
                                           '32414/udp': 32414
                                       }
                                       )
        except docker.errors.APIError:
            container = self.client.containers.get('plex')
            container.start()

    def start_mongodb(self):
        try:
            self.client.images.pull(repository='mongo:latest')
            self.client.containers.run("mongo",
                                       detach="True",
                                       name="mongo",
                                       hostname="Mike",
                                       environment=[
                                            "MONGO_INITDB_ROOT_USERNAME="+'test',
                                            "MONGO_INITDB_ROOT_PASSWORD="+'password'
                                           ],
                                       ports={
                                           '27017/tcp': 27017
                                       }
                                       )
        except docker.errors.APIError:
            container = self.client.containers.get('mongo')
            container.start()

    def start_rabbitmq(self):
        try:
            self.client.images.pull(repository='rabbitmq:latest')
            self.client.containers.run("rabbitmq",
                                       detach="True",
                                       name="rabbit",
                                       hostname="Mike",
                                       ports={
                                           '15672/tcp': 15672,
                                           '5673/tcp': 5672
                                       }
                                       )
        except docker.errors.APIError:
            container = self.client.containers.get('mongo')
            container.start()

    def start_server(self, server_name):
        if server_name == 'plex':
            self.start_plex()
        elif server_name == 'terraria':
            self.start_terraria()
        elif server_name == 'mongo':
            self.start_mongodb()
        elif server_name == 'rabbit':
            self.start_rabbitmq()
        return

    def stop_server(self, server_name):
        container = self.client.containers.get(server_name)
        container.stop()

    def container_status(self):
        server_status = {}
        for container_name in self.server_names:
            try:
                container = self.client.containers.get(container_name)
                status = container.status
                server_status[container_name] = status
            except docker.errors.NotFound:
                server_status[container_name] = "missing"
                continue
        return server_status

    def fake_container_status(self):
        server_status = {
            "plex": "running",
            "minecraft": "running"
        }
        return server_status

    def terraria_(self):
        pass

    def list_containers(self):
        test = self.client.containers.list()
        print(test)
