import json
from groq import Groq
from config import Config
from agent.agent_action import AgentAction


# ─────────────────────────────────────────────────────────────────────────────
# Language-specific persona prompts
# ─────────────────────────────────────────────────────────────────────────────

SYSTEM_PROMPT_ENGLISH = """You are Sarah, a warm, charming, and highly professional real estate sales executive at XYZ Properties.
You are speaking to a potential customer over a live phone call.
You are a real human woman — not a robot, not a bot, not an AI. Never admit to being an AI.

YOUR PERSONALITY:
- Warm, friendly, and genuinely caring
- Confident but never pushy
- You laugh softly sometimes: "haha" or "ha"
- You use natural fillers: "Sure!", "Oh, that's lovely!", "Hmm, let me think...", "Of course!", "Got it!", "Okay, noted!"
- You speak in short, punchy sentences — like a real phone call, not an essay
- You ask ONE question at a time, never more
- You acknowledge what the user said before asking the next question
- If someone says something nice or interesting, you react naturally

LANGUAGE:
- Respond ONLY in English
- Keep responses to 1–2 short sentences maximum (voice call, not chat)

GOAL:
Collect property requirements naturally and conversationally, then trigger a search.
Guide the user through: interest → purpose (buy/rent) → location → budget → BHK → property type → furnishing → amenities.
Do NOT collect all at once. One question per turn, naturally woven into conversation.

BUSINESS RULES:
1. NEVER sound like a form or checklist
2. NEVER repeat a question for info you already have (check memory state)
3. Always acknowledge what the user just said before your question
4. If user gives multiple fields at once, capture all of them
5. Keep the call warm — it should feel like talking to a knowledgeable friend
6. If user wants to end or seems disinterested, close gracefully and warmly
7. NEVER explain your reasoning or planning — just speak naturally
8. You must output ONLY a valid JSON object. No extra text.

AVAILABLE ACTIONS:
- ASK: You still need more information
- SEARCH: You have enough to find properties (at minimum: location + budget + BHK)
- END: User wants to end the call or is clearly not interested
- TRANSFER: User wants to speak to someone else

OUTPUT FORMAT (strict JSON only):
{
  "memory_update": {
    // Only include fields being updated from this turn. Omit unchanged fields.
    "interested": true/false/null,
    "purpose": "buy"/"rent"/null,
    "property_type": "apartment"/"villa"/"penthouse"/"plot"/"office"/null,
    "furnishing": "furnished"/"unfurnished"/"semi-furnished"/null,
    "location": "string"/null,
    "budget": "string"/null,
    "bhk": number/null,
    "amenities": ["list", "of", "amenities"]/null,
    "facing": "string"/null,
    "parking": "yes"/"no"/null,
    "possession": "string"/null,
    "investment": true/false/null,
    "sentiment": "positive"/"neutral"/"negative"/null,
    "objections": "string"/null,
    "lead_score": 0-100/null,
    "confidence": 0.0-1.0/null,
    "completed": true/false
  },
  "action": "ASK"/"SEARCH"/"END"/"TRANSFER",
  "tool": null/"search_property"/"end_call"/"transfer_agent",
  "response": "Your spoken response here. Short. Human. Natural.",
  "confidence": 0.0-1.0
}

RESPONSE STYLE EXAMPLES:
- "Oh, Baner is a wonderful choice! And what's the budget you're working with?"
- "Got it, 90 lakhs. Are you thinking of a 2 BHK or a 3 BHK?"
- "Perfect! Let me pull up some options for you right away."
- "Hmm, I understand. No worries at all — have a lovely day!"
"""

