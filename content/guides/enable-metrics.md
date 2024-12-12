+++
title = 'Enabling Metrics on a deployed OpenRelik Server'
linkTitle = 'Enable Metrics'
date = 2024-12-12T11:59:33+01:00
draft = false
+++

{{< callout type="info" >}}
Metrics are enabled by default starting with version **2024.12.12**. This guide is for
enabling the metrics functionality on a already deployed server.
{{< /callout >}}

This guide outlines the steps to enable metrics collection on your OpenRelik server using Prometheus.

**1. Add Metrics Collector:**

* Define a service named `openrelik-metrics` in your Docker Compose file.
```
openrelik-metrics:
    container_name: openrelik-metrics
    image: ghcr.io/openrelik/openrelik-metrics:${OPENRELIK_METRICS_VERSION}
    restart: always
    environment:
      - REDIS_URL=redis://openrelik-redis:6379
    command: "python exporter.py"
```

**2. Define Metrics Version:**

* In your `config.env` file, set the environment variable `OPENRELIK_METRICS_VERSION` to `2024.12.12` or `latest` to use the most recent version of the metrics collector image.

**3. Add Prometheus Server:**

* Define a service named `openrelik-prometheus` in your Docker Compose file.
```
openrelik-prometheus:
  container_name: openrelik-prometheus
  image: prom/prometheus:v3.0.1
  restart: always
  volumes:
    - ./config/prometheus:/etc/prometheus
    - ./data/prometheus:/prometheus
  command: --config.file=/etc/prometheus/prometheus.yml
```

**4. Configure Prometheus:**

* Create a `prometheus.yml` file in the `./config/prometheus` directory.
```
global:
  scrape_interval: 10s
  external_labels:
    monitor: "openrelik"
scrape_configs:
  - job_name: "celery"
    static_configs:
      - targets: ["openrelik-task-metrics:8080"]
```

**Note:**
* Adjust the configuration to suit your specific needs and monitoring requirements.
