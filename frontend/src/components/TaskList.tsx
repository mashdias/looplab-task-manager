import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';

interface Task {
    id: number;
    title: string;
    description: string;
    status: string;
    priority: string;
    due_date: string;
    project: number;
}

export default function TaskList() {
    const [tasks, setTasks] = useState<Task[]>([]);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchTasks = async () => {
            try {
                const res = await api.get('tasks/');
                setTasks(res.data.results || res.data); // Handle pagination
            } catch (err) {
                console.error(err);
                // Redirect if unauthorized
                navigate('/');
            }
        };
        fetchTasks();
    }, [navigate]);

    const handleLogout = () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        navigate('/');
    };

    return (
        <div className="task-list-container">
            <header className="header">
                <h2>My Tasks</h2>
                <button onClick={handleLogout} className="logout-btn">Logout</button>
            </header>
            <div className="tasks">
                {tasks.length === 0 ? (
                    <p>No tasks found.</p>
                ) : (
                    tasks.map((task) => (
                        <div key={task.id} className="task-card">
                            <h3>{task.title}</h3>
                            <p>{task.description}</p>
                            <div className="task-meta">
                                <span>Status: {task.status}</span>
                                <span>Priority: {task.priority}</span>
                                <span>Due: {task.due_date || 'N/A'}</span>
                            </div>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
}
