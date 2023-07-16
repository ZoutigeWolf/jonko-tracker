window.onload = () => {
    document.getElementById("register-button").addEventListener("click",() => {
        window.location.href = window.location.origin + "/register";
    })

    document.getElementById("login-button").addEventListener("click",() => {
        let email = document.getElementById("email-input").value;
        let password = document.getElementById("password-input").value;
        let remember = document.getElementById("remember-input").value;

        fetch(window.location.origin + "/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: email,
                password: password,
                remember: remember
            })
        }).then(response => {
            if (response.status === 200) {
                window.location.href = window.location.origin;
            }
            else {
                location.reload();
            }
        });
    })
};