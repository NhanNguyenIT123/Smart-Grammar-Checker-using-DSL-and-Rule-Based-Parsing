import { BrowserRouter, Routes, Route } from "react-router-dom";

import HomePage from "@/pages/HomePage";
import AuthPortal from "@/pages/AuthPortal";
import GrammarWorkspace from "@/pages/GrammarWorkspace";

function App() {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<HomePage />} />

          <Route path="/login" element={<AuthPortal />} />
          <Route path="/register" element={<AuthPortal />} />
          <Route path="/forgot-password" element={<AuthPortal />} />

          <Route path="/grammar" element={<GrammarWorkspace />} />
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
