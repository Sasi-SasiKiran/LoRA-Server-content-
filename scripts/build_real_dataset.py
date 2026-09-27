import json
import random
from pathlib import Path

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

random.seed(42)

SYSTEM_PROMPT = (
    "You are a Cloud and Server Operations Specialist. "
    "Analyze infrastructure incidents using evidence, metrics, logs, "
    "events and configuration. Do not guess when evidence is insufficient. "
    "Clearly separate observations, possible causes, verification steps, "
    "root cause and recommended remediation."
)


def make_example(category, situation, evidence, causes, verification, action):
    assistant = (
        f"INCIDENT\n"
        f"{situation}\n\n"
        f"OBSERVED\n"
        f"- No confirmed root cause has been established from the initial report.\n\n"
        f"EVIDENCE NEEDED\n"
        + "\n".join(f"- {x}" for x in evidence)
        + "\n\n"
        f"POSSIBLE CAUSES\n"
        + "\n".join(f"- {x}" for x in causes)
        + "\n\n"
        f"NEEDS VERIFICATION\n"
        f"{verification}\n\n"
        f"LIKELY CAUSE\n"
        f"Cannot be determined until the required evidence is collected.\n\n"
        f"CONFIDENCE\n"
        f"Low\n\n"
        f"RECOMMENDED ACTION\n"
        f"{action}"
    )

    return {
        "category": category,
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": situation
            },
            {
                "role": "assistant",
                "content": assistant
            }
        ]
    }


examples = []


# ============================================================
# 1. LINUX / SERVER OPERATIONS - 50
# ============================================================

linux_scenarios = [
    "A Linux server has very high CPU usage. What should be investigated?",
    "A Linux server is running out of memory. What evidence should be collected?",
    "A server has very high disk utilization. How should it be investigated?",
    "A Linux server has almost no free disk space. What should be checked?",
    "A server becomes slow after running continuously for several days. What should be investigated?",
    "A Linux process is consuming excessive CPU. How should it be diagnosed?",
    "A process is consuming most of the available memory. What should be checked?",
    "A server has unusually high load average. What evidence is needed?",
    "SSH connections to a Linux server are taking a long time. What should be investigated?",
    "A Linux server unexpectedly rebooted. What evidence should be collected?",
    "A service fails to start after reboot. How should the problem be investigated?",
    "A systemd service repeatedly crashes. What should be checked?",
    "A Linux server reports high I/O wait. What should be investigated?",
    "A filesystem suddenly becomes read-only. What evidence should be collected?",
    "A mounted filesystem is inaccessible. What should be investigated?",
    "A scheduled cron job is not executing. What should be checked?",
    "A Linux server has many zombie processes. What should be investigated?",
    "A server has a large number of open files. What should be checked?",
    "A Linux server cannot resolve DNS names. How should this be investigated?",
    "A server cannot reach another internal host. What evidence is required?",
    "A server clock is incorrect. What should be investigated?",
    "NTP synchronization has stopped on a Linux server. What should be checked?",
    "A server's network interface unexpectedly went down. What should be investigated?",
    "A Linux server is dropping network packets. What evidence is needed?",
    "A server has unexpectedly high swap usage. What should be checked?",
    "A server's load average is high but CPU utilization is low. What could explain this?",
    "A Linux server has thousands of running processes. What should be investigated?",
    "A service works manually but fails when started by systemd. What should be checked?",
    "A Linux server reports permission denied for an application. What should be investigated?",
    "A log directory is consuming most of the disk space. What should be checked?",
    "A server has rapidly growing temporary files. What should be investigated?",
    "A Linux application cannot access a required file. What evidence is needed?",
    "A server has unexpectedly high network traffic. What should be investigated?",
    "A Linux server cannot mount a remote filesystem. What should be checked?",
    "A server's hostname resolves incorrectly. What should be investigated?",
    "A Linux service becomes unavailable periodically. What evidence should be collected?",
    "A server experiences intermittent performance degradation. How should it be investigated?",
    "A Linux server has high context switching. What should be checked?",
    "A server has high interrupt activity. What evidence is needed?",
    "A Linux host is reporting kernel errors. What should be investigated?",
    "A server becomes unresponsive during backup operations. What should be checked?",
    "A Linux host has unusually high disk latency. What evidence should be collected?",
    "A server has a growing number of established network connections. What should be investigated?",
    "A Linux server cannot access an external service. What should be checked?",
    "A server has unexpectedly high CPU steal time. What should be investigated?",
    "A Linux virtual machine is slower than expected. What evidence is needed?",
    "A service's response time increases gradually over several hours. What should be investigated?",
    "A server experiences resource exhaustion every night. What evidence should be collected?",
    "A Linux server is generating excessive logs. What should be checked?",
    "A server fails health checks although the operating system is reachable. What should be investigated?",
]

for s in linux_scenarios:
    examples.append(make_example(
        "Linux",
        s,
        [
            "CPU utilization and load average",
            "Memory and swap usage",
            "Disk capacity and I/O latency",
            "Top processes",
            "System and service logs",
            "Recent configuration changes"
        ],
        [
            "Resource exhaustion",
            "Runaway process",
            "Disk or filesystem problem",
            "Network problem",
            "Service failure",
            "Recent configuration change"
        ],
        "Correlate system metrics with process information, service status and logs.",
        "Collect telemetry first, identify the constrained resource and then investigate the related service or process."
    ))


# ============================================================
# 2. DOCKER - 50
# ============================================================

