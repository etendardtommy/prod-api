const BASE = "/api";

export function getSiteId(): string {
  return localStorage.getItem("admin_site_id") || "1";
}

export function setSiteId(id: string) {
  localStorage.setItem("admin_site_id", id);
}

function authHeaders(): Record<string, string> {
  return {
    "x-site-id": getSiteId(),
    "Content-Type": "application/json",
  };
}

function checkAuth(status: number) {
  if (status === 401) {
    window.location.href = "/admin/login";
  }
}

export async function get<T>(path: string): Promise<T> {
  const r = await fetch(BASE + path, { headers: authHeaders(), credentials: "include" });
  checkAuth(r.status);
  if (!r.ok) throw new Error(await r.text());
  return r.json() as Promise<T>;
}

export async function post<T>(path: string, body: unknown): Promise<T> {
  const r = await fetch(BASE + path, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify(body),
    credentials: "include",
  });
  if (!r.ok) throw new Error(await r.text());
  return r.json() as Promise<T>;
}

export async function put<T>(path: string, body: unknown): Promise<T> {
  const r = await fetch(BASE + path, {
    method: "PUT",
    headers: authHeaders(),
    body: JSON.stringify(body),
    credentials: "include",
  });
  if (!r.ok) throw new Error(await r.text());
  return r.json() as Promise<T>;
}

export async function del(path: string): Promise<void> {
  await fetch(BASE + path, { method: "DELETE", headers: authHeaders(), credentials: "include" });
}

export async function uploadSynthesis(file: File): Promise<void> {
  const form = new FormData();
  form.append("file", file);
  const r = await fetch(BASE + "/synthesis/upload", {
    method: "POST",
    headers: { "x-site-id": getSiteId() },
    body: form,
    credentials: "include",
  });
  if (!r.ok) throw new Error(await r.text());
}

export async function uploadCV(file: File): Promise<void> {
  const form = new FormData();
  form.append("file", file);
  const r = await fetch(BASE + "/cv/upload", {
    method: "POST",
    headers: { "x-site-id": getSiteId() },
    body: form,
    credentials: "include",
  });
  if (!r.ok) throw new Error(await r.text());
}

export async function uploadImage(file: File): Promise<string> {
  const form = new FormData();
  form.append("file", file);
  const r = await fetch(BASE + "/upload/", {
    method: "POST",
    headers: { "x-site-id": getSiteId() },
    body: form,
    credentials: "include",
  });
  if (!r.ok) throw new Error(await r.text());
  const data = await r.json() as { url: string };
  return data.url;
}
