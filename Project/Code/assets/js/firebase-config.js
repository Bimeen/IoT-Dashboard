const firebaseConfig = {
    apiKey: "AIzaSyCiO5C7z-tTmeWjQi_1UmbyZQuoh-Di_vk",
    authDomain: "ioot2-eb41f.firebaseapp.com",
    projectId: "ioot2-eb41f",
    storageBucket: "ioot2-eb41f.appspot.com",
    messagingSenderId: "1095872702306",
    appId: "1:1095872702306:web:dd1035e000fa41ae152e3b",
    measurementId: "G-5SPGPVYKM8"
};

// Initialize Firebase
const app = firebase.initializeApp(firebaseConfig);
const db = firebase.firestore();