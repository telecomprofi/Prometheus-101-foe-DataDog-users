# Prometheus-101-foe-DataDog-users

## Q& A
#### 
Q: What is Prometheus?  
A: is a self-hosted OpenSource Time-Series DB that stores metrics (in two words metric db)

Q: What are others TSDB out there beside Prometheus?  A: InfluxDB, VictoriaMetrics

Q: Where is config of prometheus stored?  A: usaully it is prometheus.yml, also could be alterd by -config argument when service is started 

Q: What is alert manager in Prometheus?  A: It is separate service (optional) that allows deduplication, silencing, and routing/sending of metrics-based alerts to e-mail, IM (slack) etc. You let know Prometheus if alert manager is there by configuring 'alertmanager' section in prometheus.yml config and 'alertmanager rules' that point to another yaml with alert rules (what is name, threshhold to fire, etc) specific metric-based alert (e.g. Node is downm, disk space  is low, free memory is low etc)
Alert manager runs on its own <alert-manager-IP>:9093 by default and has its own alermanager.yml config file and secrets.yaml where you list alert receivers and API keys respectively. 

Q: Can I use prometheus exporters, alerts and charts without Prometheus tsdb?  A: Yes! with VictoriaMetrics & Grafana & alertmanager.

  
Q: What is default port on node exporter used by Prometheus server to scrape metrics?   A: 5000?




### Entity names

#### Agent: 

##### DataDog -> **DataDog agent**  (binary that you as SRE have to install on your server/node to collect and send/aka Push metrics and logs to DataDog SaaS. Will use API key to let SaaS server know where to put your metrics on the server.

##### Prometheus -> **node exporter**, **black box exporter** - agents that will 'expose' aka offere to poll your metrics for collection by Prometheus server. Process is called 'scraping', metrics sraping.  agents are called 'targets' in prometheus.yml config file. **Black-box exporter** is a name for Synthetic test service that make GET/Post to one of your endpoints and checks response, then allow you to calculate how much time service was healthy and how much it did not return OK/200 + stuff like latency of the request/responce, its body etc.

#### WebUI:
<prometheus-server-ip:9090>
<alertmanager-server-ip:9030>
Prometheus has limited web-ui and metrics explorer to see config, metrics being collected, alerts, etc. Usually separate dashboard solution is used for displaying grahs/charts -> Grafana. Prometheus would act as datasource for Grafana.

<datadog.com /region>





