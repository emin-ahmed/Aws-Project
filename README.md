# 🗂️ Project 1 – Scalable Web Application Infrastructure on AWS

This repository contains:

✅ An AWS **CloudFormation** template to deploy a **production-grade, highly available web application infrastructure**  
✅ A simple **Flask-based TODO app** to demonstrate deployment on this infrastructure

---

## 📜 Overview

The project automates the creation of a complete, production-style AWS architecture:

- **VPC** with public and private subnets across multiple Availability Zones
- **Application Load Balancer (ALB)**
- **Auto Scaling Group (ASG)** with EC2 instances running the app
- **Amazon RDS** (MySQL) in private subnets
- **CloudWatch** Logs and Alarms
- **IAM Roles and Security Groups**

It is designed to meet these **acceptance criteria**:

- All resources are appropriately tagged
- The application is accessible via the ALB endpoint
- The RDS instance is private and secure
- Auto scaling triggers based on CPU utilization
- Logs are visible in CloudWatch
- Infrastructure is defined as code (CloudFormation)
- App and infrastructure code are version-controlled in this repo

---

## 📦 Repository Structure

├── project-1.yml # CloudFormation template

└── todo-app/

├── app.py

└── templates/

  └── index.html



---

## 🗺️ Architecture Diagram

Below is the architecture deployed by the CloudFormation template:

![AWS Architecture Diagram](architecture.png)

✅ **Explanation**:

- **Public Subnets**  
  - Contain the Application Load Balancer (ALB)  
  - Two NAT Gateways for outbound internet access from private subnets  

- **Private App Subnets**  
  - Contain EC2 instances running the Flask app in an Auto Scaling Group  
  - ASG spans multiple Availability Zones (AZ-A, AZ-B) for high availability  

- **Private DB Subnets**  
  - Host the Amazon RDS MySQL instance with Multi-AZ deployment  
  - Ensure the database is not publicly accessible  

- **CloudWatch Logs**  
  - Collects ALB access logs, EC2 system and application logs, and RDS logs  

---

## 🔹 Database Design and High Availability

The Amazon RDS instance is provisioned with:

```yaml
MultiAZ: true
Properties:
      Engine: mysql
      EngineVersion: '8.0.35'
      DBInstanceClass: db.t3.micro
      AllocatedStorage: 8
      StorageType: gp2
      MasterUsername:   # set a username
      MasterUserPassword: # set a password
      DBSubnetGroupName: !Ref DBSubnetGroup
      VPCSecurityGroups: [ !Ref DBSG ]
      MultiAZ: true
      PubliclyAccessible: false
      BackupRetentionPeriod: 7

```
---

## 🚀 How It Works

**1️⃣ CloudFormation template**  
- Provisions the full AWS infrastructure.
- Launches EC2 instances in private subnets behind an ALB.
- Auto-scaling configured with CPU-based policies.
- Sets up RDS MySQL in private subnets with Multi-AZ support.
- Enables CloudWatch log collection for:
  - ALB access logs
  - Nginx/Flask logs on EC2
  - System logs

**2️⃣ Flask TODO App**  
- Simple Flask app with an HTML front-end.
- Automatically installed and started on EC2 instances via baked AMI or UserData script.
- Demonstrates the deployment flow for a real web service.

---

## 🛠️ Prerequisites

✅ AWS Account with sufficient permissions  
✅ AWS CLI configured (`aws configure`)  
✅ An existing EC2 Key Pair (for SSH/SSM access to instances)  
✅ S3 bucket (if using to transfer app artifact to EC2)  

---

## ⚙️ How to Deploy

### 1️⃣ Prepare Your Flask App

You can use the included `todo-app/` or modify it:



Or bake your app into an AMI for production use.

---

### 2️⃣ Deploy the CloudFormation stack

```bash
aws cloudformation deploy \
  --region <your-region> \
  --template-file project-1.yml \
  --stack-name project1-stack \
  --parameter-overrides KeyPairName=<YourKeyPairName> \
  --capabilities CAPABILITY_IAM
