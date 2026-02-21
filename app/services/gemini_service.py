"""
ImaraFund AI Recommendation Service
Using your proven Gemini 2.5 Flash prompts and configuration
"""

from typing import Dict
import logging

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logging.warning("google-generativeai not installed")

from app.core.config import settings

logger = logging.getLogger(__name__)


class GeminiService:
    """Your proven AI recommendation service using Gemini 2.5 Flash"""

    def __init__(self):
        self.ai_enabled = False

        if not GEMINI_AVAILABLE:
            logger.warning("⚠️ google-generativeai not installed. AI recommendations disabled.")
            return

        api_key = settings.GEMINI_API_KEY

        if api_key:
            try:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
                self.ai_enabled = True
                logger.info("✅ ImaraFund Gemini AI enabled!")
            except Exception as e:
                logger.warning(f"⚠️ AI setup failed: {e}")
        else:
            logger.info("ℹ️ AI disabled - Add GEMINI_API_KEY to .env")

    def get_ai_recommendation(self, company_profile: Dict, match: Dict) -> str:
        """Generate clear, simple AI recommendation using your exact prompt"""
        if not self.ai_enabled:
            return "🔑 Add your Gemini API key to .env file to get AI-powered recommendations!"

        # Your exact prompt that works - preserved completely
        prompt = f"""You are a friendly business advisor helping someone who is NOT a finance expert.

COMPANY:
- Business: {company_profile.get('company_name', 'Startup')}
- What they do: {company_profile.get('sector', 'Unknown')}
- Location: {company_profile.get('nationality', 'Unknown')}
- Stage: {company_profile.get('business_stage', 'Unknown')}
- Money needed: ${company_profile.get('funding_need_usd', 0):,}

FUNDING MATCH:
- Program: {match['program_name']}
- Institution: {match['institution']}
- Amount: ${match['funding_amount']:,}
- Match Score: {match['match_score']}/100

Write advice using SIMPLE language that anyone can understand. Include these 4 sections:

**WHY THIS WORKS:**
Explain in 2-3 simple sentences why this funding fits their business. Use everyday words.

**WHAT TO DO NEXT:**
Give 3 specific actions they can take today. Use simple words like "create a budget" not "develop financial projections."

**WATCH OUT FOR:**
Mention 1-2 realistic challenges in plain English. Be honest but encouraging.

**YOUR CHANCES:**
Say "Excellent", "Good", "Fair", or "Challenging" and explain why in one sentence.

Use everyday words. No jargon. Be encouraging but honest. Keep under 200 words."""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config={
                    'temperature': 0.8,
                    'top_p': 0.9,
                    'max_output_tokens': 600,
                }
            )
            return response.text

        except Exception as e:
            error_msg = str(e)
            logger.error(f"ImaraFund Gemini AI error: {error_msg}")

            # Your exact error handling logic
            if "quota" in error_msg.lower() or "rate" in error_msg.lower():
                return "⚠️ Too many requests. Free tier: 15 requests/minute. Please wait 60 seconds."
            elif "404" in error_msg or "not found" in error_msg.lower():
                return "⚠️ Model not available. Check your API key."
            else:
                return f"⚠️ AI temporarily unavailable: {error_msg}"