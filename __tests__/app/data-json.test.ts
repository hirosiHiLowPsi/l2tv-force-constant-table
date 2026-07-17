import { describe, it, expect, vi, beforeEach } from "vitest";
import { fetchTableData } from "@/lib/fetch-table-data";

vi.mock("@/lib/fetch-table-data", () => ({
  fetchTableData: vi.fn(),
}));

const fetchTableDataMock = vi.mocked(fetchTableData);

describe("GET /data.json", () => {
  beforeEach(() => {
    fetchTableDataMock.mockReset();
  });

  it("fetchTableDataの結果をJSONレスポンスとして返す", async () => {
    const mockData = [
      { md5: "abc123", level: "1", title: "Song", artist: "Artist" },
    ];

    fetchTableDataMock.mockResolvedValue(mockData);

    const { GET } = await import("@/app/data.json/route");
    const response = await GET();
    const body = await response.json();

    expect(response.status).toBe(200);
    expect(response.headers.get("Content-Type")).toBe("application/json; charset=utf-8");
    expect(body).toEqual(mockData);
  });

  it("fetch失敗時に502を返す", async () => {
    fetchTableDataMock.mockRejectedValue(new Error("Internal Server Error"));

    const { GET } = await import("@/app/data.json/route");
    const response = await GET();

    expect(response.status).toBe(502);
  });
});
