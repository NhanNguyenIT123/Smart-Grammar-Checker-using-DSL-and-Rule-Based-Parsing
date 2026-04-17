import { BrowserRouter, Routes, Route } from "react-router-dom";

import HomePage from "@/pages/HomePage";
import AuthPage from "@/pages/AuthPage";
import GrammarChecker from "./pages/GrammarChecker";

function App() {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<HomePage />} />

          <Route path="/login" element={<AuthPage />} />
          <Route path="/register" element={<AuthPage />} />
          <Route path="/forgot-password" element={<AuthPage />} />

          <Route path="/grammar" element={<GrammarChecker />} />
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
