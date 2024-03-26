// JavaScript code to handle form submission and update UI dynamically
document.getElementById('add-todo-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission
    var category = document.getElementById('category').value;
    var description = document.getElementById('description').value;
    var dueDate = document.getElementById('due_date').value;

    // Create a new table row for the todo
    var newRow = document.createElement('tr');
    newRow.innerHTML = '<td>' + category + '</td><td>' + description + '</td><td>' + dueDate + '</td>' +
                       '<td>' +
                       '<button class="btn btn-danger btn-sm" onclick="deleteTodo(this)">Delete</button>' +
                       '<button class="btn btn-success btn-sm" onclick="markFinished(this)">Mark as Finished</button>' +
                       '</td>';
    document.getElementById('todo-list').appendChild(newRow);

    // Clear the form fields after submission
    document.getElementById('category').value = '';
    document.getElementById('description').value = '';
    document.getElementById('due_date').value = '';

    // Make AJAX request to add todo to the server
    var formData = new FormData(this); // Get form data
    fetch('/add-todo', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json' // Specify content type as JSON
        },
        body: JSON.stringify({
            category: category,
            description: description,
            due_date: dueDate
        })
    })
    .then(response => {
        if (response.ok) {
            // Reload the page after adding the todo
            window.location.reload();
        }
        throw new Error('Error adding todo');
    })
    .catch(error => {
        console.error('Error:', error);
        // Handle error if needed
    });
});


// JavaScript functions to handle deleting and marking todos as finished
function deleteTodo(button, todoId) {
    var row = button.closest('tr'); // Get the closest table row
    row.remove(); // Remove the row from the table

    // Make AJAX request to delete todo from the server
    fetch('/delete-todo/' + todoId, {
        method: 'POST'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error deleting todo');
        }
        // Handle successful response from server if needed
    })
    .catch(error => {
        console.error('Error:', error);
        // Handle error if needed
    });
}

function deleteFinishedTodo(button, todoId) {
    var row = button.closest('tr'); // Get the closest table row
    row.remove(); // Remove the row from the table

    // Make AJAX request to delete finished todo from the server
    fetch('/delete-finished-todo/' + todoId, {
        method: 'POST'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error deleting finished todo');
        }
        // Handle successful response from server if needed
    })
    .catch(error => {
        console.error('Error:', error);
        // Handle error if needed
    });
}

function markFinished(button, todoId) {
    var row = button.closest('tr'); // Get the closest table row
    row.querySelector('.btn-success').remove(); // Remove the "Mark as Finished" button
    var deleteButton = document.createElement('button');
    deleteButton.className = 'btn btn-danger btn-sm';
    deleteButton.textContent = 'Delete';
    deleteButton.onclick = function() {
        deleteFinishedTodo(this, todoId);
    };
    row.querySelector('.btn-danger').replaceWith(deleteButton); // Replace the button with a delete button
    document.getElementById('finished-list').getElementsByTagName('tbody')[0].appendChild(row); // Move the todo to the Finished section

    // Make AJAX request to mark todo as finished on the server
    fetch('/mark-finished/' + todoId, {
        method: 'POST'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error marking todo as finished');
        }
        // Handle successful response from server if needed
    })
    .catch(error => {
        console.error('Error:', error);
        // Handle error if needed
    });
}

// Fetch finished todos when the dashboard page loads
window.addEventListener('DOMContentLoaded', function() {
    fetchFinishedTodos();
});

// Function to fetch finished todos from the server
function fetchFinishedTodos() {
    fetch('/get-finished-todos') // Adjust the route to match your Flask route
    .then(response => response.json())
    .then(data => {
        // Call a function to render the fetched todos in the table
        renderFinishedTodos(data);
    })
    .catch(error => {
        console.error('Error fetching finished todos:', error);
    });
}

// Function to render finished todos in the table
function renderFinishedTodos(todos) {
    const finishedTodosBody = document.getElementById('finished-todos-body');
    finishedTodosBody.innerHTML = ''; // Clear existing content

    // Loop through each finished todo and create table rows
    todos.forEach(todo => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${todo.category}</td>
            <td>${todo.description}</td>
            <td>${todo.due_date}</td>
            <td>
                <button class="btn btn-danger btn-sm" onclick="deleteFinishedTodo(this, '${todo._id}')">Delete</button>
            </td>
        `;
        finishedTodosBody.appendChild(row);
    });
}