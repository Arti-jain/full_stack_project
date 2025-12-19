// Load Projects
fetch("/projects")
  .then(res => res.json())
  .then(data => {
    const container = document.getElementById("projects");
    data.forEach(p => {
      container.innerHTML += `
        <div class="card">
          <img src="${p.image}">
          <h3>${p.name}</h3>
          <p>${p.description}</p>
        </div>`;
    });
  });

// Load Clients
fetch("/clients")
  .then(res => res.json())
  .then(data => {
    const container = document.getElementById("clients");
    data.forEach(c => {
      container.innerHTML += `
        <div class="card">
          <img src="${c.image}">
          <h3>${c.name}</h3>
          <p>${c.designation}</p>
          <small>${c.description}</small>
        </div>`;
    });
  });

// Contact Form
document.getElementById("contactForm").onsubmit = function(e) {
  e.preventDefault();
  const formData = Object.fromEntries(new FormData(this));
  fetch("/contact", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(formData)
  }).then(() => alert("Message sent"));
};

// Newsletter
function subscribe() {
  const email = document.getElementById("email").value;
  fetch("/subscribe", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email })
  }).then(() => alert("Subscribed successfully"));
}
