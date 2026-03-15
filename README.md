# Prioritix AI

An AI-driven product feedback intelligence platform that transforms large volumes of unstructured app reviews into prioritized, actionable insights for product and engineering teams.

![CI](https://github.com/harshitamandalika/prioritix-ai/actions/workflows/ci.yml/badge.svg)

## Overview

Prioritix AI helps teams analyze customer feedback at scale. Instead of manually reading thousands of app reviews, the platform processes review data, classifies it by sentiment, urgency, and feature area, groups related reviews into clusters, and surfaces the most important patterns through an interactive dashboard and AI-generated executive summaries.

The goal is to reduce noise, speed up feedback analysis, and help product teams make better roadmap decisions using structured evidence from customer reviews.

## Problem Statement

Modern product teams receive large volumes of feedback, especially through app store reviews. While this feedback is valuable, it is often:

- Unstructured and difficult to analyze manually
- Time-consuming to review at scale
- Repetitive, noisy, and low-signal
- Difficult to prioritize consistently across teams

Prioritix AI addresses this by building an end-to-end pipeline that converts raw app reviews into structured product insights and presents them through a dashboard designed for exploration and prioritization.

## Key Features

- Ingests and processes 10K+ app reviews
- Classifies reviews by feature area, sentiment, and urgency
- Groups related reviews into clusters for issue exploration
- Highlights recurring pain points across customer feedback
- Provides a dashboard for feature-level and cluster-level analysis
- Displays representative cluster samples for qualitative inspection
- Generates AI-powered executive summaries of processed review insights using Gemini
- Stores both raw and enriched review data in SQLite
- Supports reproducible development workflows with Docker
- Uses GitHub Actions for continuous integration

## Impact

- Reduced manual review effort by **80%**
- Reduced ambiguous feedback by **65%+**
- Identified recurring issue themes from high-priority negative reviews

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
- Sentiment classification
- Urgency classification
- Feature area classification

### LLM Integration
- Gemini API
- Executive summarization of processed review insights

### DevOps / Tooling
- Docker
- GitHub Actions

## System Architecture

The platform follows an end-to-end feedback intelligence workflow:

1. **Data Ingestion**  
   Raw app reviews are collected and stored in SQLite.

2. **Preprocessing**  
   Reviews are cleaned, normalized, and prepared for downstream analysis.

3. **Feedback Enrichment**  
   Each review is enriched with structured labels such as:
   - Feature area
   - Sentiment
   - Urgency
   - Issue type

4. **Theme Discovery**  
   Reviews are grouped into clusters to surface recurring issue patterns and enable exploratory analysis of related complaints.

5. **Feature-Level Analysis**  
   Aggregated insights are computed by feature area to show:
   - total review volume
   - sentiment distribution
   - high-urgency concentration

6. **Dashboard Visualization**  
   A React dashboard presents:
   - a feature table
   - cluster summaries
   - representative cluster samples

7. **AI Executive Summary**  
   A Gemini-powered summarization layer generates concise executive summaries from processed review insights, highlighting top pain points, urgent issues, and recommended product priorities.

## Example Use Cases

- Identify the most urgent product issues from thousands of app reviews
- Track which feature areas receive the most negative or high-urgency feedback
- Explore clusters of related complaints to understand recurring patterns
- Inspect sample reviews within each cluster for qualitative context
- Generate executive summaries for product and engineering stakeholders
- Support roadmap planning using structured customer feedback insights

## Why This Project Matters

Prioritix AI demonstrates how AI can be used to convert noisy customer feedback into structured decision support for product teams. Rather than treating reviews as raw text alone, the platform combines analytics, clustering, and LLM-based summarization to help teams identify what matters most and respond faster to user pain points.
