let map;

window.onload = () => {
    highlightSelectedSidebarButton();

    loadMap();
    loadLocations();
};

function loadMap() {
    map = new L.map('map', {
        center: [0, 0],
        zoom: 3,
        maxZoom: 18,
    });

    L.tileLayer('https://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}&hl=en',{
        maxZoom: 20,
        subdomains:['mt0','mt1','mt2','mt3'],
        attribution: '&copy; <a href="https://maps.google.com">Google Maps</a>',
        crossOrigin: true
    }).addTo(map);

    navigator.geolocation.getCurrentPosition(
        position => map.flyTo(new L.LatLng(position.coords.latitude, position.coords.longitude), 6),
        null, {
            enableHighAccuracy: true
    });
}

function loadLocations() {
    fetch(window.location.origin + "/api/locations")
        .then(response => response.json())
        .then(locations => {
            locations.forEach(l => L.marker([l.latitude, l.longitude], {
                title: l.name,
            }).addTo(map).bindPopup(`${l.name}<br><button onclick="window.location.href = window.location.origin + '/locations?id=${l.id}'">View</button>`));
        });
}