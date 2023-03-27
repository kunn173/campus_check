window.onload = function () {
    const map = L.map('map', {
        center: [54.8, -4.6],
        zoom: 5
    });// Central of United Kingdom
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© <a href=" ">OpenStreetMap</a > contributors'
    }).addTo(map);

    let mapEle = document.getElementById('map');
    let locations = mapEle.getAttribute('data-locations')
    locations = JSON.parse(locations)
    console.log('locations', locations)
    for (let i = 0; i < locations.length; i++) {
       let marker = L.marker([locations[i].latitude, locations[i].longitude]).bindPopup(locations[i].name).addTo(map)
        // marker on click event redirect to university detail page
        marker.on('click', function (e) {
            window.location.href = `/universities/university_detail/${locations[i].university_slug}/`
        }
        )
    }
}


