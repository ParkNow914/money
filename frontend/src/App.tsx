import { Routes, Route } from "react-router-dom";

import Header from "./components/Header";
import Footer from "./components/Footer";
import Home from "./pages/Home";
import IADemo from "./pages/IADemo";
import Marketplace from "./pages/Marketplace";
import Admin from "./pages/Admin";

function App() {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col">
      <Header />
      <main className="flex-1 w-full max-w-6xl mx-auto px-4 py-8">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/ia-demo" element={<IADemo />} />
          <Route path="/marketplace" element={<Marketplace />} />
          <Route path="/admin" element={<Admin />} />
        </Routes>
      </main>
      <Footer />
    </div>
  );
}

export default App;
