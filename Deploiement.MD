# Deploiement
## Créer un service systemd
 
sudo nano /etc/systemd/system/bixiviz.service  

``` 
[Unit]
Description=Gunicorn instance to serve bixiviz
After=network.target
 
[Service] 
User=comero
Group=www-data
WorkingDirectory=/home/comero/INF8808E_BIXI
Environment="/home/comero/INF8808E_BIXI/.venv/bin"
ExecStart=/home/comero/INF8808E_BIXI/.venv/bin/gunicorn -b 127.0.0.1:8000 app:server

[Install]
WantedBy=multi-user.target

```

sudo cp ./bixiviz.service /etc/systemd/system/

sudo systemctl daemon-reload
sudo systemctl start bixiviz
sudo systemctl enable bixiviz  

bixiviz
```
server {
    listen 80;
    server_name inf8808.ceyraud.com ;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

sudo cp bixiviz /etc/nginx/sites-available/


sudo ln -s /etc/nginx/sites-available/bixiviz /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx


sudo certbot --nginx -d inf8808.ceyraud.com
