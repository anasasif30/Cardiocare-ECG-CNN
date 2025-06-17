import React from "react";
import ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Layout from "../src/components/Layout/Layout";
import Home from "../src/components/Home/Home";
import Login from "./components/Login/Login";
import Signup from "./components/Sign-up/signup";
import Dashboard from "./components/Dashboard/Dashboard";
import CardiovascularDisease from "./components/CardiovascularDisease/CardiovascularDisease";
import CardiologistFinder from "./components/CardiologistFinder/CardiologistFinder";


const router = createBrowserRouter([
  {
    path: "/", 
    element: <Layout />, // Parent component (Includes Navbar)
    children: [
      { path: "/", element: <Home /> }, 
      { path: "/login", element: <Login /> }, 
      { path: "/signup", element: <Signup /> }, 
      { path: "/dashboard", element: <Dashboard /> }, 
      { path: "/cvd", element: <CardiovascularDisease /> }, 
      { path: "/finder", element: <CardiologistFinder /> }
    ],
  },
]);

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);







// import { StrictMode } from 'react'
// import { createRoot } from 'react-dom/client'
// import './index.css'
// import App from './App.jsx'

// createRoot(document.getElementById('root')).render(
//   <StrictMode>
//     <App />
//   </StrictMode>,
// )
