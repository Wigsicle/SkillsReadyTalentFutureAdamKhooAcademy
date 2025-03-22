## Project Architecture
- SRTFAKA Backend
    - Gateway: apiGateway
    - Services:
        - accountService
        - assessmentService
        - courseService
        - certificateService
        - jobService
- These components are dockerized in addition with the Citus Database
- They exist within a Docker Network on the subnet: 172.18.0.0/16

## Installation & Execution of Application
- In the directory where "docker-compose.yml" is, run the following:
    - docker compose up

## Service IPs and Ports
Below is a list of the services, their assigned IP addresses, and exposed ports.

| **Service**            | **Container Name**     | **IP Address**  | **Port (Host:Container)** |
|------------------------|-----------------------|----------------|---------------------------|
| **Job Database**       | `SRTFAKA_database`    | `172.18.0.2`   | `5433:5432`               |
| **API Gateway**        | `apiGateway`          | `172.18.0.3`   | `80:80`                   |
| **Account Service**    | `accountService`      | `172.18.0.4`   | `50051:50051`             |
| **Assessment Service** | `assessmentService`   | `172.18.0.5`   | `50053:50053`             |
| **Certificate Service**| `certificateService`  | `172.18.0.6`   | `50055:50055`             |
| **Course Service**     | `courseService`       | `172.18.0.7`   | `50052:50052`             |
| **Job Service**        | `jobService`          | `172.18.0.8`   | `50054:50054`             |

> **Note:** These services are running on the `gateway_network` with subnet `172.18.0.0/16`.  
> Inside Docker, use the IP addresses directly. From the host machine, use `localhost` with the host port.
- If you encounter an issue with conflicting Docker network during initialization, either remove the conflicted network or change the network subnet in the Docker Compose file.

## API Routes Documentation
- Located at http://localhost/docs

## Front End Page
- Located at http://localhost

## Features
- Registration
- Login
- User Profile
- Courses
- Assessments
- Certifications
- Job applications

## Other Notes
- Postgres Conflict
    - Ensure that all Postgres instances on local and within Docker are down before running this system
