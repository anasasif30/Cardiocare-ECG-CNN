const mongoose = require("mongoose");

const ecgSchema = new mongoose.Schema({
  userId: { type: mongoose.Schema.Types.ObjectId, ref: "User", required: true },
  image: { type: String, required: true }, // ✅ Store Base64 string
  prediction: { type: String, required: true },
  uploadedAt: { type: Date, default: Date.now },
}, { timestamps: true });

module.exports = mongoose.model("ECG", ecgSchema);
