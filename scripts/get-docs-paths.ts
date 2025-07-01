import { resolve } from "node:path";
import { readdirSync } from "node:fs";

export function getDocSlugs() {
  const docsDir = resolve(process.cwd(), "EIPS");
  const files = readdirSync(docsDir, { recursive: true });
  
  return files
    .filter((file) => typeof file === "string" && file.endsWith(".md"))
    .map((file) => {
      const path = file
        .replace(/\.md$/, "")
        .split("/")
        .filter((p) => p !== "index");
      
      return { slug: path };
    });
} 