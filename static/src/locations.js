let isLoading = false;

window.onload = () => {
    highlightSelectedSidebarButton();
    loadLocations();

    document.getElementById("new-location-button")
        .addEventListener("click", () =>
            navigator.geolocation.getCurrentPosition(
                position => createNewLocation(position.coords.latitude, position.coords.longitude),
                () => createNewLocation(0, 0), {
                    enableHighAccuracy: true
                }));
}

function createNewLocation(lat ,lng) {
    fetch(window.location.origin + "/api/locations", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            name: "New location",
            latitude: lat.toFixed(6),
            longitude: lng.toFixed(6)
        })
    }).then(response => response.json())
        .then(location => {
           loadLocations();
        });
}

function loadLocations() {
    if (isLoading) {
        return;
    }

    isLoading = true;

    const locationsList = document.getElementById("locations-list");
    locationsList.innerHTML = "";

    fetch(window.location.origin + "/api/locations")
        .then(response => response.json())
        .then(locations => {
            locations.forEach(l => {
                let el = createElementFromHTML(createItem(l));
                el.addEventListener("click", (e) => {
                    window.location.href = window.location.origin + "/locations?id=" + l.id;
                });

                locationsList.appendChild(el);
            })

            isLoading = false;
        });

    const createItem = (location) => `
        <div id="locations-item" class="locations-item-row" data-locationid="${location.id}">
            <img src="${window.location.origin + `/api/locations/${location.id}.png`}">
            <p id="location-item-name">${location.name}</p>
            <p id="location-item-geo">${location.geo_data}</p>
        </div>`;
}

function createElementFromHTML(htmlString) {
    let div = document.createElement("div");
    div.innerHTML = htmlString.trim();

    return div.firstChild;
}