docker_scenarios = [
    "A Docker container repeatedly restarts. What should be investigated?",
    "A Docker container exits with code 137. What should be checked?",
    "A Docker container exits immediately after starting. What evidence is needed?",
    "A Docker health check is failing. How should it be investigated?",
    "A Docker image builds successfully but the container fails at runtime. What should be checked?",
    "A Docker container cannot connect to another container. What should be investigated?",
    "A Docker container cannot resolve another service by hostname. What should be checked?",
    "Docker disk usage is continuously increasing. What should be investigated?",
    "A Docker host is running out of disk space. What should be checked?",
    "A Docker container is consuming excessive CPU. What evidence should be collected?",
    "A Docker container is consuming excessive memory. What should be investigated?",
    "A Docker container has very high network traffic. What should be checked?",
    "A Docker application becomes slow after deployment. What evidence is needed?",
    "A Docker container is healthy but the application is unreachable. What should be investigated?",
    "A Docker port mapping does not work. What should be checked?",
    "A Docker volume cannot be mounted. What evidence should be collected?",
    "A Docker container reports permission denied. What should be investigated?",
    "A Docker application cannot read a mounted configuration file. What should be checked?",
    "A Docker container cannot access the internet. What should be investigated?",
    "A Docker build is extremely slow. What should be checked?",
    "Docker image size has become very large. What should be investigated?",
    "A Docker build fails only in CI. What evidence should be collected?",
    "A Docker container works locally but fails on another host. What should be checked?",
    "Docker logs are growing rapidly. What should be investigated?",
    "A Docker container reaches its memory limit. What should be checked?",
    "A Docker container has frequent CPU throttling. What evidence is needed?",
    "Docker Compose services fail to start together. What should be investigated?",
    "A Docker Compose dependency is unavailable. What should be checked?",
    "A Docker service cannot connect to a database container. What evidence is required?",
    "A Docker container has an incorrect environment variable. What should be checked?",
    "A container starts with the wrong configuration after deployment. What should be investigated?",
    "Docker container startup time has increased significantly. What evidence is needed?",
    "A Docker container loses data after restart. What should be investigated?",
    "A Docker volume contains unexpected data. What should be checked?",
    "Docker networking behaves differently between development and production. What should be investigated?",
    "A container receives intermittent connection failures. What evidence should be collected?",
    "A Docker daemon is consuming excessive resources. What should be checked?",
    "Docker pull operations are failing. What should be investigated?",
    "A private registry authentication fails. What evidence is needed?",
    "Docker image pulls are unusually slow. What should be investigated?",
    "A container's filesystem is filling rapidly. What should be checked?",
    "A Docker application crashes only under load. What evidence should be collected?",
    "A container becomes unhealthy after several hours. What should be investigated?",
    "Docker restart policies are not behaving as expected. What should be checked?",
    "A Docker container cannot access a host service. What should be investigated?",
    "A container has unexpected open ports. What should be checked?",
    "A Docker deployment creates multiple conflicting containers. What evidence is needed?",
    "A container process becomes stuck. What should be investigated?",
    "Docker resource limits appear ineffective. What should be checked?",
    "A Docker host shows many unused resources and containers. What should be investigated?",
]

for s in docker_scenarios:
    examples.append(make_example(
        "Docker",
        s,
        [
            "Container status",
            "Container logs",
            "Exit code",
            "Health-check status",
            "CPU and memory usage",
            "Container configuration",
            "Docker daemon information"
        ],
        [
            "Application crash",
            "Resource limit",
            "Network configuration",
            "Invalid environment configuration",
            "Volume or filesystem problem",
            "Image or runtime problem"
        ],
        "Inspect the container configuration, logs, resource usage and Docker events.",
        "Identify the failing container component from evidence before changing the image, configuration or resource limits."
    ))


# ============================================================
# 3. KUBERNETES - 50
# ============================================================

