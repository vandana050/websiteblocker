async function fetchStatus() {
  const res = await fetch('/status');
  const data = await res.json();

  document.getElementById('status').textContent =
    data.active ? "Blocking: ACTIVE" : "Blocking: INACTIVE";

  document.getElementById('toggleBtn').textContent =
    data.active ? "Stop Blocking" : "Start Blocking";

  const list = document.getElementById('siteList');
  list.innerHTML = "";
  data.websites.forEach(w => {
    const li = document.createElement('li');
    li.textContent = w;
    list.appendChild(li);
  });

  document.getElementById('startTime').value = data.start.slice(0,5);
  document.getElementById('endTime').value = data.end.slice(0,5);
}

document.getElementById('toggleBtn').addEventListener('click', async () => {
  await fetch('/toggle', { method: 'POST' });
  fetchStatus();
});

document.getElementById('addBtn').addEventListener('click', async () => {
  const site = document.getElementById('newSite').value.trim();
  if (!site) return;
  await fetch('/update', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ site })
  });
  document.getElementById('newSite').value = '';
  fetchStatus();
});

document.getElementById('saveBtn').addEventListener('click', async () => {
  const start = document.getElementById('startTime').value;
  const end = document.getElementById('endTime').value;
  await fetch('/update', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ start, end })
  });
  alert("Working hours updated!");
});

fetchStatus();
