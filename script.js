const API_BASE = "https://your-backend.onrender.com";  // apna backend URL daalna

document.getElementById("uploadForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const fileInput = document.getElementById("fileInput");
  const file = fileInput.files[0];

  let formData = new FormData();
  formData.append("file", file);

  let res = await fetch(`${API_BASE}/upload`, {
    method: "POST",
    body: formData,
  });

  let data = await res.json();
  document.getElementById("status").innerText = "Task ID: " + data.task_id;

  // Polling status
  let interval = setInterval(async () => {
    let statusRes = await fetch(`${API_BASE}/status/${data.task_id}`);
    let statusData = await statusRes.json();
    document.getElementById("status").innerText = JSON.stringify(statusData);
    if (statusData.status === "Done") clearInterval(interval);
  }, 3000);
});
