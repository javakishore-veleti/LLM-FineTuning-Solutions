from flask import Blueprint, request, jsonify, current_app
from modules.core.dao.event_dao import create_event, get_event, list_events, update_event, delete_event

bp = Blueprint('events', __name__, url_prefix='/api/events')


@bp.route('/', methods=['GET'])
def events_list():
    events = list_events()
    data = [
        {
            'event_id': e.event_id,
            'event_name': e.event_name,
            'event_description': e.event_description,
            'source_url': e.source_url,
            'source_location_type': e.source_location_type,
            'is_active': e.is_active,
            'created_at': e.created_at.isoformat() if e.created_at else None
        }
        for e in events
    ]
    return jsonify(data), 200


@bp.route('/<int:event_id>', methods=['GET'])
def events_get(event_id):
    e = get_event(event_id)
    if not e:
        return jsonify({'error': 'not found'}), 404
    return jsonify({
        'event_id': e.event_id,
        'event_name': e.event_name,
        'event_description': e.event_description,
        'source_url': e.source_url,
        'source_location_type': e.source_location_type,
        'is_active': e.is_active,
        'created_at': e.created_at.isoformat() if e.created_at else None
    }), 200


@bp.route('/', methods=['POST'])
def events_create():
    payload = request.get_json() or {}
    if not payload.get('event_name') or not payload.get('source_url'):
        return jsonify({'error': 'event_name and source_url required'}), 400
    ev = create_event(payload)
    return jsonify({'event_id': ev.event_id}), 201


@bp.route('/<int:event_id>', methods=['PUT'])
def events_update(event_id):
    payload = request.get_json() or {}
    ev = update_event(event_id, payload)
    if not ev:
        return jsonify({'error': 'not found'}), 404
    return jsonify({'event_id': ev.event_id}), 200


@bp.route('/<int:event_id>', methods=['DELETE'])
def events_delete(event_id):
    ok = delete_event(event_id)
    if not ok:
        return jsonify({'error': 'not found'}), 404
    return jsonify({'deleted': True}), 200
