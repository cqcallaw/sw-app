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
            console.log("Login success!")
            $('#message').text('Login success!')
            document.location.replace('/')
        },
        error: function(xhr, text, status) {
            const reponse_as_json = jQuery.parseJSON(xhr.responseText)
            const message = reponse_as_json['message']
            console.log('Login failure: ' + message)
            $('#message').text('ERROR: ' + message)
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
            console.log("Logout success!")
            $('#message').text('Logout success!')
            document.location.replace('/')
        },
        error: function(xhr, text, status) {
            const reponse_as_json = jQuery.parseJSON(xhr.responseText)
            const message = reponse_as_json['message']
            console.log('Logout failure: ' + message)
            $('#message').text('ERROR: ' + message)
        }
    })
}
