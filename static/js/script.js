const API_URL = '/api/tasks';

// Load tasks on page load
document.addEventListener('DOMContentLoaded', () => {
    loadTasks();
});

// Handle form submission
document.getElementById('taskForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const title = document.getElementById('taskTitle').value;
    const description = document.getElementById('taskDescription').value;
    
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                title: title,
                description: description || null
            })
        });
        
        if (response.ok) {
            document.getElementById('taskForm').reset();
            loadTasks();
        } else {
            alert('Errore nella creazione del task');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Errore di connessione');
    }
});

// Load all tasks
async function loadTasks() {
    try {
        const response = await fetch(API_URL);
        const tasks = await response.json();
        
        displayTasks(tasks);
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('tasksContainer').innerHTML = 
            '<div class="empty-state"><p>Errore nel caricamento dei task</p></div>';
    }
}

// Display tasks
function displayTasks(tasks) {
    const container = document.getElementById('tasksContainer');
    const countElement = document.getElementById('taskCount');
    
    countElement.textContent = tasks.length;
    
    if (tasks.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
                <p>Nessun task presente. Inizia aggiungendone uno!</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = tasks.map(task => `
        <div class="task-item ${task.completed ? 'completed' : ''}" data-id="${task.id}">
            <div class="task-header">
                <div class="task-title">${escapeHtml(task.title)}</div>
            </div>
            ${task.description ? `<div class="task-description">${escapeHtml(task.description)}</div>` : ''}
            <div class="task-meta">
                <div class="task-date">
                    ${task.created_at ? formatDate(task.created_at) : ''}
                </div>
                <div class="task-actions">
                    ${!task.completed ? 
                        `<button class="btn-small btn-complete" onclick="toggleTask(${task.id}, true)">✓ Completa</button>` :
                        `<button class="btn-small btn-complete" onclick="toggleTask(${task.id}, false)">↺ Riapri</button>`
                    }
                    <button class="btn-small btn-delete" onclick="deleteTask(${task.id})">🗑 Elimina</button>
                </div>
            </div>
        </div>
    `).join('');
}

// Delete completed tasks
document.getElementById('deleteCompletedBtn').addEventListener('click', async () => {
    if (!confirm('Sei sicuro di voler eliminare tutti i task completati?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/completed`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            loadTasks();
        } else {
            alert('Errore nell\'eliminazione dei task completati');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Errore di connessione');
    }
});

// Toggle task completion
async function toggleTask(taskId, completed) {
    try {
        const response = await fetch(`${API_URL}/${taskId}`);
        const task = await response.json();
        
        task.completed = completed;
        
        const updateResponse = await fetch(`${API_URL}/${taskId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(task)
        });
        
        if (updateResponse.ok) {
            loadTasks();
        } else {
            alert('Errore nell\'aggiornamento del task');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Errore di connessione');
    }
}

// Delete task
async function deleteTask(taskId) {
    if (!confirm('Sei sicuro di voler eliminare questo task?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/${taskId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            loadTasks();
        } else {
            alert('Errore nell\'eliminazione del task');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Errore di connessione');
    }
}

// Utility functions
function escapeHtml(text) {
    if (text === null || text === undefined) {
        return '';
    }
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

function formatDate(dateString) {
    const date = new Date(dateString);
    const options = { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    return date.toLocaleDateString('it-IT', options);
}
