window.onload = () => {
    document.getElementById("submit-button").addEventListener("click", submitRequest);
};

function submitRequest() {
    let email = document.getElementById("email-input").value;

    fetch(window.location.origin + "/forgot-password", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            email: email
        })
    }).then(response => {
        if (response.status !== 201) {
            window.location.reload();
        } else {
            window.location.href = window.location.origin + "/login";
        }
    });
}