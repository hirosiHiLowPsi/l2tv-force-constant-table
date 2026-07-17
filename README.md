# L2TV FORCE RATE 譜面定数表

L2TV FORCE RATEの譜面定数を、`L1`から`L27`までのBMSTable互換難易度表として公開するプロジェクトです。

## レベル区分

- `L1`: 定数1.00〜1.99
- `L2`: 定数2.00〜2.99
- 同様に整数部分で分類
- `L27`: 定数27.00

## 対象

- 発狂BMS難易度表
- 初代Overjoy
- 第二期Overjoy

同じMD5の譜面は1譜面として扱います。曲名、アーティスト、本体URL、差分URLはLR2IR Archiveの譜面メタデータを利用します。

## データ生成

```powershell
python scripts/generate-force-constant-bmstable.py `
  --constants ../l2tv-tauri2/public/data/force-chart-constants.json `
  --archive-db C:/path/to/lr2ir-archive.db `
  --output data/force-constant-table.json
```

## 開発

```powershell
npm install
npm run dev
```

BMSTableヘッダーは`/header.json`、譜面データは`/data.json`から取得できます。

## 出典・ライセンス

- 表示基盤: [meta-BE/bms-diff-table-template](https://github.com/meta-BE/bms-diff-table-template) (MIT)
- 譜面統計・メタデータ: LR2IR Archive
- L2TV FORCE RATE制作: HiLowPsi

テンプレート由来のコードはMIT Licenseに従います。
