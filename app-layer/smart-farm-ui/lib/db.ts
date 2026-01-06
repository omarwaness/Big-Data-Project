import mongoose from 'mongoose';

const MONGODB_URI = process.env.MONGODB_URI || "mongodb://mongodb:27017/farm";

export const connectDB = async () => {
  try {
    if (mongoose.connection.readyState >= 1) {
      console.log("--> Using existing DB connection");
      return;
    }
    
    console.log("--> Attempting to connect to MongoDB at:", MONGODB_URI);
    const conn = await mongoose.connect(MONGODB_URI);
    
    console.log(`--> MongoDB Connected: ${conn.connection.host}`);
  } catch (error) {
    console.error("--> MongoDB Connection Error:", error);
  }
};