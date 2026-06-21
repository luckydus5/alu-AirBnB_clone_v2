#!/usr/bin/env bash
# Sets up the web servers for the deployment of web_static.
# Installs Nginx, creates the required folder tree, a fake index.html,
# a 'current' symlink, fixes ownership and configures Nginx to serve
# /data/web_static/current/ at the /hbnb_static location using 'alias'.

# Install Nginx if it is not already installed
if ! command -v nginx > /dev/null 2>&1; then
    apt-get update
    apt-get -y install nginx
fi

# Create the required folder structure (-p makes parents and is idempotent)
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# Create a fake HTML file to test the Nginx configuration
printf '%s\n' \
    "<html>" \
    "  <head>" \
    "  </head>" \
    "  <body>" \
    "    Holberton School" \
    "  </body>" \
    "</html>" > /data/web_static/releases/test/index.html

# (Re)create the symbolic link 'current' pointing to the test release
ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of /data/ recursively to the ubuntu user and group
chown -R ubuntu:ubuntu /data/

# Write the Nginx server config, serving /data/web_static/current/
# at /hbnb_static with alias. Rewriting the whole file keeps the script
# idempotent (re-runs never stack duplicate location blocks).
config="server {
    listen 80 default_server;
    listen [::]:80 default_server;
    root /var/www/html;
    index index.html index.htm;
    add_header X-Served-By \$hostname;
    location /hbnb_static/ {
        alias /data/web_static/current/;
    }
    location / {
        try_files \$uri \$uri/ =404;
    }
}"
echo "$config" > /etc/nginx/sites-available/default
ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default

# Restart Nginx to apply the new configuration
service nginx restart

exit 0
