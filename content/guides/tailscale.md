+++
title = 'Serving OpenRelik with Tailscale'
linkTitle = 'Tailscale'
date = 2024-10-26T21:53:59+02:00
draft = false
+++

This guide outlines the process of integrating your OpenRelik server with Tailscale, allowing secure access to your server from anywhere on your Tailscale network.

**Prerequisites:**

* An installed and functioning OpenRelik server.
* A Tailscale account with administrative privileges.

**Steps:**

1. **Install OpenRelik:** Follow the standard OpenRelik installation instructions to set up your server. [Installation instructions](/docs/getting-started)

2. **Obtain your Tailscale Name:** Identify your Tailscale network name, which usually follows the format `yourname.ts.net`.

3. **Generate a Tailscale AuthKey:**

    * Log in to your Tailscale admin console at [https://tailscale.com](https://tailscale.com).
    * Navigate to **Settings -> Personal settings -> Keys**
    * Click **"Generate auth key..."**
    * Provide a descriptive name for your key (e.g., "OpenRelik")
    * Enable the **"Reusable"** option to use the same key for both API and UI servers
    * Copy the generated key for later use

4. **Create Configuration Directories:** In your OpenRelik directory, create the following directories:

    ```bash
    tailscale-nginx-api/config
    tailscale-nginx-ui/config
    ```

5. **Configure Tailscale for OpenRelik API:** Create the file `tailscale-nginx-api/config/openrelik-api.json` with the following content:

    ```json
    {
      "TCP": {
        "443": {
          "HTTPS": true
        }
      },
      "Web": {
        "openrelik-api.yourname.ts.net:443": {
          "Handlers": {
            "/": {
              "Proxy": "http://127.0.0.1:8710"
            }
          }
        }
      }
    }
    ```

    **Important:** Replace `yourname.ts.net` with your actual Tailscale network name.

6. **Configure Tailscale for OpenRelik UI:** Create the file `tailscale-nginx-ui/config/openrelik-ui.json` with the following content:

    ```json
    {
      "TCP": {
        "443": {
          "HTTPS": true
        }
      },
      "Web": {
        "openrelik.yourname.ts.net:443": {
          "Handlers": {
            "/": {
              "Proxy": "http://127.0.0.1:8711"
            }
          }
        }
      }
    }
    ```

    **Important:** Replace `yourname.ts.net` with your actual Tailscale network name.

7. **Update docker-compose.yml:** Add the following services to your `docker-compose.yml` file:

    ```yaml
    tailscale-nginx-ui:
      container_name: openrelik-tailscale-nginx-ui
      image: tailscale/tailscale:latest
      hostname: openrelik
      environment:
        - TS_AUTHKEY=<AUTHKEY>
        - TS_SERVE_CONFIG=/config/openrelik-ui.json
        - TS_STATE_DIR=/var/lib/tailscale
      volumes:
        - ${PWD}/tailscale-nginx-ui/state:/var/lib/tailscale
        - ${PWD}/tailscale-nginx-ui/config:/config
        - /dev/net/tun:/dev/net/tun
      cap_add:
        - net_admin
        - sys_module

    tailscale-nginx-api:
      container_name: openrelik-tailscale-nginx-api
      image: tailscale/tailscale:latest
      hostname: openrelik-api
      environment:
        - TS_AUTHKEY=<AUTHKEY>
        - TS_SERVE_CONFIG=/config/openrelik-api.json
        - TS_STATE_DIR=/var/lib/tailscale
      volumes:
        - ${PWD}/tailscale-nginx-api/state:/var/lib/tailscale
        - ${PWD}/tailscale-nginx-api/config:/config
        - /dev/net/tun:/dev/net/tun
      cap_add:
        - net_admin
        - sys_module
    ```
    **Important:** Replace `<AUTHLEY>` with your AuthKey that you created in step 3.

8. **Modify Existing Services in docker-compose.yml:** Adjust the `openrelik-server` and `openrelik-ui` services in your `docker-compose.yml` file as follows:

    ```yaml
    openrelik-server:
      # ... (existing configuration) ...
      depends_on:
        - tailscale-nginx-api
      network_mode: service:tailscale-nginx-api
      command: uvicorn main:app --proxy-headers --forwarded-allow-ips '*' --workers 1 --host 0.0.0.0 --port 8710

    openrelik-ui:
      # ... (existing configuration) ...
      depends_on:
        - tailscale-nginx-ui
      network_mode: service:tailscale-nginx-ui
    ```

9. **Update config.env:** In your OpenRelik directory, modify the `config.env` file:

    ```
    OPENRELIK_SERVER_URL=https://openrelik-api.yourname.ts.net
    ```

    **Important:** Replace `yourname.ts.net` with your actual Tailscale network name.

10. **Update settings.toml:** In your OpenRelik directory, modify the `config/settings.toml` file:

    ```toml
    # ... (existing configuration) ...
    api_server_url = "https://openrelik-api.yourname.ts.net"
    ui_server_url = "https://openrelik.yourname.ts.net"
    allowed_origins = ["https://openrelik.yourname.ts.net"]
    ```

    **Important:** Replace `yourname.ts.net` with your actual Tailscale network name.

11. **Restart OpenRelik:** Restart your OpenRelik server using `docker-compose up -d` to apply the changes.

Your OpenRelik server should now be accessible via your Tailscale network at the URLs you configured. You can access the UI by navigating to `https://openrelik.yourname.ts.net` from any device connected to your Tailscale network.


