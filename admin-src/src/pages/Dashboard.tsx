import { useEffect, useState } from "react";
import { get } from "../lib/api";

export default function Dashboard() {
  const [counts, setCounts] = useState({ projects: 0, articles: 0, experiences: 0, skills: 0, messages: 0 });

  useEffect(() => {
    Promise.all([
      get<unknown[]>("/portfolio/projects").catch(() => [] as unknown[]),
      get<unknown[]>("/articles").catch(() => [] as unknown[]),
      get<unknown[]>("/experience").catch(() => [] as unknown[]),
      get<unknown[]>("/skills").catch(() => [] as unknown[]),
      get<unknown[]>("/messages").catch(() => [] as unknown[]),
    ]).then(([p, a, e, s, m]) => {
      setCounts({ projects: p.length, articles: a.length, experiences: e.length, skills: s.length, messages: m.length });
    });
  }, []);

  const items = [
    { label: "Projets", num: counts.projects },
    { label: "Articles", num: counts.articles },
    { label: "Experiences", num: counts.experiences },
    { label: "Competences", num: counts.skills },
    { label: "Messages", num: counts.messages },
  ];

  return (
    <>
      <div className="page-header">
        <h1>Dashboard</h1>
      </div>
      <div className="dash-grid">
        {items.map((item) => (
          <div key={item.label} className="dash-card">
            <div className="dash-num">{item.num}</div>
            <div className="dash-label">{item.label}</div>
          </div>
        ))}
      </div>
    </>
  );
}
