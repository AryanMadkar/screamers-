from flask import Blueprint, request, jsonify
from services.call_service import CallService


call_router = Blueprint('call_router', __name__)

@call_router.route('/call/start', methods=['POST'])
def call_start():
    try:
        call_data = CallService.start_call()
        return jsonify(call_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@call_router.route('/call/end', methods=['POST'])
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

@call_router.route('/call/status/<call_id>', methods=['GET'])
def call_status(call_id):
    try:
        call = CallService.get_call(call_id)
        if call:
            return jsonify(call.to_dict()), 200
        else:
            return jsonify({'error': 'Call not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500