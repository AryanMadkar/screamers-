from flask import Blueprint, request, jsonify
from services.call_service import CallService

router = Blueprint('router', __name__, url_prefix='/api')

@router.route('/call/start', methods=['POST'])
def call_start():
    try:
        call_data = CallService.start_call()
        if not call_data:
            return jsonify({'error': 'Failed to start call'}), 500
        return jsonify(call_data), 200
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
            # Check if call exists or if validation failed
            call = CallService.get_call(call_id)
            if not call:
                return jsonify({'error': 'Call not found'}), 404
            if not call.active:
                return jsonify({'error': 'Call is inactive'}), 400
            return jsonify({'error': 'Invalid audio chunk'}), 400
            
        return jsonify({'status': 'accepted'}), 202
    except Exception as e:
        return jsonify({'error': str(e)}), 500