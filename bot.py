import os, base64, hashlib, secrets
from pathlib import Path
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
OWNER_NAME = "𝐃𝐄𝐕𝐋𝐎𝐏𝐄𝐑 𝐅𝐈𝐀𝐂𝐁 𝐁𝐃"
OWNER_USERNAME = "@DEVLOPER_FIACB_BD"

if not BOT_TOKEN:
    raise RuntimeError("Set BOT_TOKEN environment variable first.")

def build_protected_html(source: str) -> str:
    raw = source.encode("utf-8")
    payload = base64.b64encode(raw).decode("ascii")
    salt = secrets.token_hex(16)
    digest = hashlib.sha256(raw + salt.encode()).hexdigest()
    chunks = [payload[i:i+180] for i in range(0, len(payload), 180)]
    js_chunks = ",\n".join(repr(x) for x in chunks)

    template = r'''<!--
╔══════════════════════════════════════════════════════════════╗
║  🔒 𝐃𝐄𝐕𝐋𝐎𝐏𝐄𝐑 𝐅𝐈𝐀𝐂𝐁 𝐁𝐃 — FIACB HTML PROTECTOR            ║
║  Telegram: @DEVLOPER_FIACB_BD                               ║
║  Security: runtime decode + tamper checks + obfuscation     ║
╚══════════════════════════════════════════════════════════════╝
-->
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>𝐃𝐄𝐕𝐋𝐎𝐏𝐄𝐑 𝐅𝐈𝐀𝐂𝐁 𝐁𝐃</title>
<style>html,body{margin:0;min-height:100%;}body{-webkit-user-select:none;user-select:none;}</style>
<script>
(()=> {
"use strict";
const BRAND="𝐃𝐄𝐕𝐋𝐎𝐏𝐄𝐑 𝐅𝐈𝐀𝐂𝐁 𝐁𝐃";
const OWNER="@DEVLOPER_FIACB_BD";
const HASH="__HASH__";
const parts=[__PARTS__];

function fail(){
  document.documentElement.innerHTML =
    '<body style="background:#111;color:#f33;font:700 18px sans-serif;text-align:center;padding-top:18vh">'+
    '⚠️ Protected source access blocked<br><small>'+BRAND+' • '+OWNER+'</small></body>';
}

window.addEventListener("contextmenu",e=>e.preventDefault(),true);
window.addEventListener("keydown",e=>{
  const k=(e.key||"").toLowerCase();
  if(e.key==="F12" || (e.ctrlKey&&["u","s"].includes(k)) ||
     (e.ctrlKey&&e.shiftKey&&["i","j","c","k"].includes(k))){
    e.preventDefault(); e.stopPropagation(); fail(); return false;
  }
},true);

let t0=performance.now();
try{
  if(performance.now()-t0>650) throw new Error("debugger");
  const bin=atob(parts.join(""));
  const bytes=Uint8Array.from(bin,c=>c.charCodeAt(0));
  const html=new TextDecoder().decode(bytes);
  const marker=document.createComment(BRAND+" "+OWNER+" "+HASH);
  document.head.appendChild(marker);
  document.open(); document.write(html); document.close();
  bytes.fill(0);
}catch(e){ fail(); }
})();
</script>
</head>
<body>
<noscript><h2 style="text-align:center;margin-top:20vh">JavaScript must be enabled.</h2></noscript>
</body>
</html>
'''
    return template.replace("__HASH__", digest).replace("__PARTS__", js_chunks)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔐 𝐃𝐄𝐕𝐋𝐎𝐏𝐄𝐑 𝐅𝐈𝐀𝐂𝐁 𝐁𝐃\n\n"
        "Send an .html file to protect/obfuscate it.\n"
        "👤 @DEVLOPER_FIACB_BD"
    )

async def protect_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    doc = update.message.document
    name = doc.file_name or "index.html"
    if not name.lower().endswith((".html", ".htm")):
        await update.message.reply_text("❌ Please send an HTML file.")
        return
    tg_file = await doc.get_file()
    data = await tg_file.download_as_bytearray()
    source = bytes(data).decode("utf-8", errors="replace")
    protected = build_protected_html(source)
    out = Path("/tmp") / f"PROTECTED_{Path(name).stem}.html"
    out.write_text(protected, encoding="utf-8")
    with out.open("rb") as f:
        await update.message.reply_document(
            document=f,
            caption="✅ Protected by 𝐃𝐄𝐕𝐋𝐎𝐏𝐄𝐑 𝐅𝐈𝐀𝐂𝐁 𝐁𝐃\n👤 @DEVLOPER_FIACB_BD"
        )
    out.unlink(missing_ok=True)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL, protect_file))
    app.run_polling()

if __name__ == "__main__":
    main()
