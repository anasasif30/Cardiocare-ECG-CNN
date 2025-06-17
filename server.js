const path = require("path");
const findConfig = require("find-config");
const dotenv = require("dotenv");
const express = require("express");
const cors = require("cors");
const connectDB = require("../config/db.js");
const authRoutes = require("../routes/auth.js");
//const uploadRoutes = require("../routes/uploadRoutes.js");
const mongoose = require("mongoose");

dotenv.config({ path: findConfig(".env") });

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

const PORT = process.env.PORT || 8000;

// Debugging
console.log("MONGO_URI:", process.env.MONGO_URI);

// Start Server
async function startServer() {
    try {
        console.log("✅ Starting server...");

        await connectDB();
        console.log("✅ Database connection established");

        // Routes
        app.use("/api/auth", authRoutes);
      //  app.use("/api/upload", uploadRoutes);

        app.listen(PORT, () => console.log(`🚀 Server running on port ${PORT}`));
    } catch (err) {
        console.error("❌ Failed to start server:", err);
        process.exit(1);
    }
}

startServer();
