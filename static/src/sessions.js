window.onload = () => {
    highlightSelectedSidebarButton();

    loadSessions();
};

function loadSessions() {
    const listParent = document.getElementById("session-list");
    listParent.innerHTML = "";

    fetch(window.location.origin + "/api/sessions")
        .then(response => response.json())
        .then(sessions => {
            fetch(window.location.origin + "/api/locations")
                .then(response => response.json())
                .then(locations => {
                    sessions.map(s => s.date_time = new Date(s.date_time));
                    sessions.map(s => s.location = locations.find(l => l.id === s.location_id));
                    sessions.sort((a, b) => b.date_time- a.date_time);

                    let lastDate = sessions[0].date_time.getDate();

                    let sArr = [];

                    sessions.forEach(s => {
                        if (s.date_time.getDate() === lastDate) {
                            sArr.push(s);
                        } else {
                            createGroup(sArr);
                            sArr = [s];
                        }
            });

            if (sArr.length !== 0) {
                createGroup(sArr);
            }
                });
        });

    const createGroup = (sessions) => {
        const createItem = (session) => {
            return `
            <div id="session-item">
                <p id="session-location"><i class="fa-solid fa-location-dot"></i>${session.location.name}</p>
            </div>`
        };

        let sHtml = sessions.map(createItem).join("\n");

        let date = sessions[0].date_time;
        let dateString = `${date.getDate()} ${getMonthName(date.getMonth())} ${date.getFullYear()}`;

        let groupHtml = `
            <div id="session-group">
                <p>${dateString}</p>
                <div id="separator"></div>
                ${sHtml}
            </div>`;

        listParent.innerHTML += groupHtml;
    };
}

async function getLocation(location_id) {
    let location = null;
    let response= await fetch(window.location.origin + `/api/locations/${location_id}`)

    if (response.status === 200) {
        location = response.json();
    }

    return location;
}