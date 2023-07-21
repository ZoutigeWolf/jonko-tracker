let locationId;
let locationData;

let map;
let marker;

let editMap;
let editMarker;

window.onload = () => {
    let params = new URLSearchParams(window.location.search);

    if (!params.has("id")) {
        window.location.redirect(window.location.origin = "/locations");
        return;
    }

    locationId = params.get("id");

    loadMap();
    loadEditMap();

    loadLocation();

    document.getElementById("image-input")
        .addEventListener("change", () => submitImageEdit())
};

function loadMap() {
    map = new L.map('location-map', {
        center: [0, 0],
        zoom: 3,
        maxZoom: 18,
        scrollWheelZoom: false
    });

    marker = L.marker([0, 0]).addTo(map);

    L.tileLayer('https://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}&hl=en',{
        maxZoom: 20,
        subdomains:['mt0','mt1','mt2','mt3'],
        attribution: '&copy; <a href="https://maps.google.com">Google Maps</a>',
        crossOrigin: true
    }).addTo(map);
}

function loadEditMap() {
    editMap = new L.map('location-edit-map', {
        center: [0, 0],
        zoom: 3,
        maxZoom: 18,
        doubleClickZoom: false
    });

    editMarker = L.marker([0, 0]).addTo(editMap);

    L.tileLayer('https://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}&hl=en',{
        maxZoom: 20,
        subdomains:['mt0','mt1','mt2','mt3'],
        attribution: '&copy; <a href="https://maps.google.com">Google Maps</a>',
        crossOrigin: true
    }).addTo(editMap);

    editMap.addEventListener("dblclick", (e) => {
        let latInput = document.getElementById("lat-input");
        let lngInput = document.getElementById("lng-input");

        latInput.value = e.latlng.lat.toFixed(6);
        lngInput.value = e.latlng.lng.toFixed(6);

        editMarker.setLatLng(e.latlng);
    });
}

function showLocationEditor() {
    showPopup("edit-location-popup");
    editMap.invalidateSize(false);

    let nameInput = document.getElementById("name-input");
    let latInput = document.getElementById("lat-input");
    let lngInput = document.getElementById("lng-input");

    nameInput.value = locationData.name;
    latInput.value = locationData.latitude;
    lngInput.value = locationData.longitude;
}

function submitImageEdit() {
    let imageInput = document.getElementById("image-input");

    let reader = new FileReader()

    reader.onloadend = () => {
        if (reader.readyState !== FileReader.DONE) {
            return;
        }

        let bytes = reader.result;

        fetch(window.location.origin + "/api/locations/" + locationId, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                cover_image: bytes
            })
        }).then(response => {
            if (response.status === 200) {
                loadLocation();
            }
        })
    };

    reader.readAsDataURL(imageInput.files[0])
}

function submitEdit() {
    let nameInput = document.getElementById("name-input");
    let latInput = document.getElementById("lat-input");
    let lngInput = document.getElementById("lng-input");

    fetch(window.location.origin + "/api/locations/" + locationId, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            name: nameInput.value,
            latitude: latInput.value,
            longitude: lngInput.value,
        })
    }).then(response => {
        if (response.status === 200) {
            loadLocation();
            closePopup('edit-location-popup');
        }
    })
}

function loadLocation() {
    fetch(window.location.origin + "/api/locations/" + locationId)
        .then(response => {
            if (response.status === 404) {
                window.location.redirect(window.location.origin = "/locations");
                return;
            }

            response.json().then(location => {
                locationData = location;

                let imageEl = document.getElementById("location-image");
                let nameEl = document.getElementById("location-name");
                let geoEl = document.getElementById("location-geo");

                imageEl.src = window.location.origin + `/api/locations/${location.id}.png?t=${new Date().getTime()}`;
                nameEl.innerText = location.name;
                geoEl.innerText = location.geo_data;

                let pos = [location.latitude, location.longitude];

                map.setView(pos, 15);
                marker.setLatLng(pos);

                editMap.setView(pos, 15);
                editMarker.setLatLng(pos);
            });
        })
}

function arrayBufferToBase64(buffer) {
  let binary = "";
  const bytes = new Uint8Array(buffer);
  const len = bytes.byteLength;
  for (let i = 0; i < len; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  return btoa(binary);
}