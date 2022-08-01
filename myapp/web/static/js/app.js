//subject login
const loginBtn = document.getElementById('login_to_account');
loginBtn.addEventListener('click', function (event) {
    event.preventDefault();
    const email = document.getElementById('user').value;
    const password = document.getElementById('password').value;
    loginBtn.innerHTML = 'Logging in...';
    if(email === '' || password === '') {
        alert('Please provide email and password');
        loginBtn.innerHTML = 'Login';
    } else {
        const data = {
            username: email,
            password: password
        };
       $.ajax({
            url: '/login',
            type: 'POST',
            data: data,
            success: function (response) {
                if(response.status == 'success') {
                    alert(response.message);
                    window.location.href = '/dashboard';
                }else if(response.message =='Password incorrect'){
                    alert(response.message);
                    loginBtn.innerHTML = 'Login';
                } else {
                    alert(response.message);
                    loginBtn.innerHTML = 'Login'; 
                }   
            },
            error: function (error) {
                console.log(error);
                loginBtn.innerHTML = 'Login';
            }
        });
    }
});

//create account
const createAccountBtn = document.getElementById('create_account');
createAccountBtn.addEventListener('click', function (event) {
    event.preventDefault();
    const email = document.getElementById('email').value;
    const username = document.getElementById('user').value;
    const fullname = document.getElementById('Fullname').value;
    const password = document.getElementById('password').value;
    const password2 = document.getElementById('verifypassword').value;

    createAccountBtn.innerHTML = 'Creating account...';

    if(email === '' || username === '' || fullname === '' || password === '' || password2 === '') {
        alert('Please provide the necessary details');
        createAccountBtn.innerHTML = 'Create Account';
    } else {
        if (password !== password2) {
            alert('Passwords do not match');
            createAccountBtn.innerHTML = 'Create Account';
        } else {
            const data = {
                username: username,
                password: password,
                email: email,
                fullname: fullname
            };
           $.ajax({
                url: '/create_account',
                type: 'POST',
                data: data,
                success: function (response) {
                    if(response.success) {
                        window.location.href = '/login';
                    } else {
                        alert(response.message);
                        createAccountBtn.innerHTML = 'Create Account'; 
                    }   
                },
                error: function (error) {
                    console.log(error);
                    createAccountBtn.innerHTML = 'Create Account';
                }
            });
        }
    }
});

//forgot password
const forgotPasswordBtn = () => {
    const email = document.getElementById('useremail').value;
    const forgotpasswordBtn = document.getElementById('login_to_forgotpassword');
    forgotpasswordBtn.innerHTML = 'Sending email...';
    const data = {
        email: email
    };
    
    if(email === '') {
        alert('Please provide your email');
        forgotpasswordBtn.innerHTML = 'Next';
    } else {
        $.ajax({
            url: '/forgot_password',
            type: 'POST',
            data: data,
            success: function (response) {
                if(response.status) {
                    alert(response.message);
                } else {
                    forgotpasswordBtn.innerHTML = 'Next';
                    alert(response.message);
                }   
            },
            error: function (error) {
                console.log(error);
                forgotpasswordBtn.innerHTML = 'Next';
            }
        });
    }
}