k8s_scenarios = [
    "A Kubernetes pod is stuck in Pending state. What should be investigated?",
    "A Kubernetes pod repeatedly enters CrashLoopBackOff. What should be checked?",
    "A pod is stuck in ImagePullBackOff. What evidence is needed?",
    "A Kubernetes deployment has unavailable replicas. What should be investigated?",
    "A Kubernetes service has no reachable endpoints. What should be checked?",
    "A pod is running but the application is unreachable. What should be investigated?",
    "A Kubernetes readiness probe is failing. What should be checked?",
    "A Kubernetes liveness probe repeatedly fails. What evidence is needed?",
    "A Kubernetes node reports NotReady. What should be investigated?",
    "A Kubernetes node is under memory pressure. What should be checked?",
    "A Kubernetes node is under disk pressure. What evidence should be collected?",
    "Pods are being evicted from a Kubernetes node. What should be investigated?",
    "A Kubernetes pod is repeatedly OOMKilled. What should be checked?",
    "A Kubernetes application has high CPU usage. What should be investigated?",
    "A Kubernetes application has high memory usage. What evidence is needed?",
    "A Kubernetes deployment rollout is stuck. What should be checked?",
    "A Kubernetes rollout succeeded but users still receive errors. What should be investigated?",
    "A ConfigMap change is not reflected in a running pod. What should be checked?",
    "A Kubernetes Secret is not being loaded by an application. What evidence is needed?",
    "A pod cannot resolve a service name. What should be investigated?",
    "Kubernetes DNS resolution is intermittently failing. What should be checked?",
    "Pods cannot communicate across namespaces. What should be investigated?",
    "A NetworkPolicy blocks application traffic. What evidence is needed?",
    "A Kubernetes ingress returns 502 errors. What should be investigated?",
    "A Kubernetes ingress returns 404 errors. What should be checked?",
    "A service load balancer remains pending. What should be investigated?",
    "A Kubernetes persistent volume is not mounting. What should be checked?",
    "A persistent volume claim remains Pending. What evidence is needed?",
    "A pod cannot write to its mounted volume. What should be investigated?",
    "Kubernetes scheduling is placing pods on unexpected nodes. What should be checked?",
    "A pod cannot be scheduled because of resource constraints. What evidence is needed?",
    "Kubernetes autoscaling is not increasing replicas. What should be investigated?",
    "Horizontal Pod Autoscaler reports unknown metrics. What should be checked?",
    "Kubernetes nodes have uneven workload distribution. What should be investigated?",
    "A DaemonSet is missing pods on some nodes. What should be checked?",
    "A StatefulSet pod is not starting. What evidence is needed?",
    "A Kubernetes job remains active indefinitely. What should be investigated?",
    "A CronJob did not execute. What should be checked?",
    "Kubernetes API requests are slow. What evidence should be collected?",
    "Kubernetes control-plane components report errors. What should be investigated?",
    "A pod starts successfully but terminates unexpectedly. What should be checked?",
    "Kubernetes events show repeated scheduling failures. What evidence is needed?",
    "A namespace is approaching its resource quota. What should be investigated?",
    "A Kubernetes deployment has excessive restart counts. What should be checked?",
    "A pod cannot pull an image from a private registry. What evidence is needed?",
    "Kubernetes service traffic is distributed unevenly. What should be investigated?",
    "A pod receives intermittent network timeouts. What should be checked?",
    "A Kubernetes application becomes slow under load. What evidence should be collected?",
    "A node has unusually high network traffic. What should be investigated?",
    "Kubernetes workloads became unhealthy after a cluster upgrade. What should be checked?",
]

for s in k8s_scenarios:
    examples.append(make_example(
        "Kubernetes",
        s,
        [
            "Pod status and events",
            "Container logs",
            "Node conditions",
            "Resource requests and limits",
            "Service and endpoint information",
            "Probe results",
            "Recent deployment changes"
        ],
        [
            "Insufficient resources",
            "Application failure",
            "Scheduling constraint",
            "Network configuration",
            "Probe failure",
            "Image or configuration problem"
        ],
        "Inspect Kubernetes events, workload status, logs, resource usage and recent changes.",
        "Correlate pod, node, service and event information before changing the workload configuration."
    ))


# ============================================================
# 4. NETWORKING - 50
# ============================================================

network_scenarios = [
    "Users are experiencing high network latency. How should it be investigated?",
    "A server is experiencing packet loss. What should be checked?",
    "DNS resolution has become slow. What evidence is needed?",
    "A service is unreachable from one subnet but reachable from another. What should be investigated?",
    "Network connections are timing out intermittently. What should be checked?",
    "A server cannot reach the internet. What evidence should be collected?",
    "A server can reach IP addresses but cannot resolve hostnames. What should be investigated?",
    "Network interface utilization is near capacity. What should be checked?",
    "A routing change caused connectivity problems. What evidence is needed?",
    "A default gateway is unreachable. What should be investigated?",
    "TCP connections are being reset unexpectedly. What should be checked?",
    "UDP traffic appears to be lost. What evidence should be collected?",
    "A firewall rule change caused application failures. What should be investigated?",
    "A load balancer is returning connection timeouts. What should be checked?",
    "A load balancer reports unhealthy backend servers. What evidence is needed?",
    "Network latency is high only during peak hours. What should be investigated?",
    "A VPN connection is unstable. What should be checked?",
    "A site-to-site VPN has intermittent packet loss. What evidence should be collected?",
    "A server has a large number of TIME_WAIT connections. What should be investigated?",
    "A server has too many open TCP connections. What should be checked?",
    "A port is not reachable even though the service is running. What evidence is needed?",
    "Network traffic suddenly increased after deployment. What should be investigated?",
    "A routing table contains an unexpected route. What should be checked?",
    "A host has duplicate IP address symptoms. What evidence should be collected?",
    "ARP resolution is failing. What should be investigated?",
    "DHCP clients are not receiving addresses. What should be checked?",
    "A VLAN client cannot communicate with another VLAN. What evidence is needed?",
    "IPv6 connectivity is failing while IPv4 works. What should be investigated?",
    "A proxy server is causing application delays. What should be checked?",
    "TLS connections are failing intermittently. What evidence should be collected?",
    "A certificate expiration caused service failures. What should be investigated?",
    "A network interface reports errors and drops. What should be checked?",
    "MTU mismatch is suspected. What evidence is needed?",
    "A service works locally but not remotely. What should be investigated?",
    "Network throughput is lower than expected. What should be checked?",
    "A remote API has high response latency. What evidence should be collected?",
    "Only one application experiences network failures. What should be investigated?",
    "Multiple services suddenly lose connectivity. What should be checked?",
    "Network traffic is being routed through an unexpected path. What evidence is needed?",
    "A DNS server is returning inconsistent responses. What should be investigated?",
    "A firewall is dropping packets unexpectedly. What should be checked?",
    "A NAT gateway is approaching connection limits. What evidence should be collected?",
    "A reverse proxy returns intermittent 502 errors. What should be investigated?",
    "A reverse proxy returns intermittent 504 errors. What should be checked?",
    "Network connections increase continuously over time. What evidence is needed?",
    "A server has high network interrupt activity. What should be investigated?",
    "A service is reachable from the same host but not from containers. What should be checked?",
    "A container network cannot reach a remote subnet. What evidence should be collected?",
    "Network connectivity changed after a firewall deployment. What should be investigated?",
    "Users in one geographic region report slow access. What should be checked?",
]

