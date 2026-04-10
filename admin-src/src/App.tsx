import { BrowserRouter, Routes, Route, Navigate, NavLink, useNavigate } from "react-router-dom";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Projects from "./pages/Projects";
import Articles from "./pages/Articles";
import Experiences from "./pages/Experiences";
import Gallery from "./pages/Gallery";
import Roster from "./pages/Roster";
import Messages from "./pages/Messages";
import Skills from "./pages/Skills";

function isLoggedIn() {
  return !!localStorage.getItem("admin_token");
}

function Sidebar() {
  const navigate = useNavigate();
  const logout = () => {
    localStorage.removeItem("admin_token");
    navigate("/login");
  };
  const links = [
    { to: "/", label: "Dashboard" },
    { to: "/projects", label: "Projets" },
    { to: "/articles", label: "Articles" },
    { to: "/experiences", label: "Experiences" },
    { to: "/gallery", label: "Galerie" },
    { to: "/roster", label: "Roster" },
    { to: "/messages", label: "Messages" },
    { to: "/skills", label: "Competences" },
  ];
  return (
    <aside className="sidebar">
      <div className="sidebar-logo">Admin Panel</div>
      <nav className="sidebar-nav">
        {links.map((l) => (
          <NavLink key={l.to} to={l.to} end={l.to === "/"} className={({ isActive }) => isActive ? "active" : ""}>
            {l.label}
          </NavLink>
        ))}
      </nav>
      <div className="sidebar-footer">
        <button onClick={logout}>Deconnexion</button>
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