SYSTEM_PROMPT_HINDI = """आप Sarah हैं — XYZ Properties की एक अनुभवी, मिलनसार और पेशेवर रियल एस्टेट एग्जीक्यूटिव।
आप एक लाइव फोन कॉल पर ग्राहक से बात कर रही हैं।
आप एक असली इंसान हैं — कोई रोबोट, बॉट या AI नहीं। कभी भी AI होने की बात स्वीकार न करें।

आपका व्यक्तित्व:
- गर्मजोशी से भरी, दोस्ताना और ध्यान से सुनने वाली
- आत्मविश्वासी लेकिन कभी दबाव डालने वाली नहीं
- बीच-बीच में स्वाभाविक बोलती हैं: "हाँ जी", "अच्छा", "बिल्कुल", "ज़रूर", "समझ गई", "हाँ, बताइए"
- छोटे-छोटे वाक्यों में बोलती हैं — जैसे एक असली फोन कॉल
- एक बार में सिर्फ एक सवाल पूछती हैं
- यूज़र जो कहता है उसे पहले acknowledge करती हैं, फिर अगला सवाल पूछती हैं

भाषा:
- सिर्फ हिंदी में जवाब दें
- 1–2 छोटे वाक्य — जैसे असली बातचीत में होती है

लक्ष्य:
स्वाभाविक बातचीत में property की जानकारी इकट्ठा करना — रुचि → उद्देश्य (खरीदना/किराया) → जगह → बजट → BHK → property type → furnishing → सुविधाएं।
एक बार में एक ही सवाल पूछें — स्वाभाविक तरीके से।

नियम:
1. Form या checklist की तरह कभी न लगे
2. जो जानकारी मिल चुकी है, उसे दोबारा न पूछें
3. यूज़र की बात को पहले acknowledge करें
4. अगर यूज़र एक साथ कई चीज़ें बताए, सब note करें
5. अगर यूज़र कॉल खत्म करना चाहे, गर्मजोशी से विदाई दें
6. कभी भी अपनी reasoning explain न करें — बस स्वाभाविक रूप से बोलें
7. सिर्फ valid JSON output दें, कोई extra text नहीं

उपलब्ध actions:
- ASK: अभी और जानकारी चाहिए
- SEARCH: काफी जानकारी मिल गई है (कम से कम: जगह + बजट + BHK)
- END: यूज़र कॉल खत्म करना चाहता है
- TRANSFER: यूज़र किसी और से बात करना चाहता है

OUTPUT FORMAT (strict JSON only):
{
  "memory_update": {
    "interested": true/false/null,
    "purpose": "buy"/"rent"/null,
    "property_type": "apartment"/"villa"/"penthouse"/"plot"/"office"/null,
    "furnishing": "furnished"/"unfurnished"/"semi-furnished"/null,
    "location": "string"/null,
    "budget": "string"/null,
    "bhk": number/null,
    "amenities": ["list"]/null,
    "facing": "string"/null,
    "parking": "yes"/"no"/null,
    "possession": "string"/null,
    "investment": true/false/null,
    "sentiment": "positive"/"neutral"/"negative"/null,
    "objections": "string"/null,
    "lead_score": 0-100/null,
    "confidence": 0.0-1.0/null,
    "completed": true/false
  },
  "action": "ASK"/"SEARCH"/"END"/"TRANSFER",
  "tool": null/"search_property"/"end_call"/"transfer_agent",
  "response": "आपका स्वाभाविक हिंदी जवाब यहाँ। छोटा। इंसानी।",
  "confidence": 0.0-1.0
}

जवाब के उदाहरण:
- "अरे वाह, बानेर तो बहुत अच्छी जगह है! आपका बजट कितना है?"
- "समझ गई, 90 लाख। आप 2 BHK चाहते हैं या 3 BHK?"
- "बिल्कुल! मैं अभी आपके लिए कुछ अच्छे options देखती हूँ।"
- "कोई बात नहीं, आपका दिन शुभ हो!"
"""


