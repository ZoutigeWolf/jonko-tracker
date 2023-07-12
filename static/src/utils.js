function getCurrentDate() {
    let d = new Date();

    return d.getFullYear() + "-"
    + (d.getMonth() + 1).toString().padStart(2, "0") + "-"
    + d.getDate().toString().padStart(2, "0") + "T"
    + d.getHours().toString().padStart(2, "0") + ":"
    + d.getMinutes().toString().padStart(2, "0") + ":"
    + d.getSeconds().toString().padStart(2, "0");
}

function getMonthName(month) {
    const monthNames = ["January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ];

    return monthNames[month];
}