// Import Firebase SDK
import { initializeApp } from "https://www.gstatic.com/firebasejs/11.4.0/firebase-app.js";
import { getDatabase, ref, set } from "https://www.gstatic.com/firebasejs/11.4.0/firebase-database.js";

// Firebase Configuration (Do NOT expose API keys in public repositories)
const firebaseConfig = {
    apiKey: "AIzaSyAfTY3nM3jbtUwS1GRKB_rRO9Sf6PFNUVE",  // Replace with secure environment key
    authDomain: "disastermanagement-7cf27.firebaseapp.com",
    databaseURL: "https://disastermanagement-7cf27-default-rtdb.firebaseio.com",
    projectId: "disastermanagement-7cf27",
    storageBucket: "disastermanagement-7cf27.appspot.com",
    messagingSenderId: "315237641108",
    appId: "1:315237641108:web:8dc2060da2b2e70432fd81",
    measurementId: "G-LW3HMVEZFK"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getDatabase(app);

// Function to trigger Python script automatically
function runPythonScript() {
    fetch("http://localhost:5000/run-python", {  // Replace with your actual backend URL
        method: "GET"
    })
    .then(response => response.json())
    .then(data => {
        console.log("Python script executed:", data);
    })
    .catch(error => {
        console.error("Error running Python script:", error);
    });
}

// Run the script automatically when the page loads
window.onload = () => {
    runPythonScript();
};

// Form Submission Handling
document.getElementById('myForm').addEventListener('submit', function (e) {
    e.preventDefault(); // Prevent default form submission

    // Get form values
    const name = document.getElementById('NameInp').value.trim();
    const phone = document.getElementById('PnoInp').value.trim();
    const email = document.getElementById('mailInp').value.trim();
    const address = document.getElementById('AddInp').value.trim();
    const state = document.getElementById('StateInp').value.trim();
    const country = document.getElementById('CounInp').value.trim();
    const pincode = document.getElementById('PinInp').value.trim();

    // Validate input fields
    if (!name || !phone || !email || !address || !state || !country || !pincode) {
        alert("Please fill all fields.");
        return;
    }

    // Firebase Database Reference
    const dbRef = ref(db, 'citizen/' + phone);

    // Store data in Firebase
    set(dbRef, {
        Name: name,
        PhoneNo: phone,
        Email: email,
        Address: address,
        State: state,
        Country: country,
        Pincode: pincode
    })
    .then(() => {
        alert('Form submitted successfully!');
        document.getElementById('myForm').reset(); // Reset form
    })
    .catch((error) => {
        alert('Error: ' + error.message);
    });
});
