import { useState, type FormEvent } from "react";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");
    try {
      const body = new URLSearchParams({ username, password });
      const r = await fetch("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded", "x-site-id": "1" },
        body: body.toString(),
      });
      if (!r.ok) { setError("Identifiants incorrects"); return; }
      const data = await r.json() as { access_token: string };
      localStorage.setItem("admin_token", data.access_token);
      navigate("/");
    } catch {
      setError("Erreur de connexion");
    }
  };

  return (
    <div className="login-wrap">
      <div className="login-box">
        <h1>Admin Panel</h1>
        {error && <div className="msg msg-error">{error}</div>}
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Identifiant</label>
            <input value={username} onChange={(e) => setUsername(e.target.value)} required autoFocus />
          </div>
          <div className="form-group">
            <label>Mot de passe</label>
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
          </div>
          <button type="submit" className="btn btn-primary">Connexion</button>
        </form>
      </div>
    </div>
  );
}
