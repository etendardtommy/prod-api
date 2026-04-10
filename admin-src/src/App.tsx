import { BrowserRouter, Routes, Route, Navigate, NavLink, useNavigate } from "react-router-dom";
import { useState } from "react";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Projects from "./pages/Projects";
import Articles from "./pages/Articles";
import Experiences from "./pages/Experiences";
import Gallery from "./pages/Gallery";
import Roster from "./pages/Roster";
import Messages from "./pages/Messages";
import Skills from "./pages/Skills";
import { getSiteId, setSiteId } from "./lib/api";

function isLoggedIn() {
  return !!localStorage.getItem("admin_token");
}

const SITES = [
  { id: "1", label: "Portfolio" },
  { id: "2", label: "Eclyps" },
];

const NAV_BY_SITE: Record<string, { to: string; label: string }[]> = {
  "1": [
    { to: "/", label: "Dashboard" },
    { to: "/projects", label: "Projets" },
    { to: "/articles", label: "Articles" },
    { to: "/experiences", label: "Expériences" },
    { to: "/skills", label: "Compétences" },
    { to: "/messages", label: "Messages" },
  ],
  "2": [
    { to: "/", label: "Dashboard" },
    { to: "/gallery", label: "Galerie" },
    { to: "/roster", label: "Roster" },
    { to: "/messages", label: "Messages" },
  ],
};

function Sidebar() {
  const navigate = useNavigate();
  const [siteId, setSiteIdState] = useState(getSiteId());

  const handleSiteChange = (id: string) => {
    setSiteId(id);
    setSiteIdState(id);
    navigate("/");
  };

  const logout = () => {
    localStorage.removeItem("admin_token");
    navigate("/login");
  };

  const links = NAV_BY_SITE[siteId] ?? NAV_BY_SITE["1"];

  return (
    <aside className="sidebar">
      <div className="sidebar-logo">⚙ Admin Panel</div>

      {/* Sélecteur de site */}
      <div className="site-selector">
        {SITES.map((site) => (
          <button
            key={site.id}
            className={`site-btn${siteId === site.id ? " active" : ""}`}
            onClick={() => handleSiteChange(site.id)}
          >
            {site.label}
          </button>
        ))}
      </div>

      <nav className="sidebar-nav">
        {links.map((l) => (
          <NavLink
            key={l.to}
            to={l.to}
            end={l.to === "/"}
            className={({ isActive }) => (isActive ? "active" : "")}
          >
            {l.label}
          </NavLink>
        ))}
      </nav>

      <div className="sidebar-footer">
        <button onClick={logout}>Déconnexion</button>
      </div>
    </aside>
  );
}

function Layout({ children }: { children: React.ReactNode }) {
  if (!isLoggedIn()) return <Navigate to="/login" replace />;
  return (
    <div className="layout">
      <Sidebar />
      <main className="main-content">{children}</main>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter basename="/admin">
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<Layout><Dashboard /></Layout>} />
        <Route path="/projects" element={<Layout><Projects /></Layout>} />
        <Route path="/articles" element={<Layout><Articles /></Layout>} />
        <Route path="/experiences" element={<Layout><Experiences /></Layout>} />
        <Route path="/gallery" element={<Layout><Gallery /></Layout>} />
        <Route path="/roster" element={<Layout><Roster /></Layout>} />
        <Route path="/messages" element={<Layout><Messages /></Layout>} />
        <Route path="/skills" element={<Layout><Skills /></Layout>} />
      </Routes>
    </BrowserRouter>
  );
}
