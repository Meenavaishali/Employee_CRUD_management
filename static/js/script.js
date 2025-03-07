// ✅ Add Employee
function addEmployee() {
    let name = document.getElementById("name").value;
    let interviewTime = document.getElementById("interview_time").value;
    let details = document.getElementById("details").value;
    let notes = document.getElementById("notes").value;

    fetch('/add_employee', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, interview_time: interviewTime, details, notes })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        document.getElementById("employee_form").reset();
    })
    .catch(error => console.error("Error adding employee:", error));
}

// ✅ Search Employee
function searchEmployee() {
    let name = document.getElementById("search_name").value;
    fetch(`http://127.0.0.1:5000/search_employee?name=${name}`)
    .then(response => response.json())
    .then(data => {
        let results = document.getElementById("search_results");
        results.innerHTML = "";

        if (data.length === 0) {
            results.innerHTML = "<p>No employees found.</p>";
            return;
        }

        data.forEach(emp => {
            let interviewTimeValue = emp.interview_time ? emp.interview_time.replace(' ', 'T') : '';

            results.innerHTML += `
                <div id="employee_${emp.id}">
                    <input type="hidden" id="emp_id_${emp.id}" value="${emp.id}">
                    <label>Name:</label>
                    <input type="text" id="name_${emp.id}" value="${emp.name || ''}"><br>
                    <label>Interview Time:</label>
                    <input type="datetime-local" id="interview_time_${emp.id}" value="${interviewTimeValue}"><br>
                    <label>Details:</label>
                    <input type="text" id="details_${emp.id}" value="${emp.details || ''}"><br>
                    <label>Notes:</label>
                    <input type="text" id="notes_${emp.id}" value="${emp.notes || ''}"><br>
                    <button onclick="updateEmployee(${emp.id})">Update</button>
                    <button class="delete-btn" onclick="deleteEmployee(${emp.id})">Delete</button>
                </div>
                <hr>
            `;
        });
    })
    .catch(error => console.error(error));
}


// ✅ Update Employee
function updateEmployee(id) {
    let name = document.getElementById(`name_${id}`).value;
    let interviewTime = document.getElementById(`interview_time_${id}`).value;
    let details = document.getElementById(`details_${id}`).value;
    let notes = document.getElementById(`notes_${id}`).value;

    fetch(`/update_employee/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, interview_time: interviewTime, details, notes })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        searchEmployee();
    })
    .catch(error => console.error("Error updating employee:", error));
}

// ✅ Delete Employee
function deleteEmployee(id) {
    if (!confirm("Are you sure you want to delete this employee?")) {
        return;
    }

    fetch(`/delete_employee/${id}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        searchEmployee();
    })
    .catch(error => console.error("Error deleting employee:", error));
}