for s in network_scenarios:
    examples.append(make_example(
        "Networking",
        s,
        [
            "Source and destination",
            "Latency and packet loss",
            "Routing information",
            "DNS resolution results",
            "Interface utilization",
            "Firewall or load-balancer logs",
            "Recent network changes"
        ],
        [
            "Network congestion",
            "Routing problem",
            "Firewall filtering",
            "DNS failure",
            "Packet loss",
            "Service-side latency"
        ],
        "Compare connectivity from multiple locations and correlate network measurements with infrastructure logs.",
        "Identify where latency, loss or filtering begins before changing routing or firewall configuration."
    ))


# ============================================================
# 5. AWS - 50
# ============================================================

aws_scenarios = [
    "An AWS EC2 instance is running slowly. What should be investigated?",
    "An EC2 instance has sustained high CPU utilization. What should be checked?",
    "An EC2 instance is running out of disk space. What evidence is needed?",
    "An EC2 instance cannot reach an S3 bucket. What should be investigated?",
    "An EC2 instance cannot reach the internet. What should be checked?",
    "An EC2 instance is unreachable through SSH. What evidence should be collected?",
    "An EC2 instance suddenly restarted. What should be investigated?",
    "An EC2 application is experiencing high latency. What should be checked?",
    "An EBS volume has high latency. What evidence is needed?",
    "An EBS volume is running out of capacity. What should be investigated?",
    "An application receives intermittent 5xx errors behind an AWS load balancer. What should be checked?",
    "An AWS load balancer reports unhealthy targets. What evidence is needed?",
    "An Auto Scaling Group is not launching instances. What should be investigated?",
    "An Auto Scaling Group is scaling too frequently. What should be checked?",
    "EC2 instances are not registering with a target group. What evidence should be collected?",
    "An S3 application is receiving AccessDenied errors. What should be investigated?",
    "An S3 upload operation is failing intermittently. What should be checked?",
    "An S3 bucket contains unexpected public access. What evidence is needed?",
    "A Lambda function is timing out. What should be investigated?",
    "A Lambda function has high duration. What should be checked?",
    "A Lambda function is hitting its memory limit. What evidence should be collected?",
    "An API Gateway endpoint returns 5xx errors. What should be investigated?",
    "An API Gateway endpoint has increased latency. What should be checked?",
    "An RDS database has high CPU usage. What evidence is needed?",
    "An RDS database has high connection count. What should be investigated?",
    "An RDS database has increasing storage usage. What should be checked?",
    "An RDS application experiences slow queries. What evidence should be collected?",
    "CloudWatch shows a sudden increase in errors. What should be investigated?",
    "An AWS service appears healthy but the application is failing. What should be checked?",
    "An IAM permission change caused an application failure. What evidence is needed?",
    "An EC2 security group change caused connectivity loss. What should be investigated?",
    "A route table change caused an outage. What should be checked?",
    "A NAT gateway has high data processing usage. What evidence should be collected?",
    "A VPC subnet is running out of available IP addresses. What should be investigated?",
    "An ECS task repeatedly stops. What should be checked?",
    "An ECS service has unhealthy tasks. What evidence is needed?",
    "An ECS task cannot access a dependent service. What should be investigated?",
    "An EKS pod cannot access an AWS service. What should be checked?",
    "An EKS node has high resource utilization. What evidence should be collected?",
    "AWS application latency increased after deployment. What should be investigated?",
    "An AWS deployment causes increased error rates. What should be checked?",
    "An AWS resource unexpectedly disappeared. What evidence is needed?",
    "AWS CloudTrail shows unexpected configuration changes. What should be investigated?",
    "AWS costs increased suddenly. What should be checked?",
    "An EC2 instance has unusually high network traffic. What evidence should be collected?",
    "An AWS database connection pool is exhausted. What should be investigated?",
    "A production AWS application is intermittently unavailable. What should be checked?",
    "An AWS health event affects application infrastructure. What evidence is needed?",
    "An EC2 instance has high memory pressure. What should be investigated?",
    "AWS monitoring alerts are firing repeatedly. What should be checked?",
]

for s in aws_scenarios:
    examples.append(make_example(
        "AWS",
        s,
        [
            "CloudWatch metrics",
            "AWS resource status",
            "Application logs",
            "Network configuration",
            "IAM or security configuration",
            "Recent infrastructure changes"
        ],
        [
            "Resource saturation",
            "Network configuration",
            "Permission problem",
            "Application failure",
            "Deployment change",
            "AWS service dependency"
        ],
        "Correlate CloudWatch metrics, application logs and AWS resource configuration.",
        "Identify the affected AWS resource and verify the corresponding metrics and configuration before remediation."
    ))


# ============================================================
# 6. AZURE - 40
# ============================================================

