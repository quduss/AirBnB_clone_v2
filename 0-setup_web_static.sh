#!/usr/bin/env bash
#
if ! command -v nginx &> /dev/null
then
    # Nginx is not installed, so install it
    apt-get -y update
    apt-get install nginx -y
fi

SOURCE="/data/web_static/releases/test/"
DESTINATION="/data/web_static/current"

mkdir -p /data/web_static/shared/
mkdir -p /data/web_static/releases/test/
echo "Hello World!" > /data/web_static/releases/test/index.html

if [ -L "$DESTINATION" ]; then
    rm "$DESTINATION"
fi

# Create a new symbolic link
ln -s "$SOURCE" "$DESTINATION"
chown -R ubuntu:ubuntu /data
sed -i "s/server_name _;/server_name _;\n\tlocation \/hbnb_static {\n\t\talias \/data\/web_static\/current\/;\n\t}/" /etc/nginx/sites-available/default
service nginx restart
