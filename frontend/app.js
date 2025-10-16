async function uploadFile() {
  const fileInput = document.getElementById("fileInput");
  if (!fileInput.files.length) return alert("Please choose a file");

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  const res = await fetch("http://127.0.0.1:8000/extract", {
    method: "POST",
    body: formData,
  });

  const data = await res.json();
  document.getElementById("output").textContent = JSON.stringify(data, null, 2);
}
