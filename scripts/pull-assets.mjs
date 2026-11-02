#!/usr/bin/env node
// One-time helper: downloads the images and CircularStd fonts from the current
// WordPress site into /assets, using the map in scripts/assets.json.
// Run from the repo root:  node scripts/pull-assets.mjs
// Requires Node 18+. Skips files that already exist (use --force to re-download).
import { readFile, writeFile, mkdir, access } from "node:fs/promises";
import { dirname } from "node:path";

const force = process.argv.includes("--force");
const map = JSON.parse(await readFile(new URL("./assets.json", import.meta.url), "utf8"));
let ok = 0, skipped = 0, failed = [];

for (const [local, remote] of Object.entries(map)) {
  if (!force) {
    try { await access(local); skipped++; continue; } catch {}
  }
  try {
    const res = await fetch(encodeURI(remote));
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    await mkdir(dirname(local), { recursive: true });
    await writeFile(local, Buffer.from(await res.arrayBuffer()));
    ok++;
    console.log("✓", local);
  } catch (err) {
    failed.push(`${local}  ←  ${remote}  (${err.message})`);
    console.log("✗", local, err.message);
  }
}

console.log(`\nDownloaded ${ok}, skipped ${skipped}, failed ${failed.length}.`);
if (failed.length) {
  console.log("\nFailed files (download these manually):\n" + failed.join("\n"));
  process.exitCode = 1;
}
