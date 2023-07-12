window.onload = () => {
    document.getElementById("login-button").addEventListener("click",() => {
        window.location.href = window.location.origin + "/login";
    })

    document.getElementById("register-button").addEventListener("click",() => {
        let username = document.getElementById("username-input").value;
        let password = document.getElementById("password-input").value;
        let passwordControl = document.getElementById("password-control-input").value;

        if (username.length === 0 || password.length < 8) return;

        if (password !== passwordControl) {
            document.getElementById("password-input").value = "";
            document.getElementById("password-control-input").value = "";
            return;
        }

        fetch(window.location.origin + "/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: username,
                password: password,
            })
        }).then(response => {
            if (response.status === 201) {
                window.location.href = window.location.origin;
            }
            else {
                location.reload();
            }
        });
    })
};