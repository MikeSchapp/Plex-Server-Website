from mock import patch
from Sophia.server_control.objects.docker_commands import DockerApi


def test_docker_images_pull():
    with patch('docker.client.DockerClient.images') as mock_docker:
        test = DockerApi('test')
        test.start_plex()
        pull = mock_docker.pull
        pull.assert_called()






