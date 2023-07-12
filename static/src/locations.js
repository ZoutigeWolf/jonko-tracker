window.onload = () => {
    highlightSelectedSidebarButton();
    loadLocations();

    let searchParams = new URLSearchParams(window.location.search);
    let locationId = searchParams.get("id");

    if (locationId !== null) {
        editLocation(locationId);
    }
}

function loadLocations() {
    const locationsList = document.getElementById("locations-list");
    locationsList.innerHTML = "";

    fetch(window.location.origin + "/api/locations")
        .then(response => response.json())
        .then(locations => locations.forEach(l => {
            getGeoInfo(l.latitude, l.longitude)
                .then(geoData => {
                    let el = createElementFromHTML(createItem(l, geoData));
                    el.addEventListener("click", () => editLocation(el.dataset.locationid));

                    locationsList.appendChild(el);
                });
        }));

    const createItem = (location, geoData) => `
        <div id="locations-item" class="locations-item-row" data-locationid="${location.id}">
            <p id="location-item-name">${location.name}</p>
            <p id="location-item-geo">${geoData.city}, ${geoData.country}</p>
        </div>`;
}

function editLocation(locationId) {
    let nameInput = document.getElementById("editor-name-input");
    let latInput = document.getElementById("editor-latitude-input");
    let lngInput = document.getElementById("editor-longitude-input");

    fetch(window.location.origin + "/api/locations/" + locationId)
        .then(response => {
            if (response.status !== 200) {
                return;
            }

            response.json().then(location => {
                nameInput.value = location.name;
                latInput.value = location.latitude;
                lngInput.value = location.longitude;
            });
        });
}

async function getGeoInfo(lat, lng) {
    let response = await fetch(`https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=${lat}&longitude=${lng}`);

    if (response.status !== 200){
        return null;
    }

    let data = await response.json();

    return {
        city: data.city,
        country: data.countryName
    };
}

function createElementFromHTML(htmlString) {
    let div = document.createElement("div");
    div.innerHTML = htmlString.trim();

    return div.firstChild;
}