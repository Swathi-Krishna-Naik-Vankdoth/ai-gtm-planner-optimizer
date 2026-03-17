from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from anthropic import Anthropic
from dotenv import load_dotenv
import json
import os

load_dotenv()

app = FastAPI(title="AI GTM Campaign Planner & Optimizer", version="1.0.0")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

class CampaignBrief(BaseModel):
    product: str
    budget: float
    objective: str
    audience: str
    timeline: int
    channels: list[str]

class LiveCampaign(BaseModel):
    campaign_name: str
    channel: str
    roas: float
    ctr: float
    spend: float
    conversion_rate: float
    frequency: float
    campaign_objective: str

@app.get("/")
def root():
    return {"status": "running"}

@app.post("/plan")
def plan_campaign(brief: CampaignBrief):
    try:
        channels_str = ", ".join(brief.channels)
        prompt = f"""You are a senior GTM campaign strategist.

Campaign brief:
- Product: {brief.product}
- Budget: ${brief.budget:,.0f} USD
- Objective: {brief.objective}
- Audience: {brief.audience}
- Timeline: {brief.timeline} weeks
- Channels: {channels_str}

Respond with ONLY a raw JSON object. No markdown. No backticks. No explanation. Just JSON.

The JSON must have these exact keys:
- budget_allocation: array of objects with keys channel, percentage, dollar_amount, expected_roas, rationale
- readiness_checks: array of objects with keys item, status (pass/warn/fail), note
- readiness_score: integer 0-100
- readiness_verdict: string
- market_insights: array of objects with keys type (success/warning/danger), title, body
- launch_recommendation: string"""

        print(f"Sending to Claude...")
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        raw_text = response.content[0].text
        print(f"Claude said: {raw_text[:300]}")
        clean_text = raw_text.strip()
        if clean_text.startswith("```"):
            clean_text = clean_text.split("```")[1]
            if clean_text.startswith("json"):
                clean_text = clean_text[4:]
        result = json.loads(clean_text.strip())
        return result
    except Exception as e:
        print(f"ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/optimize")
def optimize_campaign(campaign: LiveCampaign):
    try:
        prompt = f"""You are a senior performance marketing analyst.

Live campaign:
- Campaign: {campaign.campaign_name}
- Channel: {campaign.channel}
- ROAS: {campaign.roas}x
- CTR: {campaign.ctr}%
- Spend: ${campaign.spend:,.0f}
- Conversion Rate: {campaign.conversion_rate}%
- Frequency: {campaign.frequency}
- Objective: {campaign.campaign_objective}

Respond with ONLY a raw JSON object. No markdown. No backticks. No explanation. Just JSON.

The JSON must have these exact keys:
- status: string (underperforming/on-track/at-risk)
- root_cause: string
- recommendations: array of objects with keys action, rationale, impact (High/Medium/Low)
- stakeholder_summary: string
- flags: array of objects with keys type (human-review/auto-resolved), item, detail"""

        print(f"Sending optimize to Claude...")
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        raw_text = response.content[0].text
        print(f"Claude optimize said: {raw_text[:300]}")
        clean_text = raw_text.strip()
        if clean_text.startswith("```"):
            clean_text = clean_text.split("```")[1]
            if clean_text.startswith("json"):
                clean_text = clean_text[4:]
        result = json.loads(clean_text.strip())
        return result
    except Exception as e:
        print(f"ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

app.mount("/app", StaticFiles(directory="frontend", html=True), name="frontend")