azure_scenarios = [
    "An Azure VM has high CPU utilization. What should be investigated?",
    "An Azure VM is running out of disk space. What should be checked?",
    "An Azure VM cannot be reached through SSH. What evidence is needed?",
    "An Azure VM cannot reach an external service. What should be investigated?",
    "Azure App Service response time has increased. What should be checked?",
    "Azure App Service is returning 5xx errors. What evidence is needed?",
    "An Azure Function is timing out. What should be investigated?",
    "An Azure Function has increased execution duration. What should be checked?",
    "Azure SQL Database has high CPU usage. What evidence should be collected?",
    "Azure SQL Database has high connection count. What should be investigated?",
    "Azure Storage requests are failing. What should be checked?",
    "An Azure Storage account returns authorization errors. What evidence is needed?",
    "Azure Load Balancer health probes are failing. What should be investigated?",
    "Azure Application Gateway returns 502 errors. What should be checked?",
    "Azure Application Gateway latency has increased. What evidence is needed?",
    "An Azure Kubernetes pod is repeatedly restarting. What should be investigated?",
    "An AKS node is under memory pressure. What should be checked?",
    "An AKS service is unreachable. What evidence should be collected?",
    "Azure Monitor shows increased application errors. What should be investigated?",
    "Azure Monitor metrics show high dependency latency. What should be checked?",
    "An Azure deployment caused application failures. What evidence is needed?",
    "Azure networking changed and connectivity was lost. What should be investigated?",
    "A Network Security Group change blocked traffic. What should be checked?",
    "Azure DNS resolution is failing. What evidence should be collected?",
    "An Azure VM has high network utilization. What should be investigated?",
    "An Azure database has slow queries. What should be checked?",
    "An Azure application cannot access Key Vault. What evidence is needed?",
    "Azure Key Vault requests are being denied. What should be investigated?",
    "Azure Container Apps are restarting unexpectedly. What should be checked?",
    "Azure Container Apps have high latency. What evidence should be collected?",
    "Azure autoscaling is not increasing capacity. What should be investigated?",
    "Azure autoscaling triggers too frequently. What should be checked?",
    "An Azure resource shows unexpected configuration changes. What evidence is needed?",
    "Azure Activity Logs show unexpected operations. What should be investigated?",
    "Azure application availability dropped after a release. What should be checked?",
    "Azure VM disk latency increased. What evidence should be collected?",
    "An Azure service dependency is returning intermittent errors. What should be investigated?",
    "Azure monitoring alerts are repeatedly firing. What should be checked?",
    "Azure resource performance changed after resizing. What evidence is needed?",
    "Azure infrastructure has unexpectedly high cost. What should be investigated?",
]

for s in azure_scenarios:
    examples.append(make_example(
        "Azure",
        s,
        [
            "Azure Monitor metrics",
            "Resource health",
            "Application logs",
            "Network configuration",
            "Activity logs",
            "Recent deployments"
        ],
        [
            "Resource saturation",
            "Network filtering",
            "Permission problem",
            "Application failure",
            "Deployment change",
            "Service dependency"
        ],
        "Correlate Azure Monitor telemetry with application logs and resource configuration.",
        "Identify the affected Azure resource and verify telemetry before applying remediation."
    ))


# ============================================================
# 7. GCP - 40
# ============================================================

gcp_scenarios = [
    "A Google Compute Engine VM has high CPU usage. What should be investigated?",
    "A GCE VM is running out of disk space. What should be checked?",
    "A GCE VM cannot reach another internal service. What evidence is needed?",
    "A GCE VM cannot access the internet. What should be investigated?",
    "A Cloud Run service is returning 5xx errors. What should be checked?",
    "A Cloud Run service has increased latency. What evidence is needed?",
    "A Cloud Function is timing out. What should be investigated?",
    "A Cloud Function has high execution duration. What should be checked?",
    "Cloud SQL has high CPU utilization. What evidence should be collected?",
    "Cloud SQL has too many connections. What should be investigated?",
    "A Cloud Storage request returns permission denied. What should be checked?",
    "A Cloud Storage upload is failing. What evidence is needed?",
    "A GKE pod repeatedly restarts. What should be investigated?",
    "A GKE node has memory pressure. What should be checked?",
    "A GKE service is unreachable. What evidence should be collected?",
    "Google Cloud Load Balancing returns 502 errors. What should be investigated?",
    "A Google Cloud load balancer reports unhealthy backends. What should be checked?",
    "Cloud Monitoring shows a sudden error-rate increase. What evidence is needed?",
    "Cloud Monitoring shows increased latency. What should be investigated?",
    "A VPC firewall change caused connectivity loss. What should be checked?",
    "A GCP route change caused an outage. What evidence should be collected?",
    "A GCP application cannot access another project resource. What should be investigated?",
    "A service account permission change caused failures. What should be checked?",
    "GKE workloads cannot access a Google Cloud API. What evidence is needed?",
    "A GCP deployment caused application failures. What should be investigated?",
    "Cloud Run instances are scaling unexpectedly. What should be checked?",
    "GCP autoscaling is not responding to load. What evidence should be collected?",
    "A Compute Engine instance has high network traffic. What should be investigated?",
    "Cloud SQL query latency has increased. What should be checked?",
    "GCP monitoring alerts are firing repeatedly. What evidence is needed?",
    "A GCP service dependency has increased latency. What should be investigated?",
    "GCP resource configuration changed unexpectedly. What should be checked?",
    "Cloud Audit Logs show unexpected operations. What evidence should be collected?",
    "A GCP application became unavailable after a release. What should be investigated?",
    "A GCP VM has high disk latency. What should be checked?",
    "A GKE deployment rollout is stuck. What evidence is needed?",
    "A GKE pod cannot pull an image. What should be investigated?",
    "GCP network traffic increased unexpectedly. What should be checked?",
    "GCP application costs increased suddenly. What evidence should be collected?",
    "A GCP service has intermittent availability problems. What should be investigated?",
]

