let map;
let centerMarker;

window.onload = () => {
    highlightSelectedSidebarButton();

    loadMap();
};

function loadMap() {
    map = new L.map('small-map', {
        center: [0, 0],
        zoom: 3,
    });

    centerMarker = L.marker(map.getCenter()).addTo(map);

    L.tileLayer('https://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}',{
        maxZoom: 20,
        subdomains:['mt0','mt1','mt2','mt3'],
        attribution: '&copy; <a href="https://maps.google.com">Google Maps</a>'
    }).addTo(map);

    navigator.geolocation.getCurrentPosition(position => {
        map.flyTo(new L.LatLng(position.coords.latitude, position.coords.longitude), 15, {
            duration: 4
        });
    });

    ["move", "zoomstart", "zoomanim", "zoomend"].forEach(e => map.addEventListener(e, () => {
        centerMarker.setLatLng(map.getCenter());
    }));
}