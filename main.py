"""append mysql service to docker-compose.yml"""

import hashlib
import os
import random
import uuid

import fire
import yaml

pwd = os.getcwd()
md5 = hashlib.md5(pwd.encode())

HEX_HASH = md5.hexdigest()
random.seed(int(HEX_HASH[:8], 16))
mysqlPort = random.randint(1024, 65535)
while True:
    phpMyAdminPort = random.randint(1024, 65535)
    if phpMyAdminPort != mysqlPort:
        break


def main(
    name=f"mysql-{HEX_HASH}",
    port=mysqlPort,
    aname=f"phpmyadmin-{HEX_HASH}",
    aport=phpMyAdminPort
):
    """main function"""
    # docker-compose.yml が存在しないときは作成する
    with open("docker-compose.yml", "a+", encoding="utf8") as file:
        pass

    with open("docker-compose.yml", "r", encoding="utf8") as file:
        data = yaml.load(file, yaml.Loader)

    if data is None:
        data = {}
    if "version" not in data:
        data["version"] = "3"
    if "services" not in data:
        data["services"] = {}
    data["services"][name] = {
        "image": "mysql:5.7",
        "ports": [f"{port}:3306"],
        "environment": [
            "MYSQL_ROOT_PASSWORD=root",
            "MYSQL_DATABASE=test",
        ]
    }
    data["services"][aname] = {
        "image": "phpmyadmin",
        "ports": [f"{aport}:80"],
        "environment": [
            "PMA_ARBITRARY=1",
            f"PMA_HOST={name}",
            "PMA_USER=root",
            "PMA_PASSWORD=root",
        ]
    }
    tmp_file_name = f"{uuid.uuid4()}.yml"
    with open(tmp_file_name, "w", encoding="utf8") as file:
        yaml.dump(data, file)

    os.remove("docker-compose.yml")
    os.rename(tmp_file_name, "docker-compose.yml")


if __name__ == "__main__":
    fire.Fire(main)
