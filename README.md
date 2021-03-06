# Prometheus-101-for-DataDog-users

## Q & A
#### 
Q: What is Prometheus?  
A: is a self-hosted OpenSource Time-Series DB that stores metrics (in two words metric db).

Q: What are others TSDB out there beside Prometheus?  
A: InfluxDB, VictoriaMetrics

Q: Where is config of prometheus stored?  
A: usaully it is prometheus.yml, also could be alterd by -config argument when service is started 

Q: What is alert manager in Prometheus?  
A: It is separate service (optional) that allows deduplication, silencing, and routing/sending of metrics-based alerts to e-mail, IM (slack) etc. You let know Prometheus if alert manager is there by configuring 'alertmanager' section in prometheus.yml config and 'alertmanager rules' that point to another yaml with alert rules (what is name, threshhold to fire, etc) specific metric-based alert (e.g. Node is downm, disk space  is low, free memory is low etc)
Alert manager runs on its own <alert-manager-IP>:9093 by default and has its own alermanager.yml config file and secrets.yaml where you list alert receivers and API keys respectively. 

Q: Can I use prometheus exporters, alerts and charts without Prometheus tsdb?  
A: Yes! with VictoriaMetrics & Grafana & alertmanager.

  
Q: What is default port on node exporter used by Prometheus server to scrape metrics?  
A: The node_exporter listens on HTTP port 9100.
  
Q: Waht is Target?
A: It is sever:port/metrics with specific name that provideds metrics for scraping by Prometheus server. It has state: up/down, and labels: job: name, instance:<ip-addr:port> etc.
  
Q: What happens if target/enpoint is down?  
A: you can create rule isDown and alert on this event.

Q: What is PromQL?
A: It is query language that used to build request to TSDB. Also used in Grafana, and Alertmanager whenever you have to extract specific metric data from TSDB.




### Lingo, Entity names

#### Agent: 

##### DataDog -> **DataDog agent**. 
  (binary that you as SRE have to install on your server/node to collect and send/aka Push metrics and logs to DataDog SaaS. Will use API key to let SaaS server know where to put your metrics on the server.

##### Prometheus -> **node exporter**, **black box exporter**. 
  agents that will 'expose' aka offere to poll your metrics for collection by Prometheus server. Process is called 'scraping', metrics sraping.  agents are called 'targets' in prometheus.yml config file. **Black-box exporter** is a name for Synthetic test service that make GET/Post to one of your endpoints and checks response, then allow you to calculate how much time service was healthy and how much it did not return OK/200 + stuff like latency of the request/responce, its body etc.

#### WebUI:
<prometheus-server-ip:9090>. 
<alertmanager-server-ip:9030>. 
Prometheus has limited web-ui and metrics explorer to see config, metrics being collected, alerts, etc. Usually separate dashboard solution is used for displaying grahs/charts -> **Grafana**. Prometheus would act as datasource for **Grafana**.

<datadog.com /region>

  
 Q: How to mute aka Silence alert with Python script for specific period of time via REST API to alert manager?
  A: You need matchers (aka alert labels, lile job: myjob, or instance:<servername> and silence durarion - 1h in example below:
  ``` 
  # silence-alert.py 
  #!/usr/bin/python3
import requests
import socket
import datetime
import time

res = requests.post("http://alertmanager:9093/api/v2/silences", json={
    "matchers": [
        {"name": "job", "value": "myjob", "isRegex": False},
        {"name": "instance", "value": "{}:1234".format(socket.gethostname()), "isRegex": False},
        ],
    "startsAt": datetime.datetime.utcfromtimestamp(time.time()).isoformat(),
    "endsAt": datetime.datetime.utcfromtimestamp(time.time() + 4*3600).isoformat(),
    "comment": "Backups on {}".format(socket.gethostname()),
    "createdBy": "My backup script",
    },
    )
res.raise_for_status()
silenceId = res.json()["silenceID"]
  ```
also do 
  ```
  chmod +x ./silenec-alert.py
  ```
  and run as 
  ```./silence-alert.py
  ```
  
  
  Q: How to expose Alertmanager through virtual host Nginx reverse proxy?
  A: 
  https://rtfm.co.ua/prometheus-alertmanager-web-ui-i-silence-alertov/
  
  1. add to command section of alertmanager coonfig yaml file ( /etc/alertmanager/config.yaml):
  ```
  /etc/prometheus/alertmanager_config.yml:/etc/alertmanager/config.yml
    command:
      - '--config.file=/etc/alertmanager/config.yml'
      - '--web.route-prefix=/alertmanager'
      - '--web.external-url=https://dev.monitor.example.com/alertmanager'
  ```
  2. Configure Ngingx virtual host:
  add new upstream section to nginx config that points to alertmanager IP address: port & restart nginx:
  ```
  upstream alertmanager {
    server 127.0.0.1:9093;
  }
  ```
  
  3. Configure Nginx proxy to redirect/proxy all request to /alertmanager path to specific upstream cofigured above:
  ```
      location /alertmanager {
        
        proxy_redirect          off;            
        proxy_set_header        Host            $host;
        proxy_set_header        X-Real-IP       $remote_addr;
        proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_pass http://alertmanager$request_uri;
    }
  ```
  4. restart nginx & alertmanager
  5. update Prometheus config with new path_prefix to point to the above virtual host
  ```...
alerting:
  alertmanagers:
  - path_prefix: "/alertmanager/"
    static_configs:
    - targets:
      - alertmanager:9093
...
  ```
  6. restart Prometheus & check if there is no errors in logs related to alerts sendign like below:
  Prometheus: ???Error sending alert??? err=???bad response status 404 Not Found???
  ```
  caller=notifier.go:527 component=notifier alertmanager=http://alertmanager:9093/api/v1/alerts count=3 msg=???Error sending alert??? err=???bad response status 404 Not Found???
  ```
  
  




