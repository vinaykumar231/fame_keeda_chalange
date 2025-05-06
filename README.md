## Overview

This repository focuses on two sections of the challenge:

- **Section A: Campaign Orchestrator API**  
  The objective was to build microservices that handle the lifecycle of influencer marketing campaigns, trigger webhooks, maintain campaign state, and retry failed actions.
  
- **Section B: AI Brief Generator**  
  This section involved integrating AI tools (LLMs) to generate influencer campaign briefs dynamically based on various input parameters (brand, product, platform).

## Tracks Chosen

I selected **Section A** (Campaign Orchestrator API) and **Section B** (AI Brief Generator) for this challenge. The reasons for my choice are:

1. **Campaign Orchestrator API**:  
   This section allows me to showcase my skills in building reliable, event-driven microservices with retries and state management. Webhook handling and event bus integration were key focus areas.

2. **AI Brief Generator**:  
   This section allowed me to demonstrate how AI models can be integrated with backend services to dynamically generate content (influencer briefs). I utilized LLMs and function calling for generating structured campaign briefs.

## Installation Instructions

To run this project locally, follow the steps below:

### Prerequisites

- Docker
- Docker Compose
- Python 3.x (for API part)

### Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/fame-keeda-backend-challenge.git
   cd app