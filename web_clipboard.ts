# 网络剪贴板
# Deno 代码，可使用 Deno 或 Deno Deploy 运行
import { serve } from "https://deno.land/std@0.150.0/http/server.ts";
const kv = await Deno.openKv();
let txt=""
const handler = async (req: Request): Promise<Response> => {
  if (new URL(req.url).hostname.endsWith(".deno.dev")) {
    return new Response("404 Not Found", {status: 404,});
  }
  if (req.method === 'POST') {
    const formData = await req.formData();
    const txt = formData.get('txt') as string;
    await kv.set(["TEXT"], txt);
    return new Response(`<meta http-equiv="refresh" content="0">`,{headers: {"Content-Type": "text/html"},});
  } else {
    try {
      txt = (await kv.get(["TEXT"])).value as string;
      txt=txt.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }catch(_){
      txt="暂无数据"
    }
    return new Response(
        `<!DOCTYPE html><html lang="zh-cn">
  <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <link rel="icon" type="image/svg+xml" href='data:image/svg+xml,%3C?xml version=%221.0%22 encoding=%22UTF-8%22?%3E%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%22144%22 height=%22144%22 viewBox=%220 0 144 144%22%3E%3Cdefs%3E%3Cstyle%3E:root {--stroke-color: %23000;}@media (prefers-color-scheme: dark) {:root {--stroke-color: %23fff;}}.st0, .st1 {fill: none;stroke: var(--stroke-color);stroke-linecap: round;stroke-miterlimit: 10;}.st0, .st2 {stroke-width: 5px;}.st1 {stroke-width: 5px;}.st2 {stroke: var(--stroke-color);fill: var(--stroke-color);}%3C/style%3E%3C/defs%3E%3Cg%3E%3Cpath class=%22st0%22 d=%22M56.96,30.24c-2.3,0-4.16-1.86-4.16-4.16s1.86-4.16,4.16-4.16%22/%3E%3Cpath class=%22st0%22 d=%22M87.04,21.92c2.3,0,4.16,1.86,4.16,4.16s-1.86,4.16-4.16,4.16%22/%3E%3Cline class=%22st0%22 x1=%2256.96%22 y1=%2221.92%22 x2=%2287.04%22 y2=%2221.92%22/%3E%3Cline class=%22st0%22 x1=%2256.96%22 y1=%2230.24%22 x2=%2287.04%22 y2=%2230.24%22/%3E%3C/g%3E%3Cline class=%22st0%22 x1=%2252.8%22 y1=%2226.08%22 x2=%2238.39%22 y2=%2225.97%22/%3E%3Cline class=%22st0%22 x1=%2234.39%22 y1=%22117.08%22 x2=%2234.39%22 y2=%2229.97%22/%3E%3Cline class=%22st0%22 x1=%2291.2%22 y1=%2226.08%22 x2=%22105.72%22 y2=%2225.97%22/%3E%3Cline class=%22st0%22 x1=%22109.72%22 y1=%22117.08%22 x2=%22109.72%22 y2=%2229.97%22/%3E%3Cline class=%22st0%22 x1=%2238.39%22 y1=%22121.08%22 x2=%22105.72%22 y2=%22121.08%22/%3E%3Cline class=%22st1%22 x1=%2247.42%22 y1=%2261.08%22 x2=%2282.25%22 y2=%2261.08%22/%3E%3Cline class=%22st1%22 x1=%2247.42%22 y1=%2279.08%22 x2=%2282.25%22 y2=%2279.08%22/%3E%3Cline class=%22st1%22 x1=%2247.81%22 y1=%2297.08%22 x2=%2282.64%22 y2=%2297.08%22/%3E%3Ccircle class=%22st2%22 cx=%2296.03%22 cy=%2261.08%22 r=%223.5%22/%3E%3Ccircle class=%22st2%22 cx=%2296.03%22 cy=%2279.08%22 r=%223.5%22/%3E%3Ccircle class=%22st2%22 cx=%2296.03%22 cy=%2297.08%22 r=%223.5%22/%3E%3Cpath class=%22st0%22 d=%22M105.72,25.97c2.21,0,4,1.79,4,4%22/%3E%3Cpath class=%22st0%22 d=%22M34.39,29.97c0-2.21,1.79-4,4-4%22/%3E%3Cpath class=%22st0%22 d=%22M38.39,121.08c-2.21,0-4-1.79-4-4%22/%3E%3Cpath class=%22st0%22 d=%22M109.72,117.08c0,2.21-1.79,4-4,4%22/%3E%3C/svg%3E'>
      <title>网络剪贴板</title>
      <style>
      html::before{
        content: "";
        width: 100%;
        height: 100%;
        position: fixed;
        z-index: -1;
        background-image: linear-gradient(120deg, #f0fffc 0%, #f6ffea 100%);
      }
      p {font-size:26px;word-break:break-all;margin:10px;}
      pre {font-size:26px;word-break:break-all;margin:10px;}
      textarea {font-family: inherit;font-size:16px;background-color: inherit;}
      button {font-size: 16px;}
      .btn {
        background-color: rgba(100, 100, 100, 0.3);
        border: none;
        border-radius: 8px;
      }
      #in{border-radius: 8px;}
      </style>
      <p style="font-size: 50px;">网络剪贴板</p>
  </head>
  <form method="post">
    <div style="display: flex;align-items: stretch;">
      <textarea name="txt" rows="1" oninput="resizeTextarea(this)" style="flex: 1; resize: none" id="in"></textarea>
      <input type="submit" value="提交" style="align-self: stretch;height: auto;margin-left: 4px;" class="btn">
    </div>
  </form>
  <button onclick="location.reload();" class="btn" style="margin-top: 10px">刷新</button>&emsp;<button onclick="copyText('0')" class="btn">复制</button><br><br>
  <textarea readonly style="width: 100%;resize: none;border: none; outline: none;" id='0'>
${txt}</textarea>
  <script>
      function resizeTextarea(textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = textarea.style.height = (textarea.scrollHeight) + 'px';
      }
      function copyText(id) {
          const copyText = document.getElementById(id);
          copyText.select();
          copyText.setSelectionRange(0, 99999);
          document.execCommand("copy");
      }
      resizeTextarea(textarea=document.getElementById('0'))
      resizeTextarea(textarea=document.getElementById("in"))
  </script>`,
        {
          headers: {"Content-Type": "text/html"},
        }
    );
  }
};


await serve(handler, { port: 80 });
