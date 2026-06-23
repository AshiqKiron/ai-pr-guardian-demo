// ⚠️ VULNERABLE CODE - FOR TESTING ONLY

// VIOLATION: Hardcoded API Keys
const API_KEY = "sk-test-abc123def456ghi789jkl012mno345";
const SECRET_KEY = "whsec_1234567890abcdefghijklmnop";

// VIOLATION: Stripe Keys
const STRIPE_SECRET = "sk_live_51HG4abc123def456ghi789jkl";

function connectToDatabase() {
    // Using hardcoded credentials
    const DB_URL = "mongodb://admin:SuperSecret123@cluster0.mongodb.net/mydb";
    return DB_URL;
}