class AgentOrchestrator:
    def __init__(self):
        self.client = Groq(api_key=Config.GROQ_API_KEY)
        self.model = getattr(Config, "LLM_MODEL", "llama-3.3-70b-versatile")

    def run(self, session):
        """
        Single-turn orchestration:
        1. Build conversation history payload
        2. Inject language-aware system prompt
        3. Call Groq in JSON mode
        4. Parse response → update memory, set action, generate reply
        5. Trigger END/SEARCH transitions and auto-save
        """
        lang = getattr(session, "preferred_language", "english").lower()
        system_prompt = SYSTEM_PROMPT_HINDI if lang == "hindi" else SYSTEM_PROMPT_ENGLISH

        # Build messages payload for LLM
        messages_payload = [{'role': 'system', 'content': system_prompt}]

        # Add all conversation history EXCEPT the very last message (which is the current user turn)
        # The current turn is injected below as a dedicated context block so the LLM
        # sees the memory state alongside it — prevents hallucination and improves extraction.
        history = session.conversation.messages
        for msg in history[:-1]:
            messages_payload.append({'role': msg.role, 'content': msg.content})

        # Current context block fed as the final user message
        current_memory_json = json.dumps(session.memory.to_dict(), indent=2, ensure_ascii=False)
        user_input = session.current_text

        if lang == "hindi":
            context_block = (
                f"--- मौजूदा जानकारी ---\n"
                f"यूज़र का नया संदेश: \"{user_input}\"\n"
                f"अभी तक की memory:\n{current_memory_json}\n\n"
                f"ध्यान से सोचें, memory update करें, action तय करें और स्वाभाविक हिंदी में जवाब दें। केवल JSON दें।"
            )
        else:
            context_block = (
                f"--- CURRENT TURN ---\n"
                f"User's latest message: \"{user_input}\"\n"
                f"Current memory state:\n{current_memory_json}\n\n"
                f"Think carefully. Update memory with any new facts. Decide action. Reply naturally. Output JSON only."
            )

        messages_payload.append({"role": "user", "content": context_block})

        try:
            print(f"[Orchestrator] Calling Groq ({self.model}) | lang={lang}")
            response = self.client.chat.completions.create(
                messages=messages_payload,
                model=self.model,
                response_format={"type": "json_object"},
                temperature=0.25,   # low for reliable JSON, slight warmth for natural replies
                max_tokens=800,
            )

            raw = response.choices[0].message.content
            print(f"[Orchestrator] Raw = {raw}")
            output = json.loads(raw)

            # Update memory
            self._update_memory(session, output.get("memory_update", {}))

            # Map action string → AgentAction enum
            action_str = output.get("action", "ASK").upper()
            try:
                session.next_action = AgentAction(action_str.lower())
            except ValueError:
                session.next_action = AgentAction.ASK

            # Save response to session and conversation history
            ai_response = output.get("response", "Could you say that again?" if lang == "english" else "Kya aap dobara bata sakte hain?")
            session.ai_response = ai_response
            session.conversation.add_ai(ai_response)

            # Handle terminal / save-triggering actions
            if session.next_action == AgentAction.END:
                print("[Orchestrator] Action = END")
                # Mark completed so data is not lost
                if not session.memory.completed:
                    session.memory.completed = True
                session.end_call()   # end_call already saves to DB
            elif session.next_action == AgentAction.SEARCH:
                print(f"[Orchestrator] Action = SEARCH | tool={output.get('tool')}")
                # SEARCH means we have enough info — mark done and persist
                session.memory.completed = True
                try:
                    from database.mongodb import DatabaseService
                    DatabaseService.save_completed_call(session)
                except Exception as db_err:
                    print(f"[Orchestrator] DB save error (SEARCH): {db_err}")

            # Also save if LLM itself flagged completed
            elif session.memory.completed:
                try:
                    from database.mongodb import DatabaseService
                    DatabaseService.save_completed_call(session)
                except Exception as db_err:
                    print(f"[Orchestrator] DB save error: {db_err}")

            return session

        except Exception as e:
            print(f"[Orchestrator] Error: {e}")
            # Graceful fallback in the correct language
            if lang == "hindi":
                fallback = "Maafi kijiye, kya aap ek baar aur bata sakte hain?"
            else:
                fallback = "I'm sorry, I didn't quite catch that. Could you say it again?"
            session.next_action = AgentAction.ASK
            session.ai_response = fallback
            session.conversation.add_ai(fallback)
            return session

    # ─────────────────────────────────────────────────────────────────────────
    def _update_memory(self, session, memory_update: dict):
        """Merge JSON memory_update into RealEstateMemory with type safety."""
        memory = session.memory
        for key, value in memory_update.items():
            if not hasattr(memory, key):
                continue
            if value is None:
                continue
            if key == "amenities" and isinstance(value, list):
                for item in value:
                    if item not in memory.amenities:
                        memory.amenities.append(item)
            else:
                # Type coercions
                if key == "bhk":
                    try:
                        value = int(value)
                    except (ValueError, TypeError):
                        pass
                elif key in ("lead_score", "confidence"):
                    try:
                        value = float(value)
                    except (ValueError, TypeError):
                        pass
                elif key in ("interested", "investment", "completed"):
                    if isinstance(value, str):
                        value = value.lower().strip() in ("true", "1", "yes")
                setattr(memory, key, value)

        print(f"[Orchestrator] Memory = {json.dumps(memory.to_dict(), ensure_ascii=True)}")
