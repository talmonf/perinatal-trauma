const fs = require("fs");
const html = fs.readFileSync("index.html", "utf8");
const root = new URL("http://127.0.0.1:8910/");
const re = /(\s(?:href|src)=)("|')(?![a-zA-Z][a-zA-Z0-9+.-]*:|\/\/|#)([^"']*)\2/g;
const out = html.replace(re, function (_, attr, quote, url) {
  return attr + quote + new URL(url, root).href + quote;
});
const orig = [...html.matchAll(/(?:href|src)="([^"]*)"/g)].map((m) => m[1]);
const next = [...out.matchAll(/(?:href|src)="([^"]*)"/g)].map((m) => m[1]);
orig.forEach((u, i) => {
  if (u !== next[i]) console.log(u, "=>", next[i]);
});
console.log("counts", orig.length, next.length);
