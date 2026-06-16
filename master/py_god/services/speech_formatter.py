import re


class SpeechFormatter:
    """
    Converts plain-text AI responses into natural SSML with <break> tags.
    Supports both English and Hindi (Devanagari) fillers and punctuation.
    Output is wrapped in <speak> for compatibility with ElevenLabs and other TTS engines.
    """

    @staticmethod
    def format_speech(text: str, language: str = "english") -> str:
        if not text or not text.strip():
            return ""

        # Normalize whitespace
        formatted = re.sub(r'\s+', ' ', text).strip()

        if language == "hindi":
            formatted = SpeechFormatter._format_hindi(formatted)
        else:
            formatted = SpeechFormatter._format_english(formatted)

        # Final cleanup: collapse consecutive break tags into the longer one
        formatted = re.sub(r'(<break time="[^"]+"/>\s*)+', lambda m: m.group(1), formatted)
        formatted = re.sub(r'\s+', ' ', formatted).strip()

        if not formatted.startswith("<speak>"):
            formatted = f"<speak>{formatted}</speak>"

        return formatted

    # ─────────────────────────────────────────────────────────────────────
    @staticmethod
    def _format_english(text: str) -> str:
        t = text

        # ── Fillers ──────────────────────────────────────────────────────
        t = re.compile(r'\bhmm+\s*\.\.\.', re.I).sub('Hmm... <break time="450ms"/>', t)
        t = re.compile(r'\bhmm+\b', re.I).sub('Hmm <break time="300ms"/>', t)

        t = re.compile(r'\bsure\s*[!.]', re.I).sub('Sure! <break time="300ms"/>', t)
        t = re.compile(r'\bsure\b', re.I).sub('Sure <break time="250ms"/>', t)

        t = re.compile(r'\bokay\s*\.\.\.', re.I).sub('Okay... <break time="350ms"/>', t)
        t = re.compile(r'\bokay\s*[!.]', re.I).sub('Okay! <break time="250ms"/>', t)
        t = re.compile(r'\bokay\b', re.I).sub('Okay <break time="200ms"/>', t)

        t = re.compile(r'\bgot it\s*[!.]', re.I).sub('Got it! <break time="300ms"/>', t)
        t = re.compile(r'\bgot it\b', re.I).sub('Got it <break time="250ms"/>', t)

        t = re.compile(r'\bof course\s*[!.]', re.I).sub('Of course! <break time="250ms"/>', t)
        t = re.compile(r'\bof course\b', re.I).sub('Of course <break time="200ms"/>', t)

        t = re.compile(r'\babsolutely\s*[!.]', re.I).sub('Absolutely! <break time="250ms"/>', t)
        t = re.compile(r'\babsolutely\b', re.I).sub('Absolutely <break time="200ms"/>', t)

        t = re.compile(r'\boh\s*[!,]', re.I).sub('Oh! <break time="200ms"/>', t)
        t = re.compile(r'\boh\b(?!\s*\w)', re.I).sub('Oh <break time="150ms"/>', t)

        t = re.compile(r'\bperfect\s*[!.]', re.I).sub('Perfect! <break time="300ms"/>', t)
        t = re.compile(r'\bperfect\b', re.I).sub('Perfect <break time="250ms"/>', t)

        t = re.compile(r'\bgreat\s*[!.]', re.I).sub('Great! <break time="250ms"/>', t)
        t = re.compile(r'\bgreat\b', re.I).sub('Great <break time="200ms"/>', t)

        t = re.compile(r'\bwonderful\s*[!.]', re.I).sub('Wonderful! <break time="300ms"/>', t)
        t = re.compile(r'\bwonderful\b', re.I).sub('Wonderful <break time="250ms"/>', t)

        # ── Ellipsis ─────────────────────────────────────────────────────
        t = re.sub(r'\.\.\.', '... <break time="500ms"/>', t)

        # ── Sentence boundaries ──────────────────────────────────────────
        t = re.sub(r'\.(?!\s*<break)(?=\s|[A-Za-z]|$)', '. <break time="250ms"/>', t)
        t = re.sub(r'\?(?!\s*<break)(?=\s|[A-Za-z]|$)', '? <break time="300ms"/>', t)
        t = re.sub(r'!(?!\s*<break)(?=\s|[A-Za-z]|$)', '! <break time="250ms"/>', t)
        t = re.sub(r',(?!\s*<break)(?=\s|[A-Za-z]|$)', ', <break time="150ms"/>', t)

        return t

    # ─────────────────────────────────────────────────────────────────────
    @staticmethod
    def _format_hindi(text: str) -> str:
        t = text

        # ── STEP 1: Hindi sentence terminator ────────────────────────────
        t = re.sub(r'।(?!\s*<break)', '। <break time="300ms"/>', t)

        # ── STEP 2: Standard punctuation (run before fillers to pre-tag) ─
        t = re.sub(r'\?(?!\s*<break)(?=\s|$)', '? <break time="350ms"/>', t)
        t = re.sub(r'!(?!\s*<break)(?=\s|$)', '! <break time="300ms"/>', t)
        t = re.sub(r',(?!\s*<break)(?=\s)', ', <break time="150ms"/>', t)
        t = re.sub(r'\.(?!\s*<break)(?=\s|[अ-ॿA-Za-z]|$)', '. <break time="250ms"/>', t)

        # ── STEP 3: Hindi filler overrides ───────────────────────────────
        # These match the filler word followed by WHATEVER punctuation+break
        # already injected in step 2, and replace the whole chunk with one
        # clean filler+break so there's never a double break.
        ALREADY = r'(?:[!,।\.]?\s*(?:<break[^/]*/>\s*)?)'

        t = re.sub(r'अच्छा' + ALREADY,  'अच्छा, <break time="300ms"/> ', t)
        t = re.sub(r'हाँ जी' + ALREADY, 'हाँ जी, <break time="250ms"/> ', t)
        t = re.sub(r'हाँ' + ALREADY,    'हाँ <break time="200ms"/> ',      t)
        t = re.sub(r'हां' + ALREADY,    'हां <break time="200ms"/> ',      t)
        t = re.sub(r'बिल्कुल' + ALREADY,'बिल्कुल! <break time="300ms"/> ',t)
        t = re.sub(r'ज़रूर' + ALREADY,   'ज़रूर! <break time="250ms"/> ',   t)
        t = re.sub(r'समझ गई' + ALREADY, 'समझ गई। <break time="300ms"/> ', t)
        t = re.sub(r'ठीक है' + ALREADY, 'ठीक है। <break time="250ms"/> ', t)
        t = re.sub(r'नोट कर लिया' + ALREADY, 'नोट कर लिया। <break time="300ms"/> ', t)
        t = re.sub(r'बहुत अच्छा' + ALREADY, 'बहुत अच्छा! <break time="300ms"/> ', t)
        t = re.sub(r'वाह' + ALREADY,    'वाह! <break time="250ms"/> ',     t)
        t = re.sub(r'अरे' + ALREADY,    'अरे <break time="150ms"/> ',      t)

        # ── STEP 4: Collapse consecutive breaks → keep longest ────────────
        def _keep_longest(m):
            times = re.findall(r'(\d+)ms', m.group(0))
            best = max(int(x) for x in times) if times else 300
            return f'<break time="{best}ms"/>'
        t = re.sub(r'(<break time="\d+ms"/>\s*)+', _keep_longest, t)

        return t

