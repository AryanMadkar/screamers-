from flask import Blueprint, request, jsonify
from services.call_service import CallService
from services.speech_formatter import SpeechFormatter

router = Blueprint('router', __name__, url_prefix='/api')

# ─── Opening greetings Sarah uses when a call starts ─────────────────────────
_GREETINGS = {
    "english": (
        "Hello! This is Sarah from XYZ Properties. "
        "Am I speaking with the right person? "
        "I just wanted to understand what kind of property you're looking for."
    ),
    "hindi": (
        "नमस्ते! मैं Sarah हूँ, XYZ Properties से। "
        "क्या मैं सही व्यक्ति से बात कर रही हूँ? "
        "मैं बस समझना चाहती थी कि आप किस तरह की property ढूंढ रहे हैं।"
    ),
}


@router.route('/call/start', methods=['POST'])
def call_start():
    """
    Start a new call session.
    Optional JSON body: { "language": "english" | "hindi" }
    Returns the call session dict plus Sarah's opening greeting in ai_response / ai_response_ssml.
    """
    try:
        data = request.get_json(silent=True) or {}
        language = data.get('language', 'english').lower().strip()
        if language not in ('english', 'hindi'):
            language = 'english'

        call_data = CallService.start_call(language=language)
        if not call_data:
            return jsonify({'error': 'Failed to start call'}), 500

        # Retrieve session so we can attach greeting
        call_session = CallService.get_call(call_data['call_id'])
        greeting_text = _GREETINGS.get(language, _GREETINGS['english'])
        greeting_ssml = SpeechFormatter.format_speech(greeting_text, language=language)

        call_session.ai_response      = greeting_text
        call_session.ai_response_ssml = greeting_ssml
        call_session.conversation.add_ai(greeting_text)

        return jsonify(call_session.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@router.route('/call/end', methods=['POST'])
def call_end():
    try:
        data = request.get_json(silent=True) or {}
        call_id = data.get('call_id')
        if not call_id:
            return jsonify({'error': 'call_id is required'}), 400
        success = CallService.end_call(call_id)
        if not success:
            return jsonify({'error': 'Call not found'}), 404
        return jsonify({'message': 'Call ended successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@router.route('/call/status/<call_id>', methods=['GET'])
def call_status(call_id):
    try:
        call = CallService.get_call(call_id)
        if call:
            return jsonify(call.to_dict()), 200
        else:
            return jsonify({'error': 'Call not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@router.route('/call/audio', methods=['POST'])
def call_audio():
    try:
        call_id = request.form.get('call_id')
        if not call_id:
            return jsonify({'error': 'call_id is required'}), 400

        if 'audio' not in request.files:
            return jsonify({'error': 'audio file is required'}), 400

        audio_file = request.files['audio']
        audio_data = audio_file.read()

        success = CallService.receive_audio(call_id, audio_data)
        if not success:
            call = CallService.get_call(call_id)
            if not call:
                return jsonify({'error': 'Call not found'}), 404
            if not call.active:
                return jsonify({'error': 'Call is inactive'}), 400
            return jsonify({'error': 'Invalid audio chunk'}), 400

        return jsonify({'status': 'accepted'}), 202
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@router.route('/call/message', methods=['POST'])
def call_message():
    """
    Text-based testing endpoint — bypasses STT entirely.

    JSON body:
    {
        "call_id": "<id>",
        "message": "user text here"
    }

    Returns the full updated session including:
      - ai_response       : plain text reply from Sarah
      - ai_response_ssml  : SSML-formatted version ready for ElevenLabs TTS
      - memory            : updated RealEstateMemory dict
      - state             : current call state
    """
    try:
        data = request.get_json(silent=True) or {}
        call_id = data.get('call_id')
        message = data.get('message', '').strip()

        if not call_id or not message:
            return jsonify({'error': 'call_id and message are required'}), 400

        call_session = CallService.get_call(call_id)
        if not call_session:
            return jsonify({'error': 'Call not found'}), 404
        if not call_session.active:
            return jsonify({'error': 'Call is inactive'}), 400

        # Lock session against worker collision
        call_session.processing = True
        try:
            from models.call_state import CallState
            from pipeline.pipeline_executor import PipelineExecutor

            call_session.current_text = message
            call_session.conversation.add_user(message)

            executor = PipelineExecutor()

            call_session.set_state(CallState.THINKING)
            call_session = executor.agent.process(call_session)

            call_session.set_state(CallState.SPEAKING)
            call_session = executor.tts.process(call_session)

            if call_session.state not in (CallState.LISTENING, CallState.ENDED):
                call_session.set_state(CallState.IDLE)
        finally:
            call_session.processing = False

        return jsonify(call_session.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500