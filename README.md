# AI GTM Campaign Planner & Optimizer

AI-powered decision-support system for GTM, marketing, and campaign teams that improves **pre-launch planning**, **live campaign optimization**, and **stakeholder communication**.

Built with **Python**, **FastAPI**, and the **Anthropic Claude API**.

---

## Overview

AI GTM Campaign Planner & Optimizer is a business-facing AI application designed to support the full campaign lifecycle, from planning before launch to diagnosing underperformance during execution and drafting decision-ready updates for leadership or partner teams.

The system helps answer three critical business questions:

1. **Planning:** Am I allocating budget and preparing this campaign correctly before launch?  
2. **Optimization:** Why is this campaign underperforming, and what should I do next?  
3. **Communication:** How do I explain performance issues and recommended actions clearly to stakeholders?

The application is exposed through REST APIs, making it easy to integrate into internal tools, campaign workflows, or marketing operations environments.

---

## Business Problem

Teams running digital campaigns often have strong data visibility but weak decision support.

Before launch, campaign plans are frequently built from past experience, static playbooks, or manual assumptions. Teams may go live without validating budget allocation, audience readiness, channel fit, creative completeness, or launch dependencies.

During campaign execution, performance dashboards surface metrics such as ROAS, CTR, spend, and conversion rate, but they do not explain **why** performance is changing. Diagnosing root cause often requires a skilled analyst manually connecting multiple signals, which slows down response and increases the chance of incorrect decisions.

After a problem is identified, campaign managers still need to translate analysis into a clear recommendation for leadership, finance, or partner teams. That communication step is often manual, inconsistent, and time-consuming.

The result is the same across all three phases:
- wasted ad spend
- slower decisions
- missed performance targets
- inconsistent stakeholder communication

This project was built to reduce that friction by combining planning, optimization, and communication into one AI-assisted workflow.

---

## Why I Built This

I built this project because I saw a recurring gap in campaign and GTM workflows: teams usually have access to data, but not to fast, consistent reasoning that helps them decide what to do next.

In real business settings, campaign managers often need to:
- evaluate whether a campaign is ready to launch
- decide how budget should be distributed across channels
- diagnose underperformance using incomplete or scattered signals
- communicate recommendations clearly to non-technical stakeholders

Those tasks are critical, but they are also repetitive, judgment-heavy, and time-sensitive.

I wanted to explore how AI could reduce friction in those workflows by acting as a business-facing decision-support system, one that helps teams plan more intelligently, respond faster during live campaigns, and communicate more clearly with leadership or partners.

This project is my attempt to turn that operational gap into an end-to-end AI system that supports faster decisions, clearer communication, and more scalable GTM execution.

---

## What the System Does

The system is designed around two core business workflows:

### 1. Pre-Launch Campaign Planning
Takes a campaign brief as input and returns:
- recommended budget allocation by channel
- expected ROAS ranges
- market opportunity insights
- launch readiness checks
- overall launch recommendation

### 2. Live Campaign Optimization
Takes live campaign metrics as input and returns:
- campaign status
- likely root-cause diagnosis
- prioritized optimization recommendations
- stakeholder-ready summary
- human-review flags for sensitive decisions

This makes the application more than a dashboard or chatbot. It is a prototype for an AI-powered GTM decision-support tool.

---

## Key Capabilities

| Endpoint | Capability | Business Value |
|---|---|---|
| `POST /plan` | Analyzes a campaign brief and recommends budget allocation, readiness checks, and launch guidance | Helps teams make stronger pre-launch decisions before spend begins |
| `POST /optimize` | Diagnoses live campaign performance, explains likely root causes, and recommends actions | Improves speed and consistency of campaign optimization |
| `GET /` | Returns app status and docs link | Supports lightweight service health and developer testing |

---

## System Workflow

The platform follows a practical business reasoning loop:

**Detect → Explain → Recommend → Draft → Flag**

- **Detect**  
  Identify meaningful performance or planning signals from campaign inputs

- **Explain**  
  Interpret those signals to diagnose likely root causes or readiness gaps

- **Recommend**  
  Generate specific next actions with rationale and expected impact

- **Draft**  
  Produce stakeholder-ready language for leadership or partner communication

- **Flag**  
  Separate recommendations that can be acted on immediately from those requiring human approval

This human-in-the-loop design is intentional. In business environments, some decisions carry budget, legal, partner, or brand implications and should remain subject to human review.

---

## Architecture

### High-Level Flow

1. **Input Layer**
   - user submits a campaign brief or live campaign metrics
   - inputs are validated using Pydantic schemas

2. **Application Layer**
   - FastAPI receives the request
   - the request is routed to the correct workflow:
     - pre-launch planning
     - live campaign optimization

3. **AI Reasoning Layer**
   - Claude API receives a structured business prompt
   - the model is instructed to return JSON-only structured output

4. **Response Layer**
   - the API returns a business-ready response such as:
     - budget allocation
     - readiness score
     - root-cause diagnosis
     - action recommendations
     - stakeholder summary
     - review flags

---

## Tech Stack

- **Python** — application logic
- **FastAPI** — REST API backend
- **Pydantic** — request and response validation
- **Anthropic Claude API** — AI reasoning and generation
- **dotenv** — environment variable management

---

## API Endpoints

### `GET /`
Returns service status and documentation link.

### `POST /plan`
Analyzes a campaign brief and returns:
- channel-level budget allocation
- readiness checks
- readiness score
- market insights
- launch recommendation

### `POST /optimize`
Analyzes live campaign performance and returns:
- campaign status
- root-cause diagnosis
- recommendations
- stakeholder summary
- flags for human review

---

## Example Use Cases

### Scenario 1: Pre-Launch Planning
A GTM team wants to validate how a new campaign budget should be distributed across Search, Display, and Video before launch.

### Scenario 2: Campaign Underperformance
A campaign manager sees declining ROAS and CTR and wants a faster explanation of what is driving the drop and what action should be taken next.

### Scenario 3: Stakeholder Communication
A manager needs to summarize campaign issues and proposed budget changes for a VP, finance partner, or advertiser-facing stakeholder.

---

## Sample Input

### Example `POST /plan`
```json
{
  "product": "New SaaS subscription offering",
  "budget": 50000,
  "objective": "Lead generation",
  "audience": "Mid-market B2B decision makers",
  "timeline": 6,
  "channels": ["Search", "Display", "Video"]
}
