# Focus Extractor

Backend service for generating `.xlsx` spreadsheets from the Central Bank of Brazil's **Focus** PDF report.

Used by the frontend project: [Focus Site](https://github.com/giovannacbs/Focus-Site)

## ✅ What it does

- Downloads the Focus PDF for a given Friday
- Extracts the forecast table
- Converts the table to Excel (`.xlsx`)
- Returns the file via API

## 📎 API

### `GET /get-excel?date=YYYYMMDD`

- `date` must be a **Friday**
- Returns an Excel file with the extracted table
- Example:  
  `https://focus-project-ix6q.onrender.com/get-excel?date=20240705`

## ⚠️ Notes

- Only supports **Fridays** from **2022 onward**
- PDFs are fetched directly from:  
  `https://www.bcb.gov.br/content/focus/focus/R{date}.pdf`

## 📤 Deployed at

`https://focus-project-ix6q.onrender.com`

