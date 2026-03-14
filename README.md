# Prioritix AI

An AI-driven product feedback intelligence platform that transforms large volumes of unstructured app reviews into prioritized, actionable insights for product and engineering teams.

![CI](https://github.com/harshitamandalika/prioritix-ai/actions/workflows/ci.yml/badge.svg)

## Overview

Prioritix AI helps teams make sense of customer feedback at scale. Instead of manually reading thousands of app reviews, the platform automatically processes feedback, identifies sentiment and urgency, groups recurring pain points, and highlights the most important issues for roadmap decision-making.

The system is designed to reduce noise, surface actionable feedback faster, and support product teams with a clear, data-driven view of user pain points.

## Problem Statement

Modern product teams receive feedback from multiple channels, especially app store reviews. While this feedback is valuable, it is often:

- Unstructured and difficult to analyze manually
- Large in volume and time-consuming to review
- Repetitive, noisy, and low-signal
- Hard to prioritize consistently across teams

Prioritix AI addresses this by building an end-to-end pipeline that converts raw reviews into structured insights.

## Key Features

- Ingests and processes 10K+ app reviews
- Filters low-signal feedback to reduce manual review effort
- Classifies reviews by feature area, sentiment, and urgency
- Clusters high-urgency negative reviews to uncover recurring themes
- Highlights top user pain points for product prioritization
- Provides a dashboard for visual exploration of feedback patterns
- Includes an AI Copilot interface for insight discovery
- Containerized for reproducible development and deployment workflows
- Automated with GitHub Actions for continuous integration

## Impact

- Reduced manual review effort by **80%**
- Reduced ambiguous feedback by **65%+**
- Identified **8–10 recurring issue themes** from high-priority negative reviews
- Enabled product and engineering teams to focus on the most actionable feedback faster

## Tech Stack

### Backend
- Python
- FastAPI
- SQLite

### Frontend
- React

### Machine Learning / NLP
- Text preprocessing
- TF-IDF
- K-Means clustering
- Sentiment and urgency classification
- Feature area classification

### DevOps / Tooling
- Docker
- GitHub Actions

## System Architecture

The platform follows an end-to-end feedback intelligence workflow:

1. **Data Ingestion**  
   Raw app reviews are collected and loaded into the system.

2. **Preprocessing**  
   Reviews are cleaned, normalized, and prepared for downstream analysis.

3. **Feedback Classification**  
   A hybrid NLP pipeline classifies each review across dimensions such as:
   - Feature area
   - Sentiment
   - Urgency

4. **Noise Reduction and Prioritization**  
   Low-signal reviews are filtered out using a prioritization framework, allowing teams to focus on actionable feedback.

5. **Theme Discovery**  
   High-urgency negative reviews are vectorized using TF-IDF and clustered using K-Means to identify recurring pain points.

6. **Visualization and Exploration**  
   A React dashboard presents trends, categories, and issue themes for easier product analysis.

7. **AI Copilot Support**  
   An AI-assisted interface helps users explore feedback insights more efficiently.

## Example Use Cases

- Identify the most urgent product issues from thousands of app reviews
- Track which feature areas are receiving the most negative feedback
- Discover recurring pain points impacting user experience
- Support roadmap planning using structured customer feedback insights
- Help product managers and engineering teams prioritize fixes with evidence
