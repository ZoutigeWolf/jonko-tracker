window.onload = () => {
    document.getElementById("submit-button").addEventListener("click", submitNewPassword);
}

function submitNewPassword() {
    let password = document.getElementById("password-input").value;
    let control = document.getElementById("control-input").value;

    if (password.length < 8 || password !== control) {
        document.getElementById("password-input").value = "";
        document.getElementById("password-control-input").value = "";
        return;
    }

    let params = new URLSearchParams(window.location.search);

    if (!params.has("token")) {
        return;
    }

    let token = params.get("token");

    fetch(window.location.origin + "/forgot-password?token=" + token, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            password: password
        })
    }).then(response => {
        if (response.status !== 200) {
            window.location.reload();
        } else {
            window.location.href = window.location.origin = "/login";
        }
    });
}