for s in gcp_scenarios:
    examples.append(make_example(
        "GCP",
        s,
        [
            "Cloud Monitoring metrics",
            "Resource status",
            "Application logs",
            "Network configuration",
            "Audit logs",
            "Recent changes"
        ],
        [
            "Resource saturation",
            "Network configuration",
            "Permission problem",
            "Application failure",
            "Deployment change",
            "Cloud service dependency"
        ],
        "Correlate Cloud Monitoring telemetry, logs and infrastructure configuration.",
        "Verify the affected GCP resource and supporting telemetry before making changes."
    ))


# ============================================================
# 8. MONITORING / PROMETHEUS / GRAFANA - 40
# ============================================================

monitoring_scenarios = [
    "Prometheus is not scraping a target. What should be investigated?",
    "A Prometheus target suddenly becomes unhealthy. What should be checked?",
    "Prometheus scrape latency has increased. What evidence is needed?",
    "Prometheus storage is growing rapidly. What should be investigated?",
    "Prometheus is running out of disk space. What should be checked?",
    "Grafana dashboards stopped showing metrics. What should be investigated?",
    "A Grafana panel shows missing data. What evidence is needed?",
    "A Prometheus query is taking too long. What should be checked?",
    "A Prometheus alert is firing unexpectedly. What should be investigated?",
    "An alert is not firing even though CPU is high. What evidence should be collected?",
    "Monitoring data is delayed. What should be investigated?",
    "Metrics from one server stopped appearing. What should be checked?",
    "A monitoring agent is consuming excessive CPU. What evidence is needed?",
    "A monitoring agent stopped sending metrics. What should be investigated?",
    "Prometheus remote write is failing. What should be checked?",
    "Prometheus retention is consuming too much disk. What evidence is needed?",
    "A Grafana data source is unavailable. What should be investigated?",
    "Grafana authentication is failing. What should be checked?",
    "An alert notification is not being delivered. What evidence is needed?",
    "Monitoring alerts suddenly increased after deployment. What should be investigated?",
    "CPU alerts fire frequently for one server. What should be checked?",
    "Memory alerts fire repeatedly. What evidence should be collected?",
    "Disk alerts are firing unexpectedly. What should be investigated?",
    "Network alerts show packet loss. What should be checked?",
    "Application latency dashboards show a sudden increase. What evidence is needed?",
    "A service-level objective alert is firing. What should be investigated?",
    "Monitoring shows high request rate but normal CPU. What should be checked?",
    "Monitoring shows high CPU but normal request rate. What evidence is needed?",
    "Metrics and logs disagree about service health. What should be investigated?",
    "A dashboard displays stale metrics. What should be checked?",
    "Prometheus configuration changes are not taking effect. What evidence is needed?",
    "A scrape endpoint returns HTTP errors. What should be investigated?",
    "Monitoring data disappears after a server restart. What should be checked?",
    "A recording rule produces unexpected values. What evidence should be collected?",
    "A PromQL query returns incorrect-looking results. What should be investigated?",
    "Monitoring cardinality has increased significantly. What should be checked?",
    "A Prometheus server has high memory usage. What evidence is needed?",
    "Grafana dashboards load slowly. What should be investigated?",
    "Alert evaluation latency has increased. What should be checked?",
    "Monitoring coverage is missing for a newly deployed service. What evidence should be collected?",
]

for s in monitoring_scenarios:
    examples.append(make_example(
        "Monitoring",
        s,
        [
            "Prometheus target status",
            "Scrape metrics",
            "PromQL query results",
            "Grafana data-source status",
            "Monitoring server resource usage",
            "Alert history",
            "Recent configuration changes"
        ],
        [
            "Scrape failure",
            "Monitoring resource saturation",
            "Incorrect configuration",
            "Query problem",
            "Target availability problem",
            "Alert configuration problem"
        ],
        "Compare target health, scrape results, monitoring logs and recent configuration changes.",
        "Verify whether the problem originates from the target, collector, query or visualization layer."
    ))


# ============================================================
# 9. DATABASE - 35
# ============================================================

database_scenarios = [
    "A database has very high CPU usage. What should be investigated?",
    "Database query latency has suddenly increased. What should be checked?",
    "A database has too many active connections. What evidence is needed?",
    "A connection pool is exhausted. What should be investigated?",
    "A database is running out of storage. What should be checked?",
    "Database disk I/O latency is high. What evidence should be collected?",
    "A database query is consuming excessive CPU. What should be investigated?",
    "A database has frequent deadlocks. What should be checked?",
    "Transactions are waiting for locks. What evidence is needed?",
    "A database replication lag has increased. What should be investigated?",
    "A replica has stopped receiving updates. What should be checked?",
    "Database backups are taking too long. What evidence should be collected?",
    "Database backups are failing. What should be investigated?",
    "An application cannot connect to the database. What should be checked?",
    "Database connections are being reset. What evidence is needed?",
    "Database performance is slow only during peak traffic. What should be investigated?",
    "A database has unexpectedly high memory usage. What should be checked?",
    "Database cache hit ratio has decreased. What evidence should be collected?",
    "A database table has grown rapidly. What should be investigated?",
    "Database logs show repeated errors. What should be checked?",
    "A schema migration caused application errors. What evidence is needed?",
    "Database queries became slower after an index change. What should be investigated?",
    "An index appears unused. What should be checked?",
    "A database connection timeout occurs intermittently. What evidence should be collected?",
    "Database replication is delayed after deployment. What should be investigated?",
    "A database instance was restarted unexpectedly. What should be checked?",
    "Database storage latency increased after workload growth. What evidence is needed?",
    "An application is generating excessive database queries. What should be investigated?",
    "A database has a sudden increase in failed queries. What should be checked?",
    "Database locks remain active for a long time. What evidence should be collected?",
    "A database replica is reporting inconsistent performance. What should be investigated?",
    "Database CPU is normal but query latency is high. What should be checked?",
    "Database CPU is high but traffic is normal. What evidence is needed?",
    "A database service is healthy but applications cannot connect. What should be investigated?",
    "Database performance degraded after a configuration change. What should be checked?",
]

