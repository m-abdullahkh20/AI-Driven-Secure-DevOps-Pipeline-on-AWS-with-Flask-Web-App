# AI-Driven Secure DevOps Pipeline

This project demonstrates the deployment of a Flask web application utilizing pre-trained AI models on AWS. The pipeline incorporates Docker, Kubernetes, and CI/CD practices to ensure a secure, automated, and scalable deployment. The solution adheres to best security practices and PCI DSS compliance standards.

## Project Overview

1. **Flask Application**: Developed a Flask application integrated with pre-trained AI models.
2. **Dockerization**: Created a Dockerfile to containerize the application.
3. **Amazon ECR**: Pushed the Docker image to Amazon Elastic Container Registry (ECR).
4. **Database Setup**: Configured a MySQL database using Amazon RDS.
5. **Kubernetes Deployment**: Deployed the application on an Amazon EKS cluster.
6. **CI/CD Pipeline**: Implemented an automated CI/CD pipeline using AWS CodePipeline.
7. **Monitoring**: Set up monitoring and logging using AWS CloudWatch.
8. **Security**: Applied security best practices, including VPC configuration, security groups, IAM roles, and database privatization.

## Features

- **AI Integration**: Utilizes pre-trained AI models for advanced functionalities.
- **Secure Deployment**: Implements Docker, Kubernetes, and CI/CD practices.
- **Database Management**: Uses Amazon RDS for scalable and reliable database services.
- **Monitoring & Logging**: Monitors application performance and logs using AWS CloudWatch.
- **Security Compliance**: Ensures PCI DSS compliance and implements security best practices.

## Architecture

1. **Source Code**: Flask application with pre-trained AI models.
2. **Build Process**: Dockerfile used to containerize the application.
3. **Container Registry**: Docker image stored in Amazon ECR.
4. **Deployment**: Application deployed on Amazon EKS.
5. **CI/CD**: Automated pipeline using AWS CodePipeline.
6. **Monitoring**: AWS CloudWatch for performance and logging.

## Setup Instructions

### Prerequisites

- AWS Account
- GitHub Repository
- Docker
- AWS CLI
- kubectl

### Steps

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/AI-Driven-Secure-DevOps-Pipeline.git
    cd AI-Driven-Secure-DevOps-Pipeline
    ```

2. **Build and Push Docker Image**:
    ```bash
    docker build -t flask-app .
    docker tag flask-app:latest <aws_account_id>.dkr.ecr.<region>.amazonaws.com/flask-app:latest
    aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.<region>.amazonaws.com
    docker push <aws_account_id>.dkr.ecr.<region>.amazonaws.com/flask-app:latest
    ```

3. **Create RDS Database**:
    - Follow AWS RDS documentation to create and configure a MySQL database instance.

4. **Set Up EKS Cluster**:
    - Use AWS EKS to create and configure the Kubernetes cluster.

5. **Deploy Application**:
    ```bash
    kubectl apply -f deployment.yaml
    ```

6. **Configure CI/CD**:
    - Set up AWS CodePipeline to automate the build, test, and deploy processes.

7. **Set Up Monitoring**:
    - Configure AWS CloudWatch for logging and monitoring application performance.

8. **Apply Security Best Practices**:
    - Create a custom VPC with public and private subnets.
    - Configure Security Groups and IAM roles.
    - Ensure database is private and secure.

## Security Features

- **IAM Roles**: Adheres to least privilege principles.
- **Custom VPC**: Segregates application components into public and private subnets.
- **Data Encryption**: Ensures encryption of data at rest using AWS KMS.
- **Security Groups**: Controls inbound and outbound traffic.
- **PCI DSS Compliance**: Meets standards for handling sensitive payment information.



## Acknowledgements

- Special thanks to the team for their contributions and dedication.


