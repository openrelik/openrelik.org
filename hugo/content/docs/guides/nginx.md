+++
title = 'OpenRelik with Nginx'
linkTitle = 'Nginx as a Reverse Proxy'
date = 2025-01-25T11:55:09+01:00
draft = false
+++

This guide provides a comprehensive walkthrough on how to configure Nginx as a reverse proxy to serve your OpenRelik server.

**Prerequisites:**

- An installed and functioning OpenRelik server.
- An installed Nginx server.

**Steps:**

1. **Install OpenRelik:** Follow the standard OpenRelik installation instructions to set up your server. [Installation instructions](/docs/getting-started)

2. **Update config.env:** In your OpenRelik directory, modify the `config.env` file:

   ```
   OPENRELIK_SERVER_URL=https://<YOUR_SERVER_NAME_OR_IP>
   ```

   **Important:** Replace `<YOUR_SERVER_NAME_OR_IP>` with your server's domain name or IP address.

3. **Update settings.toml:** In your OpenRelik directory, modify the `config/settings.toml` file:

   ```toml
   # ... (existing configuration) ...
   api_server_url = "https://<YOUR_SERVER_NAME_OR_IP>"
   ui_server_url = "https://<YOUR_SERVER_NAME_OR_IP>"
   allowed_origins = ["https://<YOUR_SERVER_NAME_OR_IP>"]
   ```

   **Important:** Replace `<YOUR_SERVER_NAME_OR_IP>` with your server's domain name or IP address.

4. **Restart OpenRelik:** Restart your OpenRelik server using `docker-compose up -d` to apply the changes.

5. **Install Nginx:** Install Nginx on your server using the package manager of your choice.

6. **Create a New Nginx Configuration File:** Create a new Nginx configuration file for your OpenRelik server. For example, create a file named `openrelik` in the `/etc/nginx/sites-available/` directory.

   ```nginx
   server {
       listen 80;
       #listen 443 ssl;
       server_name <YOUR_SERVER_NAME_OR_IP>;

       #ssl_certificate <PATH_TO_TLS_CERT_CRT>.crt;
       #ssl_certificate_key <PATH_TO_TLS_CERT_KEY>.key;

       location /auth/ {
           proxy_pass http://127.0.0.1:8710/auth/;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header Cookie $http_cookie;
       }

       location /api/v1/ {
           proxy_pass http://127.0.0.1:8710/api/v1/;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header Cookie $http_cookie;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           client_max_body_size 100M;
       }

       location / {
           proxy_pass http://127.0.0.1:8711/;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header Cookie $http_cookie;
       }
   }
   ```

   **Important:** You can generate a certificate using [Let's Encrypt](https://certbot.eff.org/instructions?ws=nginx&os=ubuntufocal) or any other certificate authority. Replace `<YOUR_SERVER_NAME_OR_IP>` with your server's domain name or IP address. Uncomment the `listen 443 ssl;`, `ssl_certificate`, and `ssl_certificate_key` lines to enable HTTPS. Replace `<PATH_TO_TLS_CERT_CRT>` and `<PATH_TO_TLS_CERT_KEY>` with the path to your TLS certificate files.

7. **Enable the Configuration File:** Create a symbolic link to the configuration file in the `/etc/nginx/sites-enabled/` directory.

   ```bash
   ln -s /etc/nginx/sites-available/openrelik /etc/nginx/sites-enabled/openrelik
   ```

8. **Test and Restart Nginx:** Test the configuration syntax and restart the Nginx service to apply the changes.

   ```bash
   sudo nginx -t
   sudo systemctl restart nginx
   ```
