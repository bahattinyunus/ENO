function updateClock() {
    const now = new Date();
    document.getElementById('sys-clock').innerText = now.toISOString().split('T')[1].split('.')[0];
}
setInterval(updateClock, 1000);

async function fetchData() {
    try {
        // 1. Status
        const statusRes = await fetch('/api/status');
        const statusData = await statusRes.json();
        
        document.getElementById('cpu-bar').style.width = statusData.hardware.cpu + '%';
        document.getElementById('cpu-val').innerText = statusData.hardware.cpu + '%';
        
        document.getElementById('mem-bar').style.width = statusData.hardware.memory + '%';
        document.getElementById('mem-val').innerText = statusData.hardware.memory + '%';
        
        document.getElementById('temp-val').innerText = statusData.hardware.temp + '°C';
        document.getElementById('uptime-val').innerText = Math.floor(statusData.system.uptime % 10000) + 's'; // Mock uptime

        // 2. Traffic
        const trafficRes = await fetch('/api/traffic');
        const trafficData = await trafficRes.json();
        const trafficLog = document.getElementById('traffic-log');
        
        trafficLog.innerHTML = '';
        trafficData.forEach(log => {
            const div = document.createElement('div');
            div.className = `log-entry ${log.status}`;
            div.innerHTML = `<span class="time">[${log.time}]</span> ${log.encrypted} <span style="opacity:0.5">(${log.status})</span>`;
            trafficLog.appendChild(div);
        });

        // 3. Alerts
        const alertsRes = await fetch('/api/alerts');
        const alertsData = await alertsRes.json();
        const alertList = document.getElementById('alert-list');
        
        if (alertsData.length > 0) {
            alertList.innerHTML = '';
            alertsData.forEach(alert => {
                const li = document.createElement('li');
                li.innerText = alert.alert;
                alertList.appendChild(li);
            });
            document.querySelector('.radar-circle').style.borderColor = 'red';
            document.querySelector('.radar-swipe').style.background = 'linear-gradient(45deg, rgba(255, 0, 0, 0.5), transparent)';
        } else {
             alertList.innerHTML = '<li>No Active Threats Detected</li>';
             document.querySelector('.radar-circle').style.borderColor = 'rgba(0, 243, 255, 0.3)';
             document.querySelector('.radar-swipe').style.background = 'linear-gradient(45deg, rgba(0, 243, 255, 0.5), transparent)';
        }

    } catch (error) {
        console.error("Connection Lost", error);
    }
}

// Poll every 1 second
setInterval(fetchData, 1000);
fetchData();
