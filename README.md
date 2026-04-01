---
title: AgroBridge OpenEnv
emoji: 🌾
colorFrom: green
colorTo: blue
sdk: docker
pinned: false
---

# AgroBridge

AgroBridge is an AI training environment that simulates matching farmers with agricultural jobs posted by landowners.

Landowners can post agricultural tasks such as harvesting, irrigation, or pesticide spraying, and farmers with different skill sets apply for these jobs.  

This environment allows AI agents to learn optimal job assignment strategies by maximizing rewards when farmer skills match the required task skills.

The environment includes multiple tasks, farmer profiles, and reward-based grading logic to simulate real-world agricultural labor matching.

## Problem
Agricultural labor allocation is inefficient because farmers and landowners lack a structured matching system.

## Solution
AgroBridge simulates an AI environment where agents learn to optimally match farmers with agricultural tasks.

## Environment Design
- Farmers with different skills
- Jobs with difficulty levels
- Reward system based on skill match

## Reward System
Correct match → +1  
Partial match → +0.5  
Incorrect match → 0