function showParkingLot() {
  fetch("/getLotData")
    .then((response) => response.json())
    .then((data) => {
      displayParkingLot(data);
    })
    .catch((error) => console.error("Error:", error));
}

function displayParkingLot(data) {
  const parkingLotDiv = document.getElementById("parkingLot");
  parkingLotDiv.innerHTML = ""; // Clear previous content

  const slots = data.slots;
  for (let i = 0; i < slots.length; i++) {
    const slot = slots[i];
    const slotDiv = document.createElement("div");
    slotDiv.classList.add("slot");
    slotDiv.style.backgroundColor = getSlotColor(slot.status);
    slotDiv.innerHTML = slot.id;
    parkingLotDiv.appendChild(slotDiv);
  }
}

function getSlotColor(status) {
  if (status === "occupied") {
    return "#D70040";
  } else if (status === "available") {
    return "#097969";
  } else {
    return "#1434A4";
  }
}

function showMessage(message, success) {
  const messageDiv = document.getElementById("message");
  messageDiv.textContent = message;
  messageDiv.style.display = "block";
  if (success) {
    messageDiv.style.backgroundColor = "#097969"; // Success message color
  } else {
    messageDiv.style.backgroundColor = "#D70040"; // Error message color
  }
  setTimeout(() => {
    messageDiv.style.display = "none";
  }, 3000); // Hide message after 3 seconds
}

function bookLot() {
  const lotNumber = document.getElementById("lotNumber").value;
  if (lotNumber == "" || Number(lotNumber) > 50 || Number(lotNumber) < 1) {
    showMessage("Enter a valid lot number!", false);
    return 1;
  }
  document.getElementById("lotNumber").value = "";
  fetch("/bookSlot", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ lotNumber: lotNumber }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        showMessage("Lot booked successfully!", true);
      } else {
        showMessage("Lot booking failed", false);
      }
    })
    .catch((error) => {
      showMessage("Lot booking failed", false);
      console.error("Error:", error);
    });
}

function showProfileDetails() {
  var profileDetails = document.getElementById("profileDetails");
  if (profileDetails.style.display === "none") {
    profileDetails.style.display = "block";
    // Fetch and populate profile details here
  } else {
    profileDetails.style.display = "none";
  }
}
