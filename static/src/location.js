let locationId;

window.onload = () => {
    let params = new URLSearchParams(window.location.search);

    if (!params.has("id")) {
        window.location.redirect(window.location.origin = "/locations");
        return;
    }

    locationId = params.get("id");

    loadLocation();
};

function loadLocation() {
    fetch(window.location.origin + "/api/locations/" + locationId)
        .then(response => {
            if (response.status === 404) {
                window.location.redirect(window.location.origin = "/locations");
                return;
            }

            response.json().then(location => {
                let imageEl = document.getElementById("location-image");
                let nameEl = document.getElementById("location-name");
                let geoEl = document.getElementById("location-geo");

                imageEl.src = window.location.origin + `/api/locations/${location.id}.png`;
                nameEl.innerText = location.name;
                geoEl.innerText = location.geo_data;
            });
        })
}