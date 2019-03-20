function log_message(message) {
    console.log(message)
    $('#message').text(message)
}

function log_api_error(xhr, text, status) {
    const reponse_as_json = $.parseJSON(xhr.responseText)
    const message = reponse_as_json['message']
    log_message('ERROR: ' + reponse_as_json['message'])
}

function login()
{
    console.log('Logging in...')
    const form = $('#login_form')[0]
    const user_id = $('#user_id').val()
    const password = $('#password').val()
    console.log('Using form action ' + form.action)
    console.log('User ID: ' + user_id)
    $.ajax({
        url: form.action,
        method: 'POST',
        contentType: "application/json",
        dataType: 'json',
        data: JSON.stringify ({
            'user_id': user_id,
            'password': password
        }),
        success: function(data, status) {
            log_message('Login success')
            document.location.replace('/')
        },
        error: log_api_error
    })
    console.log('Login submitted.')
}

function logout() {
    console.log('Logging out...')
    $.ajax({
        url: '/api/auth/logout',
        method: 'POST',
        success: function(data, status) {
            log_message("Logout succeeded")
            document.location.replace('/')
        },
        error: log_api_error
    })
}

function register() {
    console.log('Registering user...')
    const form = $('#registration_form')[0]
    const user_id = $('#user_id').val()
    const name = $('#name').val()
    const password = $('#password').val()
    $.ajax({
        url: form.action,
        method: 'POST',
        contentType: "application/json",
        dataType: 'json',
        data: JSON.stringify ({
            'user_id': user_id,
            'name': name,
            'password': password
        }),
        success: function(data, status) {
            log_message("Registration successful")
            document.location.replace('/')
        },
        error: log_api_error
    })
}

function load_user_list() {
    log_message("Loading user list...")
    $.ajax({
        url: '/api/users',
        method: 'GET',
        contentType: "application/json",
        dataType: 'json',
        success: function(data, status, xhr) {
            $('#message').text('') // clear log message
            const users = data.objects
            const user_list = $('#user_list')
            $.each(
                users,
                function (key, user) {
                    var li = $('<li/>').appendTo(user_list)
                    $('<a/>')
                    .attr('href', '/users/' + user.user_id)
                    .text(user.name)
                    .appendTo(li)
                }
            )
        },
        error: log_api_error
    })
}