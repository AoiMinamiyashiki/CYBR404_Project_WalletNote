document.addEventListener("DOMContentLoaded", () => {
  // Button elements
  const recallBtn = document.querySelector(".recall");
  const historyBtn = document.querySelector(".history");
  const inBtn = document.querySelector(".in");
  const outBtn = document.querySelector(".out");
  const photoBtn = document.querySelector(".photo");
  const saveBtn = document.querySelector(".save");

  // Input fields
  const dateInput = document.querySelector('input[placeholder="Date"]');
  const serviceInput = document.querySelector('input[placeholder="Product or Service"]');
  const priceInput = document.querySelector('input[placeholder="Price"]');

  let currentType = "OUT"; // default

  // -----------------------------
  // IN / OUT toggle
  // -----------------------------
  inBtn.addEventListener("click", () => {
    currentType = "IN";
    inBtn.style.backgroundColor = "#4CAF50";
    outBtn.style.backgroundColor = "#ccc";
  });

  outBtn.addEventListener("click", () => {
    currentType = "OUT";
    outBtn.style.backgroundColor = "#E74C3C";
    inBtn.style.backgroundColor = "#ccc";
  });

  // -----------------------------
  // Save Information
  // -----------------------------
  saveBtn.addEventListener("click", () => {
    const data = {
      date: dateInput.value,
      service: serviceInput.value,
      price: Number(priceInput.value),
      type: currentType
    };

    if (!data.date || !data.service || !data.price) {
      alert("Please fill all fields.");
      return;
    }

    fetch("/api/record", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(() => {
      alert("Saved successfully");
      dateInput.value = "";
      serviceInput.value = "";
      priceInput.value = "";
    })
    .catch(err => {
      console.error(err);
      alert("Save failed");
    });
  });

  // -----------------------------
  // Recall (simple reload dashboard)
  // -----------------------------
  recallBtn.addEventListener("click", () => {
    window.location.reload();
  });

  // -----------------------------
  // Show Used History
  // -----------------------------
  historyBtn.addEventListener("click", () => {
    fetch("/api/records")
      .then(res => res.json())
      .then(data => {
        console.log("History:", data);
        alert(`History loaded: ${data.length} records (check console)`);
      });
  });

  // -----------------------------
  // Take Photo (OCR placeholder)
  // -----------------------------
  photoBtn.addEventListener("click", () => {
    alert("Photo OCR feature will be implemented here.");
  });
});
