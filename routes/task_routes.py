from flask import Blueprint, request, jsonify
from models import db, Task
from config import VALID_STATUSES

task_bp = Blueprint('task', __name__, url_prefix='/api')

@task_bp.route('/tasks', methods=['POST'])
def create_task():
    try:
        data = request.get_json()
        if not data or 'title' not in data or not data['title'].strip():
            return jsonify({'error': 'Title is required'}), 400
        
        status = data.get('status', 'pending')
        if status not in VALID_STATUSES:
            return jsonify({'error': 'Invalid status. Must be pending or completed'}), 400
        
        task = Task(
            title=data['title'].strip(),
            description=data.get('description', ''),
            status=status
        )
        db.session.add(task)
        db.session.commit()
        return jsonify(task.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500

@task_bp.route('/tasks', methods=['GET'])
def get_tasks():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)
        
        pagination = Task.query.paginate(page=page, per_page=per_page, error_out=False)
        tasks = [task.to_dict() for task in pagination.items]
        
        return jsonify({
            'tasks': tasks,
            'page': page,
            'per_page': per_page,
            'total': pagination.total
        })
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@task_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    try:
        task = db.session.get(Task, task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        data = request.get_json()
        if not data or 'status' not in data:
            return jsonify({'error': 'Status is required'}), 400
        
        if data['status'] not in VALID_STATUSES:
            return jsonify({'error': 'Invalid status. Must be pending or completed'}), 400
        
        task.status = data['status']
        db.session.commit()
        return jsonify(task.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500

@task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        task = db.session.get(Task, task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500
