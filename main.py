from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
import pandas as pd
import io
from natural_pdf import PDF 
import numpy as np

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou use ['https://seuusuario.github.io'] se quiser restringir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def focus(date):
    url = f'https://www.bcb.gov.br/content/focus/focus/R{date}.pdf'
    pdf = PDF(url)
    page = pdf.pages[0]

    df = page.find('text:contains("IPCA")').below(
        until='text:contains(comportamento)',
        include_endpoint=False,
        include_source=True
    ).extract_table().to_df()

    df.replace(["None", "none", "NaN", "nan", ""], np.nan, inplace=True)
    df.dropna(how="all", inplace=True)

    df['year'] = df.iloc[:, 3]
    df['year+1'] = df.iloc[:, 11]
    df['year+2'] = df.iloc[:, 19]
    df['year+3'] = df.iloc[:, 25]

    df.set_index(df.columns[0], inplace=True)
    df_focus = df[['year', 'year+1', 'year+2', 'year+3']]
    df_focus = df_focus.applymap(lambda x: pd.to_numeric(str(x).replace(",", "."), errors='coerce'))

    filter_list = [
        'IPCA (variação %)', 
        'PIB Total (variação % sobre ano anterior)', 
        'Câmbio (R$/US$)', 
        'Selic (% a.a)', 
        'Conta corrente (US$ bilhões)', 
        'Balança comercial (US$ bilhões)', 
        'Investimento direto no país (US$ bilhões)'
    ]

    df_focus = df_focus[df_focus.index.isin(filter_list)]
    return df_focus

@app.get("/get-excel")
def get_excel(date: str = Query(...)):
    df = focus(date)
    buffer = io.BytesIO()
    df.to_excel(buffer, index=True)
    buffer.seek(0)
    
    filename = f"R{date}.xlsx"
    return StreamingResponse(buffer, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                             headers={'Content-Disposition': f'attachment; filename="{filename}"'})