for s in database_scenarios:
    examples.append(make_example(
        "Database",
        s,
        [
            "CPU and memory usage",
            "Connection count",
            "Query latency",
            "Disk I/O",
            "Database logs",
            "Lock and transaction information",
            "Recent schema or configuration changes"
        ],
        [
            "Resource saturation",
            "Slow query",
            "Lock contention",
            "Connection exhaustion",
            "Storage limitation",
            "Configuration or schema change"
        ],
        "Correlate database metrics, active queries, locks, logs and recent changes.",
        "Identify the database resource or workload responsible before changing indexes, configuration or capacity."
    ))


# ============================================================
# 10. SECURITY - 30
# ============================================================

security_scenarios = [
    "A server shows an unexpected increase in failed SSH logins. What should be investigated?",
    "A cloud resource configuration changed unexpectedly. What evidence is needed?",
    "An application suddenly receives many authentication failures. What should be checked?",
    "A service account is generating unexpected API calls. What should be investigated?",
    "A production server shows an unexpected new process. What evidence should be collected?",
    "A firewall rule was changed unexpectedly. What should be checked?",
    "A user reports unauthorized access to an application. What should be investigated?",
    "A server is communicating with an unknown external address. What evidence is needed?",
    "An API key may have been exposed. What should be investigated?",
    "Cloud audit logs show unusual administrative activity. What should be checked?",
    "A database account shows unexpected login attempts. What evidence should be collected?",
    "A container is running with excessive privileges. What should be investigated?",
    "A Kubernetes workload is using privileged access unexpectedly. What should be checked?",
    "A server certificate is close to expiration. What should be investigated?",
    "TLS certificate validation is failing. What evidence is needed?",
    "A production secret may have been exposed in logs. What should be checked?",
    "An IAM permission change caused unexpected access. What should be investigated?",
    "A security alert indicates unusual network traffic. What evidence should be collected?",
    "A server has an unexpected listening port. What should be investigated?",
    "A cloud storage resource became publicly accessible. What should be checked?",
    "A service suddenly begins making many authentication requests. What evidence is needed?",
    "A user account is locked repeatedly. What should be investigated?",
    "An application reports repeated authorization failures. What should be checked?",
    "A security monitoring agent stopped reporting. What evidence should be collected?",
    "A host firewall is disabled unexpectedly. What should be investigated?",
    "A new privileged account appeared on a server. What should be checked?",
    "Audit logs stopped arriving. What evidence is needed?",
    "An application secret rotation caused failures. What should be investigated?",
    "A security policy change caused service connectivity problems. What should be checked?",
    "A server has suspicious resource consumption. What evidence should be collected?",
]

for s in security_scenarios:
    examples.append(make_example(
        "Security",
        s,
        [
            "Authentication and authorization logs",
            "Audit events",
            "Process and network information",
            "Firewall configuration",
            "Identity activity",
            "Recent configuration changes"
        ],
        [
            "Credential problem",
            "Unauthorized configuration change",
            "Excessive permissions",
            "Unexpected network activity",
            "Secret or certificate problem",
            "Security monitoring failure"
        ],
        "Correlate audit logs, identity events, process activity and network telemetry.",
        "Preserve evidence, identify the affected identity or resource and verify the event timeline before remediation."
    ))


# ============================================================
# 11. CI/CD AND DEPLOYMENT - 30
# ============================================================

deployment_scenarios = [
    "A production deployment failed. What evidence should be collected?",
    "A CI pipeline fails during the build stage. What should be investigated?",
    "A deployment succeeds but the application is unhealthy. What should be checked?",
    "A deployment causes a sudden increase in error rate. What evidence is needed?",
    "A deployment is stuck waiting for resources. What should be investigated?",
    "A container image builds in CI but fails in production. What should be checked?",
    "A deployment works in staging but fails in production. What evidence should be collected?",
    "A rollback does not restore application health. What should be investigated?",
    "A deployment causes increased latency. What should be checked?",
    "A release causes database connection errors. What evidence is needed?",
    "A pipeline cannot access a required secret. What should be investigated?",
    "A CI job suddenly takes much longer than before. What should be checked?",
    "A deployment creates unhealthy containers. What evidence should be collected?",
    "A production service becomes unavailable after configuration changes. What should be investigated?",
    "A deployment succeeds but new code is not running. What should be checked?",
    "A release causes memory usage to increase. What evidence is needed?",
    "A release causes CPU usage to increase. What should be investigated?",
    "A pipeline fails only on one runner. What should be checked?",
    "A deployment artifact is missing. What evidence should be collected?",
    "A release is blocked by failed health checks. What should be investigated?",
    "A canary deployment shows increased errors. What should be checked?",
    "A blue-green deployment has inconsistent traffic. What evidence is needed?",
    "A deployment causes network connectivity failures. What should be investigated?",
    "A migration step fails during deployment. What should be checked?",
    "A deployment timeout occurs repeatedly. What evidence should be collected?",
    "A CI dependency download fails intermittently. What should be investigated?",
    "A deployment environment has unexpected configuration. What should be checked?",
    "A release causes unexpected log volume. What evidence is needed?",
    "A production deployment passes tests but fails runtime health checks. What should be investigated?",
    "A deployment rollback leaves some instances on the old version. What should be checked?",
]

