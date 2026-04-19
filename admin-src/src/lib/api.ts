const BASE = "/api";

export function getSiteId(): string {
  return localStorage.getItem("admin_site_id") || "1";
}

export function setSiteId(id: string) {
  localStorage.setItem("admin_site_id", id);
}

function getToken() {
  return localStorage.getItem("admin_token") || "";
}

function authHeaders(): Record<string, string> {
  return {
    "Authorization": `Bearer ${getToken()}`,
    "x-site-id": getSiteId(),
    "Content-Type": "application/json",
  };
}

function checkAuth(status: number) {
  if (status === 401) {
    localStorage.removeItem("admin_token");
    window.location.href = "/admin/login";
  }
}

export async function get<T>(path: string): Promise<T> {
  const r = await fetch(BASE + path, { headers: authHeaders() });
  checkAuth(r.status);
  if (!r.ok) throw new Error(await r.text());
  return r.json() as Promise<T>;
}

export async function post<T>(path: string, body: unknown): Promise<T> {
  const r = await fetch(BASE + path, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify(body),
  });
  if (!r.ok) throw new Error(await r.text());
  return r.json() as Promise<T>;
}

export async function put<T>(path: string, body: unknown): Promise<T> {
  const r = await fetch(BASE + path, {
    method: "PUT",
    headers: authHeaders(),
    body: JSON.stringify(body),
  });
  if (!r.ok) throw new Error(await r.text());
  return r.json() as Promise<T>;
}

export async function del(path: string): Promise<void> {
  await fetch(BASE + path, { method: "DELETE", headers: authHeaders() });
}

export async function uploadCV(file: File): Promise<void> {
  const form = new FormData();
  form.append("file", file);
  const r = await fetch(BASE + "/cv/upload", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${getToken()}`,
      "x-site-id": getSiteId(),
    },
    body: form,
  });
  if (!r.ok) throw new Error(await r.text());
}

export async function uploadImage(file: File): Promise<string> {
  const form = new FormData();
  form.append("file", file);
  const r = await fetch(BASE + "/upload/", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${getToken()}`,
      "x-site-id": getSiteId(),
    },
    body: form,
  });
  if (!r.ok) throw new Error(await r.text());
  const data = await r.json() as { url: string };
  return data.url;
}
