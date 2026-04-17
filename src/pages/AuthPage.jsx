// src/pages/AuthPage.jsx
import { Box } from "@mui/material";
import { useLocation } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import Login from "../components/auth/Login";
import Register from "../components/auth/Register";
import ForgotPassword from "../components/auth/ForgotPassword";
import Navigation from "@/components/Navigation";

export default function AuthPage() {
  const location = useLocation();
  
  const renderAuthComponent = () => {
    switch (location.pathname) {
      case "/login": return <Login />;
      case "/forgot-password": return <ForgotPassword />;
      case "/register": return <Register />;
      default: return <Login />;
    }
  };

  return (
    <Box sx={{ minHeight: "100vh", width: "100vw", position: "relative", overflow: "hidden", display: "flex", flexDirection: "column" }}>
      <Box sx={{ position: "fixed", top: 0, left: 0, width: "100%", zIndex: 2 }}>
      <Navigation hideLinks={true}/>
      </Box>
      {/* LỚP NỀN: Luôn cố định, không bị ảnh hưởng bởi Animation */}
      <Box sx={{ position: "fixed", top: 0, left: 0, width: "100%", height: "100%", zIndex: 0 }}>
      </Box>

      {/* LỚP NỘI DUNG: Nằm trên nền (zIndex: 1) */}
      <Box
        sx={{
          position: "relative",
          zIndex: 1,
          height: "100vh",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <AnimatePresence mode="wait">
          <motion.div
            key={location.pathname} 
            initial={{ opacity: 0, y: 20 }} 
            animate={{ opacity: 1, y: 0 }} 
            exit={{ opacity: 0, y: -20 }} 
            transition={{ duration: 0.3 }}
            style={{ width: "100%", display: "flex", justifyContent: "center" }}
          >
            {renderAuthComponent()}
          </motion.div>
        </AnimatePresence>
      </Box>
    </Box>
  );
}