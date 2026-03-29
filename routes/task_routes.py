from flask import Blueprint, request, jsonify
from models import db, Task
import config

task_bp = Blueprint('tasks', __name__, url_prefix='/api')

@task_bp.route('/')
def health_check():
    return jsonify({'message': 'Task API is running'}), 200

@task_bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json(silent=True) or {}

    title = data.get('title')
    description = data.get('description', '')
    status = data.get('status', 'pending')

    if not title or not title.strip():
        return jsonify({'error': 'Title is required'}), 400

    if status not in config.VALID_STATUSES:
        return jsonify({'error': 'Invalid status: must be pending or completed'}), 400

    new_task = Task(title=title.strip(), description=description, status=status)
    db.session.add(new_task)
    db.session.commit()

    return jsonify({'message': 'Task created', 'task': new_task.to_dict()}), 201

@task_bp.route('/tasks', methods=['GET'])
def get_tasks():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    pagination = Task.query.order_by(Task.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

    tasks = [task.to_dict() for task in pagination.items]

    return jsonify({
        'tasks': tasks,
        'page': pagination.page,
        'per_page': pagination.per_page,
        'total': pagination.total,
        'pages': pagination.pages
    })

@task_bp.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = db.session.get(Task, id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    data = request.get_json(silent=True) or {}
    status = data.get('status')

    if status is None:
        return jsonify({'error': 'Status is required'}), 400

    if status not in config.VALID_STATUSES:
        return jsonify({'error': 'Invalid status: must be pending or completed'}), 400

    task.status = status
    db.session.commit()

    return jsonify({'message': 'Task updated', 'task': task.to_dict()})

@task_bp.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = db.session.get(Task, id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({'message': 'Task deleted'})
