import streamlit as st
import pandas as pd
import io

# ── Configuração da página ──────────────────────────────────────────────────
st.set_page_config(page_title="Limpeza de Leads", page_icon="🧹", layout="wide")

st.title("🧹 Tratamento de Arquivos dos Leads")
st.markdown("Faça upload do arquivo bruto (Excel ou CSV), aplique os filtros e exporte o resultado limpo.")

# ── Colunas de interesse ────────────────────────────────────────────────────
COLUNAS_INTERESSE = ["Id", "Nome", "E-mail", "Telefone", "Último Empreendimento", "Última Origem"]

ORIGENS_BLOQUEADAS = ["Painel Corretor", "Painel Imobiliária", "Painel Gestor"]

# ── Upload ──────────────────────────────────────────────────────────────────
uploaded_file = st.file_uploader("📂 Upload do arquivo bruto", type=["xlsx", "xls", "csv"])

if uploaded_file is not None:
    # Leitura do arquivo
    with st.spinner("Lendo arquivo..."):
        try:
            if uploaded_file.name.endswith(".csv"):
                # Tenta detectar separador e lidar com campos inconsistentes
                raw_bytes = uploaded_file.read()

                # Tenta diferentes encodings
                for encoding in ["utf-8-sig", "utf-8", "latin-1", "cp1252"]:
                    try:
                        content = raw_bytes.decode(encoding)
                        break
                    except UnicodeDecodeError:
                        continue

                # Detecta separador (vírgula ou ponto-e-vírgula)
                primeira_linha = content.split("\n")[0]
                separador = ";" if primeira_linha.count(";") > primeira_linha.count(",") else ","

                df_raw = pd.read_csv(
                    io.StringIO(content),
                    dtype=str,
                    sep=separador,
                    on_bad_lines="skip",   # pula linhas com campos a mais
                    engine="python",
                    quoting=0,             # respeita aspas para campos com vírgula interna
                )
            else:
                df_raw = pd.read_excel(uploaded_file, dtype=str)
        except Exception as e:
            st.error(f"Erro ao ler o arquivo: {e}")
            st.stop()

    st.success(f"Arquivo carregado: **{uploaded_file.name}** — {len(df_raw):,} linhas | {len(df_raw.columns)} colunas")

    # ── Preview do bruto ────────────────────────────────────────────────────
    with st.expander("👁️ Prévia do arquivo bruto (primeiras 5 linhas)"):
        st.dataframe(df_raw.head(), width="stretch")

    # ── Verificar colunas faltantes ─────────────────────────────────────────
    colunas_faltando = [c for c in COLUNAS_INTERESSE if c not in df_raw.columns]
    if colunas_faltando:
        st.warning(f"⚠️ Colunas não encontradas no arquivo: {colunas_faltando}")

    # ── Limpeza ─────────────────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("⚙️ Limpeza e Tratamento")

    df = df_raw.copy()

    # 1. Manter apenas colunas de interesse (que existem no df)
    colunas_presentes = [c for c in COLUNAS_INTERESSE if c in df.columns]
    df = df[colunas_presentes]

    # 2. Remover linhas com Última Origem bloqueada
    if "Última Origem" in df.columns:
        antes = len(df)
        df = df[~df["Última Origem"].isin(ORIGENS_BLOQUEADAS)]
        removidas_origem = antes - len(df)
    else:
        removidas_origem = 0

    # 3. Limpar campo Telefone: remover + e aspas
    if "Telefone" in df.columns:
        df["Telefone"] = (
            df["Telefone"]
            .astype(str)
            .str.replace("+", "", regex=False)
            .str.replace("'", "", regex=False)
            .str.replace('"', "", regex=False)
            .str.strip()
        )
        # Tratar NaN/nan que virou string
        df["Telefone"] = df["Telefone"].replace("nan", "")

    col1, col2, col3 = st.columns(3)
    col1.metric("Linhas originais", f"{len(df_raw):,}")
    col2.metric("Removidas (Painel)", f"{removidas_origem:,}")
    col3.metric("Linhas após limpeza", f"{len(df):,}")

    # ── Filtro por Empreendimento ───────────────────────────────────────────
    st.markdown("---")
    st.subheader("🏢 Filtro por Empreendimento")

    if "Último Empreendimento" in df.columns:
        empreendimentos_disponiveis = sorted(
            df["Último Empreendimento"].dropna().unique().tolist()
        )

        empreendimentos_selecionados = st.multiselect(
            "Selecione os empreendimentos de interesse (deixe vazio para manter todos):",
            options=empreendimentos_disponiveis,
            default=[],
        )

        if empreendimentos_selecionados:
            df_filtrado = df[df["Último Empreendimento"].isin(empreendimentos_selecionados)]
        else:
            df_filtrado = df.copy()

        st.info(f"📊 Registros após filtro de empreendimento: **{len(df_filtrado):,}**")
    else:
        df_filtrado = df.copy()
        st.warning("Coluna 'Último Empreendimento' não encontrada.")

    # ── Preview do resultado ────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("📋 Resultado Final")
    st.dataframe(df_filtrado, width="stretch", height=400)

    # ── Exportação ──────────────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("📥 Exportar Arquivo Tratado")

    col_xlsx, col_csv = st.columns(2)

    # Excel
    with col_xlsx:
        buffer_xlsx = io.BytesIO()
        with pd.ExcelWriter(buffer_xlsx, engine="openpyxl") as writer:
            df_filtrado.to_excel(writer, index=False, sheet_name="Leads Tratados")
        buffer_xlsx.seek(0)
        st.download_button(
            label="⬇️ Baixar Excel (.xlsx)",
            data=buffer_xlsx,
            file_name="leads_tratados.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            width="stretch",
        )

    # CSV
    with col_csv:
        csv_data = df_filtrado.to_csv(index=False, encoding="utf-8-sig")
        st.download_button(
            label="⬇️ Baixar CSV (.csv)",
            data=csv_data,
            file_name="leads_tratados.csv",
            mime="text/csv",
            width="stretch",
        )

else:
    st.info("👆 Faça upload de um arquivo Excel ou CSV para começar.")

    # Mostrar as regras aplicadas
    with st.expander("📖 Regras de limpeza aplicadas"):
        st.markdown("""
        **1. Limpeza do Telefone**  
        Remove o `+` e aspas do campo Telefone. Ex: `+5586999553232` → `5586999553232`

        **2. Remoção por Última Origem**  
        Remove todas as linhas onde `Última Origem` for:
        - Painel Corretor
        - Painel Imobiliária  
        - Painel Gestor

        **3. Colunas de interesse**  
        Mantém apenas: `Id`, `Nome`, `E-mail`, `Telefone`, `Último Empreendimento`, `Última Origem`

        **4. Filtro por Empreendimento**  
        Permite selecionar apenas os empreendimentos desejados da coluna `Último Empreendimento`

        **5. Exportação**  
        Disponibiliza download em `.xlsx` e `.csv`
        """)