for s in deployment_scenarios:
    examples.append(make_example(
        "Deployment",
        s,
        [
            "Pipeline logs",
            "Deployment status",
            "Application logs",
            "Health-check results",
            "Runtime metrics",
            "Artifact information",
            "Recent configuration changes"
        ],
        [
            "Build failure",
            "Configuration mismatch",
            "Application regression",
            "Dependency problem",
            "Health-check failure",
            "Deployment inconsistency"
        ],
        "Correlate pipeline logs, deployment events, application health and runtime telemetry.",
        "Identify the failed lifecycle stage before retrying, rolling back or changing configuration."
    ))


# ============================================================
# 12. INCIDENT RESPONSE / RCA - 35
# ============================================================

rca_scenarios = [
    "A production service is unavailable and no root cause is known. How should the investigation begin?",
    "A server became slow without any obvious configuration change. What evidence is needed?",
    "An application has intermittent failures. How should the incident be investigated?",
    "A service recovered before engineers could inspect it. What evidence should be collected?",
    "Several services failed at approximately the same time. What should be investigated?",
    "A performance incident started shortly after a deployment. What evidence is needed?",
    "An outage affects only one region. What should be investigated?",
    "An incident affects only one customer group. What evidence should be collected?",
    "CPU, memory and disk metrics are normal but the application is slow. What should be investigated?",
    "Logs show errors but no infrastructure metrics changed. What evidence is needed?",
    "Infrastructure metrics changed but application logs show no errors. What should be investigated?",
    "A service repeatedly recovers without manual intervention. What evidence should be collected?",
    "An alert fired but the service appears healthy. What should be investigated?",
    "A service appears unhealthy but no monitoring alert fired. What should be checked?",
    "An incident occurs at the same time every day. What evidence is needed?",
    "A problem occurs only under high traffic. What should be investigated?",
    "A problem cannot be reproduced in staging. What evidence should be collected?",
    "A production issue has multiple possible causes. How should they be prioritized for investigation?",
    "A service fails after a configuration change but the exact cause is unknown. What should be checked?",
    "A server has unusual behavior with insufficient telemetry. What should be done first?",
    "A dependency is suspected of causing an outage. What evidence is needed?",
    "Several alerts fire simultaneously. How should the incident be analyzed?",
    "An application returns errors only for some requests. What should be investigated?",
    "An outage started during a scheduled maintenance window. What evidence should be collected?",
    "A service has gradually degraded over several hours. What should be investigated?",
    "A sudden outage has no obvious deployment associated with it. What evidence is needed?",
    "An incident affects multiple hosts but only one application. What should be investigated?",
    "An incident affects multiple applications on the same host. What evidence should be collected?",
    "An application is healthy but users report failures. What should be investigated?",
    "Monitoring data is incomplete during an incident. How should the investigation proceed?",
    "An incident has already been mitigated. What evidence should be preserved for RCA?",
    "A root cause is suspected but not yet verified. How should it be reported?",
    "An incident investigation has conflicting evidence. What should be done?",
    "A remediation was applied but the incident returned. What evidence is needed?",
    "An incident requires determining whether infrastructure or application changes caused it. How should this be investigated?",
]

for s in rca_scenarios:
    examples.append(make_example(
        "Incident Response",
        s,
        [
            "Incident timeline",
            "System metrics",
            "Application logs",
            "Infrastructure events",
            "Recent deployments",
            "Configuration changes",
            "Dependency health"
        ],
        [
            "Resource saturation",
            "Application regression",
            "Infrastructure failure",
            "Dependency failure",
            "Configuration change",
            "Unknown cause requiring additional evidence"
        ],
        "Build a timeline and correlate metrics, logs, events and changes. Do not select a root cause without supporting evidence.",
        "Preserve evidence, establish the incident timeline, test competing hypotheses and verify the suspected cause before declaring RCA."
    ))


# ============================================================
# VERIFY TOTAL
# ============================================================

print(f"Total unique scenarios: {len(examples)}")

if len(examples) != 500:
    raise RuntimeError(
        f"Expected exactly 500 examples, but generated {len(examples)}"
    )


# ============================================================
# SHUFFLE AND SPLIT
# ============================================================

random.shuffle(examples)

train = examples[:400]
validation = examples[400:450]
test = examples[450:500]


def write_jsonl(path, data):
    with open(path, "w", encoding="utf-8") as f:
        for item in data:
            item.pop("category", None)
            f.write(json.dumps(item, ensure_ascii=False) + "\n")


write_jsonl(DATA_DIR / "train.jsonl", train)
write_jsonl(DATA_DIR / "validation.jsonl", validation)
write_jsonl(DATA_DIR / "test.jsonl", test)


print()
print("BALANCED DATASET CREATED")
print("========================")
print(f"Training examples:   {len(train)}")
print(f"Validation examples: {len(validation)}")
print(f"Test examples:       {len(test)}")
print(f"Total examples:      {len(train) + len(validation) + len(test)}")