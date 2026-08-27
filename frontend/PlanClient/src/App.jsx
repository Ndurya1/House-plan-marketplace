import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import BrowsePage from './pages/BrowsePage';
import Register from './components/register';
import SellerDashboard from './pages/SellerDashboard';
import AboutPage from './pages/AboutPage';
import SideNav from './components/sideNav';
import MobileNav from './components/MobileNav';
export default function App() {
  return (
    <Router>
      <div className="min-h-screen font-sans antialiased text-slate-900 bg-slate-50">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/plans/:category" element={<BrowsePage />} />
          <Route path="/signUp" element={<Register />} />
          <Route path="/dashboard" element={<SellerDashboard />} />
          <Route path="*" element={<div>404 Not Found</div>} />
          <Route path="sidebar" element={<SideNav/> }/>
          <Route path="mobile-nav" element={<MobileNav/> }/>
        </Routes>
      </div>
    </Router>
  );
}
