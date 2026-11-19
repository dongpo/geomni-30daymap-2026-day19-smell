# Day19 — Senses: Smell

臺灣異味陳情：件數與占比雙圖。公開地圖：https://dongpo.github.io/geomni-30daymap-2026-day19-smell/

資料：環境部 STAT_P_134（下載2026-11-18；最新2026-09）、國土測繪中心縣市界。
來源與限制見 DATA-NOTES.txt。陳情量不是氣味濃度或污染風險，比例分母是全部公害陳情；不含個案位置。

手機直向上下排列，寬螢幕並排；年月與縣市同步。前10名依地理位置排列，數字為實際排名。

## 重現
安裝 requirements.txt 後執行 `python3 scripts/build.py`。index.html 內嵌資料，可直接開啟，不依賴外部JavaScript套件。

來源資料依政府資料開放授權條款第1版：https://data.gov.tw/license 。原始資料及處理程式保留。
