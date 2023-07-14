let currentEditingId = null;

let map;
let marker;

let isLoading = false;

window.onload = () => {
    highlightSelectedSidebarButton();
    loadLocations();
    initEditingEvents();
    loadMap();

    let searchParams = new URLSearchParams(window.location.search);
    let locationId = searchParams.get("id");

    if (locationId !== null) {
        editLocation(locationId);
    }
}

function loadMap() {
    map = new L.map("editor-map", {
        center: [0, 0],
        zoom: 3,
        doubleClickZoom: false
    });

    marker = L.marker([0, 0]).addTo(map);

    L.tileLayer('https://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}',{
        maxZoom: 20,
        subdomains:['mt0','mt1','mt2','mt3'],
        attribution: '&copy; <a href="https://maps.google.com">Google Maps</a>',
        crossOrigin: true
    }).addTo(map);

    map.addEventListener("dblclick", (e) => {
        let latInput = document.getElementById("editor-latitude-input");
        let lngInput = document.getElementById("editor-longitude-input");

        latInput.value = e.latlng.lat.toFixed(6);
        lngInput.value = e.latlng.lng.toFixed(6);

        submitLocationEdit();

        marker.setLatLng(e.latlng);
    });
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
           editLocation(location.id);
        });
}

function initEditingEvents() {
    let nameInput = document.getElementById("editor-name-input");
    let latInput = document.getElementById("editor-latitude-input");
    let lngInput = document.getElementById("editor-longitude-input");

    [nameInput, latInput, lngInput].forEach(e => e.addEventListener("change", submitLocationEdit));

    document.getElementById("editor-delete-button").addEventListener("click", () => {
        if (confirm("Are you sure you want to delete this location?")) {
            submitLocationDeletion();
        }
    });

    document.getElementById("locations-list")
        .addEventListener("click", () => toggleSidebar(false));

    document.getElementById("new-location-button")
        .addEventListener("click", () =>
            navigator.geolocation.getCurrentPosition(
                position => createNewLocation(position.coords.latitude, position.coords.longitude),
                () => createNewLocation(0, 0), {
                    enableHighAccuracy: true
                }));
}

function submitLocationEdit() {
    let nameInput = document.getElementById("editor-name-input");
    let latInput = document.getElementById("editor-latitude-input");
    let lngInput = document.getElementById("editor-longitude-input");

    fetch(window.location.origin + "/api/locations/" + currentEditingId, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            name: nameInput.value,
            latitude: latInput.value,
            longitude: lngInput.value,
        })
    }).then(loadLocations);
}

function submitLocationDeletion() {
    fetch(window.location.origin + "/api/locations/" + currentEditingId, {
        method: "DELETE"
    }).then(() => {
        loadLocations();
        toggleSidebar(false);
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
                    if (currentEditingId === el.dataset.locationid) {
                        toggleSidebar(false);
                        return;
                    }

                    e.stopPropagation();
                    editLocation(el.dataset.locationid);
                });

                locationsList.appendChild(el);
            })

            isLoading = false;
        });

    const createItem = (location) => `
        <div id="locations-item" class="locations-item-row" data-locationid="${location.id}">
            <p id="location-item-name">${location.name}</p>
            <p id="location-item-geo">${location.geo_data}</p>
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

                map.setView([location.latitude, location.longitude], 16);
                marker.setLatLng([location.latitude, location.longitude]);
            });
        });

    currentEditingId = locationId;

    toggleSidebar(true);
}

function toggleSidebar(show) {
    let sideBar = document.getElementById("locations-sidebar");
    let grid = document.getElementById("locations-page-content");

    sideBar.style.display = show ? "flex" : "none";
    grid.style.gridTemplateColumns = show ? "1fr 350px" : "1fr";

    if (!show) {
        currentEditingId = null;
    }

    map.invalidateSize(false);
}

function createElementFromHTML(htmlString) {
    let div = document.createElement("div");
    div.innerHTML = htmlString.trim();

    return div.firstChild;
}