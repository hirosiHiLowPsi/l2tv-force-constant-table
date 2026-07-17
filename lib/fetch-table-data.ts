import { config } from "./config";
import fs from "fs/promises";
import path from "path";

export interface TableEntry {
  md5: string;
  level: string;
  [key: string]: unknown;
}

export async function fetchTableData(
  url: string = config.dataUrl
): Promise<TableEntry[]> {
  if (url.startsWith("local:")) {
    const relativePath = url.slice("local:".length);
    const filePath = path.resolve(process.cwd(), relativePath);
    const root = `${process.cwd()}${path.sep}`;

    if (!filePath.startsWith(root)) {
      throw new Error("ローカルデータのパスが不正です");
    }

    return JSON.parse(await fs.readFile(filePath, "utf-8")) as TableEntry[];
  }

  const res = await fetch(url, {
    redirect: "follow",
    next: { revalidate: 300 },
  });

  if (!res.ok) {
    throw new Error(
      `データの取得に失敗しました: ${res.status} ${res.statusText}`
    );
  }

  return res.json();
}
