//  toggling functionality for side Bar 
const sidebarToggle = document.querySelector("#sidebar-toggle");

sidebarToggle.addEventListener("click",function(){
    document.querySelector("#sidebar").classList.toggle("collapsed")
})

function addStudent() {
    // Retrieve the entered student ID
    const studentId = document.getElementById('studentId').value;

    // Clear the input field
    document.getElementById('studentId').value = '';

    // Display the added student in the list
    const addedStudentsList = document.getElementById('addedStudentsList');
    const listItem = document.createElement('li');
    listItem.textContent = studentId;
    addedStudentsList.appendChild(listItem);
}

function submitAssignment() {
    // Retrieve other assignment details (e.g., project name)
    const projectName = document.getElementById('projectName').value;

    // Retrieve the added student IDs from the list
    const addedStudentsList = document.getElementById('addedStudentsList');
    const studentItems = addedStudentsList.getElementsByTagName('li');
    const studentIds = Array.from(studentItems).map(item => item.textContent);

    // Log the assignment details
    console.log('Project Name:', projectName);
    console.log('Student IDs:', studentIds);

    // Add your logic here to handle the assignment, e.g., send data to the server

    // Clear the form
    document.getElementById('assignProjectForm').reset();

    // Clear the added students list
    addedStudentsList.innerHTML = '';

    // Close the modal
    const modal = new bootstrap.Modal(document.getElementById('assignProjectModal'));
    modal.hide();
}

