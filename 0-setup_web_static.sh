#!/usr/bin/env bash
# setup my web server to serve the content present in a designated path
# to hbnb_static (ex: https://mydomainname.tech/hbnb_static).

sudo apt-get update -qq
sudo apt-get install -y nginx -qq
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/
touch /data/web_static/releases/test/index.html
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu:ubuntu /data
sudo chmod -R 755 /data/
sudo sed -i "/listen 80 default_server;/ a \\\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n" /etc/nginx/sites-available/default
sudo service nginx restart
