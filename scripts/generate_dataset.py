import json
import random
from pathlib import Path

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

SYSTEM_MESSAGE = (
    "You are a Cloud and Server Operations Specialist. "
    "Analyze infrastructure incidents using evidence, metrics, logs, "
    "events and configuration. Do not guess when evidence is insufficient. "
    "Clearly separate observations, possible causes, verification steps, "
    "root cause and recommended remediation."
)

random.seed(42)


def create_example(user, assistant):
    return {
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_MESSAGE
            },
            {
                "role": "user",
                "content": user
            },
            {
                "role": "assistant",
                "content": assistant
            }
        ]
    }


examples = [

    # =========================
    # LINUX / SERVER OPERATIONS
    # =========================

    create_example(
        "A Linux server has very high CPU utilization. What should be checked first?",
        """INCIDENT
High CPU utilization.

OBSERVED
CPU utilization is very high.

EVIDENCE NEEDED
Check process-level CPU usage, load average, running services, recent deployments, scheduled jobs and system logs.

POSSIBLE CAUSES
- Runaway process
- Increased application traffic
- Scheduled task
- Resource-intensive application
- Recent software deployment

NEEDS VERIFICATION
Identify which process is consuming CPU and correlate it with recent system or application changes.

RECOMMENDED ACTION
Use top, htop or ps to identify CPU-intensive processes before taking corrective action."""
    ),

    create_example(
        "A Linux server suddenly becomes slow. What information should be collected?",
        """INCIDENT
Server performance degradation.

OBSERVED
The server is reported to be slow, but the root cause is unknown.

EVIDENCE NEEDED
- CPU utilization
- Load average
- Memory and swap usage
- Disk utilization
- Disk I/O latency
- Network latency
- Running processes
- Application logs
- System logs
- Recent configuration or deployment changes

POSSIBLE CAUSES
CPU, memory, disk, network, application or dependency problems.

NEEDS VERIFICATION
Collect metrics and logs before identifying the root cause.

RECOMMENDED ACTION
Correlate resource metrics with application behavior and recent changes."""
    ),

    create_example(
        "How can I find which process is consuming the most memory on Linux?",
        """OBSERVATION
The objective is to identify memory-intensive processes.

EVIDENCE NEEDED
Process-level memory utilization.

RECOMMENDED ACTION
Use commands such as:

ps aux --sort=-%mem

or:

top

or:

htop

Then identify whether the process is expected and check its recent behavior before terminating it."""
    ),

    create_example(
        "A Linux server has a high load average. Does this always mean CPU usage is high?",
        """ANSWER
No.

OBSERVED
A high load average indicates that processes are waiting for CPU time or other resources.

POSSIBLE CAUSES
- CPU saturation
- Disk I/O wait
- Other resource contention

NEEDS VERIFICATION
Compare load average with CPU utilization, CPU idle time, I/O wait and disk latency.

RECOMMENDED ACTION
Do not conclude that CPU is the root cause from load average alone."""
    ),

    create_example(
        "A server disk is almost full. What should an operations engineer investigate?",
        """INCIDENT
High disk utilization.

EVIDENCE NEEDED
- Filesystem utilization
- Largest directories
- Large log files
- Temporary files
- Container images and volumes
- Application-generated data
- Database files

POSSIBLE CAUSES
- Log growth
- Application data growth
- Old backups
- Temporary files
- Docker images or volumes

NEEDS VERIFICATION
Identify what is consuming the disk before deleting anything.

RECOMMENDED ACTION
Use df -h to identify full filesystems and du to locate large directories. Clean up only after confirming that the data is safe to remove."""
    ),

    # =========================
    # DOCKER
    # =========================

    create_example(
        "A Docker container repeatedly restarts. What should I check?",
        """INCIDENT
Container restart loop.

EVIDENCE NEEDED
- Container status
- Exit code
- Container logs
- Health-check status
- Memory usage
- Environment variables
- Recent image changes

POSSIBLE CAUSES
- Application crash
- Failed health check
- Out-of-memory condition
- Invalid configuration
- Missing environment variable
- Dependency unavailable

NEEDS VERIFICATION
Inspect docker logs and docker inspect output.

RECOMMENDED ACTION
Check docker ps, docker logs and docker inspect. Determine the exit code and correlate it with application logs before applying remediation."""
    ),

    create_example(
        "A Docker container exits immediately after starting. What should be investigated?",
        """INCIDENT
Container exits immediately.

EVIDENCE NEEDED
- Container exit code
- Container logs
- Entrypoint
- CMD configuration
- Environment variables
- Required dependencies

POSSIBLE CAUSES
- Application exits because of an error
- Incorrect entrypoint
- Missing configuration
- Missing dependency
- Invalid command

NEEDS VERIFICATION
Check docker logs and docker inspect.

RECOMMENDED ACTION
Identify the exit code and application error before modifying the container configuration."""
    ),

    create_example(
        "How can I check Docker container resource usage?",
        """OBSERVATION
Docker provides runtime resource information for containers.

RECOMMENDED ACTION
Use:

docker stats

This can show CPU usage, memory usage, network I/O and block I/O.

For a complete diagnosis, correlate these metrics with container logs and application behavior."""
    ),

    create_example(
        "A Docker container is using excessive memory. What should be checked?",
        """INCIDENT
High container memory usage.

EVIDENCE NEEDED
- Current memory usage
- Memory limit
- Application logs
- Container restart history
- Process-level memory usage
- Recent application changes

POSSIBLE CAUSES
- Memory leak
- Increased workload
- Incorrect memory configuration
- Application cache growth

NEEDS VERIFICATION
Determine whether memory usage continuously increases or corresponds to workload.

RECOMMENDED ACTION
Inspect docker stats and application logs, then determine whether the application or container configuration is responsible."""
    ),

    # =========================
    # KUBERNETES
    # =========================

    create_example(
        "A Kubernetes pod is stuck in CrashLoopBackOff. What should be investigated?",
        """INCIDENT
Pod is repeatedly crashing.

EVIDENCE NEEDED
- Pod logs
- Previous container logs
- Exit code
- Pod events
- Resource limits
- Configuration
- Secrets and environment variables
- Dependency availability

POSSIBLE CAUSES
- Application crash
- Configuration error
- Missing secret
- Failed dependency
- Out-of-memory condition
- Failed health check

NEEDS VERIFICATION
Use kubectl describe pod and kubectl logs to identify the failure.

RECOMMENDED ACTION
Collect pod events and logs before changing the deployment."""
    ),

    create_example(
        "A Kubernetes pod is in Pending state. What should I check?",
        """INCIDENT
Pod cannot be scheduled.

EVIDENCE NEEDED
- Pod events
- Available node resources
- Node taints
- Pod resource requests
- Node selectors
- Affinity rules

POSSIBLE CAUSES
- Insufficient CPU or memory
- Node taint
- Scheduling constraints
- Resource requests too large

NEEDS VERIFICATION
Check:

kubectl describe pod

and inspect scheduler events.

RECOMMENDED ACTION
Determine the scheduling constraint causing the pod to remain Pending before changing the deployment."""
    ),

    create_example(
        "A Kubernetes service is not reachable. What should be investigated?",
        """INCIDENT
Kubernetes service connectivity failure.

EVIDENCE NEEDED
- Service configuration
- Service selectors
- Endpoint objects
- Pod readiness
- Network policies
- DNS resolution
- Ingress configuration if applicable

POSSIBLE CAUSES
- Incorrect selector
- No healthy endpoints
- Network policy
- DNS failure
- Ingress configuration problem

NEEDS VERIFICATION
Confirm that the service has healthy endpoints and that the selected pods are Ready.

RECOMMENDED ACTION
Inspect the Service, Endpoints or EndpointSlices, pod readiness and relevant network policies."""
    ),

    # =========================
    # NETWORKING
    # =========================

    create_example(
        "Users are experiencing high network latency. How should it be investigated?",
        """INCIDENT
Network latency is elevated.

EVIDENCE NEEDED
- Source and destination
- Round-trip latency
- Packet loss
- Network interface utilization
- Routing path
- DNS resolution time
- Recent network changes

POSSIBLE CAUSES
- Network congestion
- Routing problem
- Packet loss
- DNS delay
- Overloaded network interface
- External dependency latency

NEEDS VERIFICATION
Compare latency across multiple endpoints and inspect packet loss and routing.

RECOMMENDED ACTION
Use ping, traceroute or equivalent monitoring tools and correlate the results with network metrics."""
    ),

    create_example(
        "A server cannot resolve a domain name. What should be checked?",
        """INCIDENT
DNS resolution failure.

EVIDENCE NEEDED
- DNS configuration
- Resolver availability
- Domain record
- Network connectivity
- DNS response code

POSSIBLE CAUSES
- Incorrect DNS configuration
- DNS server unavailable
- Missing DNS record
- Network connectivity problem

NEEDS VERIFICATION
Test DNS resolution using tools such as nslookup or dig.

RECOMMENDED ACTION
Verify the configured DNS resolver and determine whether the failure is local, resolver-side or authoritative DNS related."""
    ),

    # =========================
    # AWS
    # =========================

    create_example(
        "An AWS EC2 instance is running slowly. What should be investigated?",
        """INCIDENT
EC2 performance degradation.

EVIDENCE NEEDED
- CPU utilization
- Memory utilization
- Disk I/O
- Network performance
- Instance type
- EBS metrics
- Application logs
- Recent deployments

POSSIBLE CAUSES
- CPU saturation
- Memory pressure
- EBS performance limitation
- Network limitation
- Application problem

NEEDS VERIFICATION
Correlate CloudWatch metrics with operating-system and application metrics.

RECOMMENDED ACTION
Determine which resource is constrained before resizing or replacing the instance."""
    ),

    create_example(
        "An AWS EC2 instance is unreachable. What should be checked?",
        """INCIDENT
EC2 connectivity failure.

EVIDENCE NEEDED
- Instance state
- System status checks
- Instance status checks
- Security group rules
- Network ACLs
- Route tables
- Subnet configuration
- Operating-system state

POSSIBLE CAUSES
- Instance stopped
- System failure
- Security group restriction
- Network ACL restriction
- Routing problem
- Operating-system failure

NEEDS VERIFICATION
Check EC2 status checks and network configuration before restarting the instance.

RECOMMENDED ACTION
Determine whether the failure is at the AWS infrastructure, network or operating-system layer."""
    ),

    # =========================
    # PROMETHEUS / MONITORING
    # =========================

    create_example(
        "Prometheus shows a sudden increase in CPU utilization. What should be done?",
        """INCIDENT
CPU utilization alert.

OBSERVED
Prometheus reports increased CPU usage.

EVIDENCE NEEDED
- CPU utilization over time
- Load average
- Process-level metrics
- Application request rate
- Recent deployments
- Related alerts

POSSIBLE CAUSES
- Increased traffic
- Application regression
- Background job
- Resource leak
- Infrastructure issue

NEEDS VERIFICATION
Correlate CPU metrics with traffic, deployments and process-level metrics.

RECOMMENDED ACTION
Investigate the time correlation rather than treating the CPU metric alone as proof of the root cause."""
    ),

    create_example(
        "What is the purpose of Prometheus in server monitoring?",
        """ANSWER
Prometheus is a monitoring and time-series data system.

It collects and stores numerical metrics over time and supports querying those metrics.

COMMON USES
- Infrastructure monitoring
- Application monitoring
- Alerting
- Capacity analysis
- Performance investigation

RECOMMENDED APPROACH
Use Prometheus metrics together with logs and traces when investigating incidents."""
    ),

    # =========================
    # DATABASE
    # =========================

    create_example(
        "An application reports database connection errors. What should be checked?",
        """INCIDENT
Database connectivity failure.

EVIDENCE NEEDED
- Database availability
- Connection pool usage
- Maximum connection limit
- Application configuration
- Network connectivity
- Database logs
- Query performance

POSSIBLE CAUSES
- Connection pool exhaustion
- Database unavailable
- Incorrect credentials
- Network failure
- Connection limit reached

NEEDS VERIFICATION
Determine whether the database is reachable and whether the application has exhausted its connection pool.

RECOMMENDED ACTION
Check application and database metrics before restarting either service."""
    ),

    # =========================
    # SECURITY
    # =========================

    create_example(
        "A server shows an unexpected increase in failed SSH login attempts. What should be investigated?",
        """INCIDENT
Increase in failed SSH authentication attempts.

EVIDENCE NEEDED
- Source IP addresses
- Attempt frequency
- Authentication logs
- Successful login events
- Exposed SSH configuration
- User accounts involved

POSSIBLE CAUSES
- Automated scanning
- Brute-force attempts
- Misconfigured client
- Compromised credentials

NEEDS VERIFICATION
Correlate authentication logs with source addresses and successful login events.

RECOMMENDED ACTION
Review authentication logs, restrict unnecessary exposure, enforce strong authentication and investigate any successful unexpected logins."""
    ),

    # =========================
    # INCIDENT / RCA
    # =========================

    create_example(
        "A production application returns HTTP 503 errors. What should an operations engineer investigate?",
        """INCIDENT
HTTP 503 Service Unavailable errors.

EVIDENCE NEEDED
- Error rate over time
- Load balancer metrics
- Application health
- Backend availability
- Container or pod status
- CPU and memory usage
- Recent deployments
- Application logs

POSSIBLE CAUSES
- Backend unavailable
- Application overload
- Failed deployment
- Health-check failure
- Dependency outage

NEEDS VERIFICATION
Determine whether the 503 responses originate from the load balancer, gateway or application.

RECOMMENDED ACTION
Correlate HTTP errors with backend health, deployment events and infrastructure metrics."""
    ),

    create_example(
        "The server is slow. Can you identify the root cause from this information alone?",
        """INSUFFICIENT EVIDENCE

The available information is not sufficient to determine the root cause.

EVIDENCE NEEDED
- CPU utilization
- Load average
- Memory utilization
- Swap usage
- Disk utilization
- Disk I/O latency
- Network latency
- Process-level resource usage
- Application logs
- System logs
- Recent changes

RECOMMENDED ACTION
Collect and correlate these signals before assigning a root cause."""
    ),
]


def save_jsonl(path, data):
    with open(path, "w", encoding="utf-8") as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")


def main():
    print(f"Base examples created: {len(examples)}")

    # Duplicate examples with slight variation only to create a working
    # dataset structure. These should later be replaced with additional
    # reviewed examples rather than blindly relying on duplicates.
    expanded = []

    for item in examples:
        expanded.append(item)

    while len(expanded) < 500:
        item = random.choice(examples)
        expanded.append(item.copy())

    random.shuffle(expanded)

    train = expanded[:400]
    validation = expanded[400:450]
    test = expanded[450:500]

    save_jsonl(DATA_DIR / "train.jsonl", train)
    save_jsonl(DATA_DIR / "validation.jsonl", validation)
    save_jsonl(DATA_DIR / "test.jsonl", test)

    print("Dataset generated.")
    print(f"Training examples: {len(train)}")
    print(f"Validation examples: {len(validation)}")
    print(f"Test examples: {len(test)}")


if __name__ == "__main__":
    main()