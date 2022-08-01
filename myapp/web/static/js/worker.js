const logout = () => {
    // Do logout
    $.ajax({
        url: '/logout',
        type: 'GET',
        success: function (data) {
            // Do something
            if(data.status == 'success') {
                // Do something
                window.location.href = '/';

            }
        },
        error: function (data) {
            // Do something
            alert('Something went wrong, please try again later.');
        }
    });
}

// update user details
const updateUserDetails = () => {
    const email = $('#email').val();
    const username = $('#user').val();
    const name = $('#fullname').val();

    const update_account = document.getElementById('update_account');
    update_account.disabled = true;
    update_account.innerHTML = 'Updating...';

    if(email == '' || username == '' || name == '') {
        alert('Please fill all the fields');
        update_account.disabled = false;
        update_account.innerHTML = 'Update Details';
    } else {
        $.ajax({
            url: '/edit_user',
            type: 'UPDATE',
            data: {
                email: email,
                username: username,
                name: name
            },
            success: function (data) {
                if(data.status == 'success') {
                    alert('User details updated successfully.');
                    window.location.href = '/dashboard';
                }else if(data.message == 'Username already exists'){
                    alert('Username already exists, please try another one.');
                    update_account.disabled = false;
                    update_account.innerHTML = 'Update Details';
                    
                }else{
                    alert('Something went wrong, please try again later.');
                    update_account.disabled = false;
                    update_account.innerHTML = 'Update Details';
                }
            },
            error: function (data) {
                alert('Something went wrong, please try again later.');
                update_account.disabled = false;
                update_account.innerHTML = 'Update Details';
            }
        });
    }
}

//delete user account
const deleteUserAccount = () => {

    $.ajax({
        url: '/delete_user',
        type: 'DELETE',
        success: function (data) {
            if(data.status == 'success') {
                alert('User account deleted successfully.');
                window.location.href = '/';
            }else{
                alert('Something went wrong, please try again later.');
            }
        },
        error: function (data) {
            alert('Something went wrong, please try again later.');
        }
    });
}

// add new task
const addNewTask = () => {
    const task = $('#heading').val();
    const description = $('#description').val();
    const priority = $('#priority').val();
    const Category = $('#Category').val();

    const add_task = document.getElementById('add_task');
    add_task.disabled = true;
    add_task.innerHTML = 'Adding...';

    if(task == '' || description == '' || priority == '' || Category == '') {
        alert('Please fill all the fields');
        add_task.disabled = false;
        add_task.innerHTML = 'Add Task';
    } else {
        $.ajax({
            url: '/add_task',
            type: 'POST',
            data: {
                task: task,
                description: description,
                priority: priority,
                Category: Category
            },
            success: function (data) {
                if(data.status == 'success') {
                    alert('Task added successfully.');
                    window.location.href = '/dashboard';
                }else{
                    alert('Something went wrong, please try again later.');
                    console.log(data.error);
                    add_task.disabled = false;
                    add_task.innerHTML = 'Add Task';
                }
            },
            error: function (_data) {
                alert('Something went wrong, please try again later.');
                add_task.disabled = false;
                add_task.innerHTML = 'Add Task';
            }
        });
    }
}

//deleteTask
const deleteTask = (id) => {
    $.ajax({
        url: '/delete_task',
        type: 'DELETE',
        data: {
            id: id
        },
        success: function (data) {
            if(data.status == 'success') {
                alert('Task deleted successfully.');
                window.location.href = '/dashboard';
            }else{
                alert('Something went wrong, please try again later.');
            }
        },
        error: function (data) {
            alert('Something went wrong, please try again later.');
        }
    });
}

//mark task as completed
const markTaskAsCompleted = (id) => {
    $.ajax({
        url: '/mark_task',
        type: 'UPDATE',
        data: {
            id: id
        },
        success: function (data) {
            if(data.status == 'success') {
                alert('Task marked as completed successfully.');
                window.location.href = '/dashboard';
            }else{
                alert('Something went wrong, please try again later.');
            }
        },
        error: function (data) {
            alert('Something went wrong, please try again later.');
        }
    });
}

//edit task
const editTask = (id) => {
    window.location.href = '/edit_task/' + id;
}

//update task
const updateTask = () => {
    const id = $('#taskid').val();
    const task = $('#heading').val();
    const description = $('#description').val();
    const priority = $('#priority').val();

    const update_task = document.getElementById('update_task');
    update_task.disabled = true;
    update_task.innerHTML = 'Updating...';

    if(task == '' || description == '' || priority == '' || id == '') {
        alert('Please fill all the fields');
        update_task.disabled = false;
        update_task.innerHTML = 'Update Task';
    } else {
        $.ajax({
            url: '/update_task',
            type: 'UPDATE',
            data: {
                id: id,
                task: task,
                description: description,
                priority: priority
            },
            success: function (data) {
                if(data.status == 'success') {
                    alert('Task updated successfully.');
                    window.location.href = '/dashboard';
                }else{
                    alert('Something went wrong, please try again later.');
                    update_task.disabled = false;
                    update_task.innerHTML = 'Update Task';
                }
            },
            error: function (data) {
                alert('Something went wrong, please try again later.');
                update_task.disabled = false;
                update_task.innerHTML = 'Update Task';
            }
        });
    }
}