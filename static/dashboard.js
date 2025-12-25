// Initialize Socket Connection
const socket = io();

// 1. Initialize Map
const map = L.map('map').setView([39.0, 35.0], 6); // Turkey View
L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; OpenStreetMap &copy; CARTO',
    subdomains: 'abcd',
    maxZoom: 19
}).addTo(map);

// Markers Store
const markers = {};

// 2. Socket Event Listeners

socket.on('connect', () => {
    console.log("Connected to ENO Uplink");
    document.querySelector('.status-ok').innerText = "ONLINE (WS)";
});

socket.on('disconnect', () => {
    document.querySelector('.status-ok').innerText = "DISCONNECTED";
    document.querySelector('.status-ok').style.color = "red";
});

// Map Updates
socket.on('map_update', (units) => {
    units.forEach(unit => {
        if (markers[unit.id]) {
            // Update existing marker
            markers[unit.id].setLatLng([unit.lat, unit.lon]);
            markers[unit.id].setPopupContent(`<b>${unit.id}</b><br>Type: ${unit.type}<br>Status: ${unit.status}`);
        } else {
            // Create new marker
            const markerColor = unit.type === 'UAV' ? 'cyan' : 'orange';
            // Simple circle marker for high-tech look
            const marker = L.circleMarker([unit.lat, unit.lon], {
                color: markerColor,
                fillColor: markerColor,
                fillOpacity: 0.5,
                radius: 6
            }).addTo(map);

            marker.bindPopup(`<b>${unit.id}</b><br>Type: ${unit.type}`);
            markers[unit.id] = marker;
        }
    });
});

// System Stats
socket.on('status_update', (data) => {
    document.getElementById('cpu-bar').style.width = data.hardware.cpu + '%';
    document.getElementById('cpu-val').innerText = data.hardware.cpu + '%';

    document.getElementById('mem-bar').style.width = data.hardware.memory + '%';
    document.getElementById('mem-val').innerText = data.hardware.memory + '%';

    document.getElementById('temp-val').innerText = data.hardware.temp + '°C';
    document.getElementById('uptime-val').innerText = Math.floor(data.system.uptime % 10000) + 's';
});

// Traffic Feed
socket.on('traffic_event', (log) => {
    const trafficLog = document.getElementById('traffic-log');
    const div = document.createElement('div');
    div.className = `log-entry ${log.status}`;
    div.innerHTML = `<span class="time">[${log.time}]</span> ${log.encrypted} <span style="opacity:0.5">(${log.status})</span>`;

    trafficLog.insertBefore(div, trafficLog.firstChild);

    if (trafficLog.children.length > 30) {
        trafficLog.removeChild(trafficLog.lastChild);
    }
});

// Alerts
socket.on('alert_event', (alert) => {
    const alertList = document.getElementById('alert-list');
    const li = document.createElement('li');
    li.innerText = `[${alert.time}] ${alert.alert}`;
    li.style.color = '#ff2a2a';
    li.style.borderLeft = '2px solid #ff2a2a';
    li.style.paddingLeft = '5px';

    alertList.insertBefore(li, alertList.firstChild);
});

// Helper: Local Clock
setInterval(() => {
    const now = new Date();
    document.getElementById('sys-clock').innerText = now.toISOString().split('T')[1].split('.')[0];
}, 1000);
