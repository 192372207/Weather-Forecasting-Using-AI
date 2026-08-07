import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyD2Fi4T39x2uInkcZjUcgWlX4_eGR2rv1w",
  authDomain: "skysense-854da.firebaseapp.com",
  projectId: "skysense-854da",
  storageBucket: "skysense-854da.firebasestorage.app",
  messagingSenderId: "521559511421",
  appId: "1:521559511421:web:f61fac484769a9ba713c14",
  measurementId: "G-74RVVEF36J"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const googleProvider = new GoogleAuthProvider();
export default app;
