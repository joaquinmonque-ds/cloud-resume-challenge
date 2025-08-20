// ==============================
// Navigation Menu Toggle & Smooth Scroll
// ==============================

function toggleMenu() {
  const menu = document.querySelector(".menu-links");
  const icon = document.querySelector(".hamburger-icon");
  menu.classList.toggle("open"); // Toggle the mobile menu visibility
  icon.classList.toggle("open"); // Toggle the hamburger icon animation
}

// Add smooth scrolling for all menu link clicks
document.querySelectorAll(".menu-links a").forEach((anchor) => {
  anchor.addEventListener("click", function (e) {
    const target = document.querySelector(this.getAttribute("href"));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: "smooth" }); // Smooth scroll to section
      toggleMenu(); // Close the menu after navigating
    }
  });
});

// ==============================
// Visitor Counter
// ==============================

// Base URL for API Gateway (update this if the API changes)
const API_BASE = "https://bfa8d5o6wk.execute-api.us-east-1.amazonaws.com/Prod";

// Function to increment visitor count in DynamoDB
async function incrementVisitorCount() {
  try {
    await fetch(`${API_BASE}/put`, { method: "POST" });
  } catch (error) {
    console.error("Error incrementing visitor count:", error);
  }
}

// Function to fetch the current visitor count from DynamoDB
async function fetchVisitorCount() {
  try {
    const response = await fetch(`${API_BASE}/get`);
    const data = await response.json();
    document.getElementById("replaceme").innerText = data.count; // Update DOM with count
  } catch (error) {
    console.error("Error fetching visitor count:", error);
  }
}

// Run visitor counter logic on page load
document.addEventListener("DOMContentLoaded", async () => {
  await incrementVisitorCount(); // First increment
  await fetchVisitorCount(); // Then fetch and display

  // Refresh the visitor count every 10 seconds (10000 ms).
  setInterval(fetchVisitorCount, 10000);
});
