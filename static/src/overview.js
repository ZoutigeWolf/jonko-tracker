window.onload = () => {
    highlightSelectedSidebarButton();
    loadStatistics();
};

function loadStatistics() {
    let grid = document.getElementById("overview-grid");
    grid.innerHTML = "";

    fetch(window.location.origin + "/api/statistics")
        .then(response => response.json())
        .then(statistics => statistics.forEach(stat => {
            grid.innerHTML += createWidget(stat.title, stat.data);
        }));

    const createWidget = (name, data) => `
        <div class="overview-widget">
            <p class="overview-widget-header">${name}</p>
            <p class="overview-widget-content">${data}</p>
        </div>`;
}