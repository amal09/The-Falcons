
window.onload=function(){
    const loginButton = document.getElementById("login");

loginButton.addEventListener("click", (event) => {
    // console.log("karitk");
    event.preventDefault();
    console.log(document.getElementById("password"))
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    fetch('http://localhost:8000/api/v1/signup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'

        },
        body: JSON.stringify({ email, password })

    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
        })
        .catch(error => {
            console.error('Error: ', error);
        });
})}

// http://localhost:8000/docs#/default/login_api_v1_login_post