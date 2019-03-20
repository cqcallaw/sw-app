function log_message(message) {
    console.log(message)
    $('#message').text(message)
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
        error: function(xhr, text, status) {
            const reponse_as_json = jQuery.parseJSON(xhr.responseText)
            log_message('ERROR: ' + reponse_as_json['message'])
        }
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
        error: function(xhr, text, status) {
            const reponse_as_json = jQuery.parseJSON(xhr.responseText)
            log_message('ERROR: ' + reponse_as_json['message'])
        }
    })
}

