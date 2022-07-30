import fire
import hashlib
import os
import random
import uuid
import yaml

pwd = os.getcwd()
hash = hashlib.md5(pwd.encode())
hexHash = hash.hexdigest()
random.seed(int(hexHash[:8], 16))
mysqlPort = random.randint(1024, 65535)
while True:
    phpMyAdminPort = random.randint(1024, 65535)
    if phpMyAdminPort != mysqlPort:
        break

def main(
    name=f"mysql-{hexHash}", 
    port=mysqlPort, 
    aname=f"phpmyadmin-{hexHash}", 
    aport=phpMyAdminPort
):
    # docker-compose.yml が存在しないときは作成する
    open("docker-compose.yml", "a+").close()
    
    with open("docker-compose.yml", "r") as f:
        data = yaml.load(f, yaml.Loader)

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
    tmpFileName = f"{uuid.uuid4()}.yml"
    with open(tmpFileName, "w") as f:
        yaml.dump(data, f)
        
    os.remove("docker-compose.yml")
    os.rename(tmpFileName, "docker-compose.yml")

if __name__ == "__main__":
    fire.Fire(main)
