// Cloudflare Pages Function: POST /api/contact
// Guarda el mensaje en KV (binding CONTACTS) y/o lo envía por correo con Resend (secreto RESEND_API_KEY).
// Si no hay ninguno configurado responde 503 y el sitio ofrece el correo directo.
const TO = "cpitta@yahoo.com";

export async function onRequestPost({ request, env }) {
  let d;
  try { d = await request.json(); } catch { return json({ error: "bad_json" }, 400); }
  const s = (v, n) => String(v ?? "").trim().slice(0, n);
  const msg = {
    name: s(d.name, 120), email: s(d.email, 160), org: s(d.org, 160),
    kind: s(d.kind, 80), message: s(d.message, 5000), lang: s(d.lang, 5),
    at: new Date().toISOString(), ip: request.headers.get("CF-Connecting-IP") || "",
    country: request.cf?.country || "",
  };
  // trampas para bots: campo oculto lleno o envío demasiado rápido
  if (s(d.website, 200) || Number(d.elapsed) < 2500) return json({ ok: true });
  if (!msg.name || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(msg.email) || !msg.message || d.consent !== "yes")
    return json({ error: "invalid" }, 422);

  let stored = false, mailed = false;
  if (env.CONTACTS) {
    await env.CONTACTS.put(`msg:${msg.at}:${crypto.randomUUID().slice(0, 8)}`, JSON.stringify(msg));
    stored = true;
  }
  if (env.RESEND_API_KEY) {
    const r = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, "Content-Type": "application/json" },
      body: JSON.stringify({
        from: env.MAIL_FROM || "carlospitta.com <onboarding@resend.dev>",
        to: [env.MAIL_TO || TO], reply_to: msg.email,
        subject: `[carlospitta.com] ${msg.kind}: ${msg.name}`,
        text: `${msg.name} <${msg.email}>\n${msg.org}\n${msg.kind}\n\n${msg.message}\n\n— ${msg.at} ${msg.country}`,
      }),
    });
    mailed = r.ok;
    if (!r.ok) console.log("resend", r.status, await r.text());
  }
  if (!stored && !mailed) return json({ error: "not_configured" }, 503);
  return json({ ok: true, stored, mailed });
}

export const onRequest = () => json({ error: "method" }, 405);

function json(o, status = 200) {
  return new Response(JSON.stringify(o), { status, headers: { "Content-Type": "application/json" } });
}
