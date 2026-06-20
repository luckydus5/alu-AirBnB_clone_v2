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
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html

# (Re)create the symbolic link 'current' pointing to the test release
ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of /data/ recursively to the ubuntu user and group
chown -R ubuntu:ubuntu /data/

# Update the Nginx configuration to serve /data/web_static/current/ at /hbnb_static
new_location="\\\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n"
sed -i "/listen 80 default_server;/a $new_location" /etc/nginx/sites-available/default

# Restart Nginx to apply the new configuration
service nginx restart

exit 0
