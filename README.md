# AgroBridge

## Project Overview

AgroBridge is an AI-based simulation environment designed to model a real-world agricultural job marketplace. It acts as a bridge between landowners and farmers.

In many rural areas, landowners need workers to perform agricultural tasks such as harvesting, planting, irrigation, and pesticide spraying. At the same time, many farmers look for temporary or seasonal work opportunities.

AgroBridge simulates this ecosystem where landowners post agricultural jobs and farmers apply for those jobs based on their skills. An AI agent interacts with this environment and learns how to assign the most suitable farmer to a job.

The goal of the AI agent is to intelligently match farmers with agricultural jobs using information such as required skills and farmer capabilities.


## Real-World Problem

Agricultural labor management is often inefficient. Landowners struggle to find skilled workers, while farmers may miss opportunities that match their skills.

AgroBridge addresses this by simulating a system that helps:

* Landowners find skilled farmers quickly
* Farmers get job opportunities that match their abilities
* Agricultural tasks get completed efficiently


## How the Environment Works

The environment follows the OpenEnv framework and includes three main functions:

### reset()

Initializes a new job scenario where a landowner posts a job with specific skill requirements.

### step(action)

The AI agent selects a farmer for the job. The environment evaluates the decision and assigns a reward based on how well the farmer's skills match the job requirements.

### state()

Returns the current environment state, including the job information and available farmers.


## Tasks and Difficulty Levels

The environment includes three task difficulty levels:

Easy – Basic skill matching between farmer and job.

Medium – Includes partial reward scenarios where skills are related but not exact.

Hard – More complex scenarios involving different job types and skill considerations.


## Reward System

The reward function evaluates how well the selected farmer matches the job requirements.

* Perfect skill match → reward = 1.0
* Partial match → reward = 0.5
* Incorrect match → reward = 0.0

This reward mechanism helps the AI agent learn better job assignment strategies.


## Project Structure

env.py – Main environment logic implementing reset(), step(), and state()
tasks.py – Defines job scenarios and difficulty levels
models.py – Defines farmer data models
graders.py – Implements reward calculation
inference.py – Baseline script to run the environment
requirements.txt – Project dependencies
Dockerfile – Container setup for reproducible execution
openenv.yaml – OpenEnv configuration file


## Objective

The goal of AgroBridge is to create a realistic AI training environment where agents learn to efficiently match farmers with agricultural job opportunities, improving labor allocation in the farming ecosystem.
