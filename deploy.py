import requests
import json
from requests.auth import HTTPDigestAuth
from base64 import urlsafe_b64encode
from config.config import Config as cfg
config = cfg.deploy_json
dns_auth = HTTPDigestAuth('admin', 'KeYv0e_xd')
portainer_auth_params = {
    "username": cfg.portainer_username,
    "password": cfg.portainer_password
}


def get_auth_headers():
    print('Authenticating...')
    auth_response = requests.post(f'{cfg.rpi_address}/auth',
                                  json=portainer_auth_params, auth=dns_auth)

    js = json.loads(auth_response.text)
    token = js['jwt']
    print('JWT token: ', token)

    docker_auth_params = config['docker']['auth']['params']
    docker_auth_params['username'] = cfg.dockerhub_username
    docker_auth_params['password'] = cfg.dockerhub_password
    auth_enc = urlsafe_b64encode(json.dumps(docker_auth_params).encode('ascii')).decode('ascii')
    headers = {
        'X-Registry-Auth': auth_enc,
        'X-API-Key': 'ptr_jbCvcvd3BPIAijhoNJPaOQ0TDRzPBZOh9TdV9SC+jK4=',
        'Authorization': f'Bearer {token}'
    }
    return headers


def get_containers(headers):
    params = config['container']['get']['params']
    containers_res = requests.get(f'{cfg.rpi_address}/endpoints/{cfg.endpoint_id}/docker/containers/json',
                                  headers=headers, auth=dns_auth, params=params)
    print('Getting all containers')
    containers = json.loads(containers_res.text)
    print(f'Found {len(containers)} containers')
    return containers


def get_images(headers):
    print('Getting all images')
    images_res = requests.get(f'{cfg.rpi_address}/endpoints/{cfg.endpoint_id}/docker/images/json',
                              headers=headers, auth=dns_auth)
    images = json.loads(images_res.text)
    print(f'Found {len(images)} images')
    return images


def stop_container(id, headers):
    print('Stopping container...')
    r = requests.post(f'{cfg.rpi_address}/endpoints/{cfg.endpoint_id}/docker/containers/{id}/stop',
                      headers=headers, auth=dns_auth)
    if not (r.status_code == 204 or r.status_code == 304):
        print('Unable to stop container')
        print(f'''Status code: {r.status_code} \
            Response text: {r.text}''')
    

def delete_container(id, headers):
    print('Removing container...')
    r = requests.delete(f'{cfg.rpi_address}/endpoints/{cfg.endpoint_id}/docker/containers/{id}',
                        headers=headers, auth=dns_auth)
    if not r.status_code == 204:
        print('Unable to delete container')
        print(f'''Status code: {r.status_code} \
            Response text: {r.text}''')


def delete_image(id, headers):
    print('Removing bot image')
    r = requests.delete(f'{cfg.rpi_address}/endpoints/{cfg.endpoint_id}/docker/images/{id}', auth=dns_auth, headers=headers)
    if not r.status_code == 200:
        print('Unable to delete image')
        print(f'''Status code: {r.status_code} \
            Response text: {r.text}''')


def create_image(headers):
    params = config['image']['create']['params']
    print('Trying to pull image')

    r = requests.post(f'{cfg.rpi_address}/endpoints/{cfg.endpoint_id}/docker/images/create',
                      auth=dns_auth, params=params, headers=headers)
    if not r.status_code == 200:
        print('Unable to pull image')
        print(f'''Status code: {r.status_code} \
            Response text: {r.text}''')


def create_container(headers):
    create_json = config['container']['create']['json']
    create_json['Env'] = [
            f"YANDEX_API_KEY={cfg.yand_api_key}",
            f"DISCORD_BOT_TOKEN={cfg.discord_bot_token}",
            f"PYOWM_API_KEY={cfg.pyowm_api_key}",
            f"GUILD_ID={cfg.guild_id}",
            f"NEWS_API_KEY={cfg.news_api_key}",
        ]
    
    create_params = config['container']['create']['params']

    print('Creating a container...')
    r = requests.post(f'{cfg.rpi_address}/endpoints/{cfg.endpoint_id}/docker/containers/create',
                      auth=dns_auth, json=create_json, headers=headers, params=create_params)
    
    if not r.status_code == 200:
        print('Unable to create container')
        print(f'''Status code: {r.status_code}\n
        Response text: {r.text}''')
    
    container_id = json.loads(r.text)['Id']
    return container_id


def start_container(id, headers):
    print('Starting container')
    r = requests.post(f'{cfg.rpi_address}/endpoints/{cfg.endpoint_id}/docker/containers/{id}/start',
                      headers=headers, auth=dns_auth)
    if not r.status_code == 204:
        print('Unable to start container')
        print(f'''Status code: {r.status_code}\n
        Response text: {r.text}''')


def main():
    headers = get_auth_headers()
    containers = get_containers(headers)
    images = get_images(headers)
    
    for container in containers:
        if config['container']['find']['name'] in container['Names']:
            print('bot container found')
            container_id = container['Id']
            if container['State'] == 'running':
                print('bot container is running')
                stop_container(container_id, headers)
                # remove the container
            delete_container(container_id, headers)

    for image in images:
        # search for bot image
        if any(config['image']['find']['name'] in x for x in image['RepoTags']):
            print('Bot image found')
            image_id = image['Id'].split(':')[1]  # get image id without sha256
            # delete image
            delete_image(image_id, headers)

    # pull new image
    create_image(headers)
    container_id = create_container(headers)
    start_container(container_id, headers)


if __name__ == '__main__':
    main()
