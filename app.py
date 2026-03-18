import json

import streamlit as st

from seo_auditor import SeoAuditService, report_to_csv


st.set_page_config(page_title="SEO Checklist Auditor", page_icon="🔎", layout="wide")

st.title("SEO Checklist Auditor")
st.write("Ingresa la URL y genera un reporte automatico alineado al checklist SEO tecnico.")

url = st.text_input("URL del sitio", placeholder="https://www.ejemplo.com")
run = st.button("Analizar", type="primary")

if run:
    if not url.strip():
        st.error("Ingresa una URL valida.")
    else:
        checker = SeoAuditService()
        try:
            with st.spinner("Analizando reglas SEO..."):
                report = checker.analyze(url)
        except Exception as exc:
            st.error(f"No se pudo completar el analisis: {exc}")
        else:
            summary = report["summary"]
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("PASS", summary.get("PASS", 0))
            col2.metric("FAIL", summary.get("FAIL", 0))
            col3.metric("WARN", summary.get("WARN", 0))
            col4.metric("MANUAL", summary.get("MANUAL", 0))

            st.caption(f"URL final evaluada: {report['final_url']}")
            st.dataframe(report["results"], use_container_width=True, hide_index=True)

            csv_data = report_to_csv(report["results"])
            json_data = json.dumps(report, ensure_ascii=False, indent=2)

            d1, d2 = st.columns(2)
            d1.download_button(
                "Descargar CSV",
                data=csv_data,
                file_name="reporte_seo.csv",
                mime="text/csv",
            )
            d2.download_button(
                "Descargar JSON",
                data=json_data,
                file_name="reporte_seo.json",
                mime="application/json",
            )
