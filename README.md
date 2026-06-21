# AirBnB clone - v2

A clone of the AirBnB website. This repository covers the v2 milestones:

- **The storage engine** — `BaseModel` and the data models, with two
  interchangeable back ends: `FileStorage` (JSON file) and `DBStorage`
  (MySQL via SQLAlchemy), selected at runtime with environment variables.
- **The console** — a command interpreter (`console.py`) to create, show,
  update and destroy objects.
- **The web framework** — a [Flask](https://flask.palletsprojects.com/)
  application (`web_flask/`) that renders the data with
  [Jinja](https://jinja.palletsprojects.com/) templates.
- **Static deployment** — the original `web_static/` deployment scripts
  (kept from the previous project, see the bottom of this file).

## Storage engines

The engine is chosen by the `HBNB_TYPE_STORAGE` environment variable:

| Value      | Engine        | Persistence            |
|------------|---------------|------------------------|
| `db`       | `DBStorage`   | MySQL (SQLAlchemy ORM) |
| any other  | `FileStorage` | `file.json`            |

`DBStorage` reads its connection settings from the environment:
`HBNB_MYSQL_USER`, `HBNB_MYSQL_PWD`, `HBNB_MYSQL_HOST`, `HBNB_MYSQL_DB`,
and (in test mode) `HBNB_ENV=test`.

### MySQL setup

```
cat setup_mysql_dev.sql | mysql -uroot -p     # hbnb_dev_db / hbnb_dev
cat setup_mysql_test.sql | mysql -uroot -p    # hbnb_test_db / hbnb_test
```

## Console

```
# FileStorage
./console.py

# DBStorage
HBNB_MYSQL_USER=hbnb_dev HBNB_MYSQL_PWD=hbnb_dev_pwd \
HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_dev_db \
HBNB_TYPE_STORAGE=db ./console.py
```

`create` accepts `<key>=<value>` parameters, e.g.
`create State name="California"`.

## Web framework (`web_flask`)

Install Flask first: `pip3 install Flask`. Each task is its own runnable
module, started with `python3 -m web_flask.<module>`:

| Task | Module                          | Routes |
|------|---------------------------------|--------|
| 0    | `0-hello_route`                 | `/` |
| 1    | `1-hbnb_route`                  | `/`, `/hbnb` |
| 2    | `2-c_route`                     | `+ /c/<text>` |
| 3    | `3-python_route`                | `+ /python/(<text>)` (default `is cool`) |
| 4    | `4-number_route`                | `+ /number/<n>` (int only) |
| 5    | `5-number_template`             | `+ /number_template/<n>` |
| 6    | `6-number_odd_or_even`          | `+ /number_odd_or_even/<n>` |
| 7    | `7-states_list`                 | `/states_list` |
| 8    | `8-cities_by_states`            | `/cities_by_states` |
| 9    | `9-states`                      | `/states`, `/states/<id>` |
| 10   | `10-hbnb_filters`               | `/hbnb_filters` |

The data-driven tasks (7-10) fetch from the active storage engine and
remove the SQLAlchemy session after every request via
`@app.teardown_appcontext`. Example:

```
HBNB_MYSQL_USER=hbnb_dev HBNB_MYSQL_PWD=hbnb_dev_pwd \
HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_dev_db \
HBNB_TYPE_STORAGE=db python3 -m web_flask.10-hbnb_filters
```

Then open `http://0.0.0.0:5000/hbnb_filters` in the browser.

## Layout

```
models/                 storage engine and data models
  engine/
    file_storage.py     JSON-file back end
    db_storage.py       MySQL/SQLAlchemy back end
  base_model.py         Base class + SQLAlchemy declarative Base
  user.py state.py city.py amenity.py place.py review.py
console.py              command interpreter
setup_mysql_dev.sql     dev database/user setup
setup_mysql_test.sql    test database/user setup
web_flask/              Flask application (tasks 0-10)
  templates/            Jinja templates
  static/styles/        CSS for the filters page
  static/images/        logo.png, icon.png
web_static/             static HTML/CSS (deployment project)
```

---

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

## Authors

- Jael Savadogo
- Olivier Dusabamahoro
