import fs from "node:fs";
import path from "node:path";
import { describe, expect, it } from "vitest";

const LITTLE_SISTER_BITCH_AFO_MD5 = "55252fa3daaeb2dff8cfc3204c647fdf";

describe("FORCE RATE chart constant data", () => {
  it("keeps same-title charts assigned by MD5", () => {
    const dataPath = path.resolve(process.cwd(), "data", "force-constant-table.json");
    const charts = JSON.parse(fs.readFileSync(dataPath, "utf8"));
    const chart = charts.find((entry: { md5?: string }) => entry.md5 === LITTLE_SISTER_BITCH_AFO_MD5);

    expect(chart).toBeDefined();
    expect(chart.source_level).toBe("★10");
    expect(chart.level).toBe("10");
    expect(chart.constant).toBe("10.23");
  });
});
