# AirBnB clone - Deploy static

Deployment of the `web_static` part of the AirBnB clone using
[Fabric](https://www.fabfile.org/) (Fabric3 for Python 3).

## Servers

| Name        | Role          | IP             |
|-------------|---------------|----------------|
| web-01      | web server    | 13.218.57.12   |
| web-02      | web server    | 44.202.228.82  |
| lb-01       | load balancer | 54.89.248.181  |

## Files

| File | Description |
|------|-------------|
| `0-setup_web_static.sh` | Bash script that prepares a web server: installs Nginx, creates the `/data/web_static/` tree, a fake `index.html`, the `current` symlink, sets ownership to `ubuntu`, and configures Nginx to serve `/data/web_static/current/` at `/hbnb_static` using `alias`. |
| `1-pack_web_static.py` | Fabric `do_pack()` — builds a timestamped `.tgz` archive of `web_static/` in `versions/`. |
| `2-do_deploy_web_static.py` | Fabric `do_deploy(archive_path)` — uploads and deploys an archive to both web servers. |
| `3-deploy_web_static.py` | Fabric `deploy()` — runs `do_pack()` then `do_deploy()` in one step. |

## Installation (Fabric 3 — version 1.14.post1)

```
pip3 uninstall Fabric
sudo apt-get install libffi-dev libssl-dev build-essential python3.4-dev libpython3-dev
pip3 install pyparsing appdirs
pip3 install setuptools==40.1.0
pip3 install cryptography==2.8
pip3 install bcrypt==3.1.7
pip3 install PyNaCl==1.3.0
pip3 install Fabric3==1.14.post1
```

## Usage

```
# 0. Prepare each web server (run ON the server, as root/sudo)
sudo ./0-setup_web_static.sh

# 1. Pack web_static into a .tgz archive (run locally)
fab -f 1-pack_web_static.py do_pack

# 2. Deploy an existing archive to both web servers
fab -f 2-do_deploy_web_static.py \
    do_deploy:archive_path=versions/web_static_<timestamp>.tgz \
    -i my_ssh_private_key -u ubuntu

# 3. Pack and deploy in one command
fab -f 3-deploy_web_static.py deploy -i my_ssh_private_key -u ubuntu
```
