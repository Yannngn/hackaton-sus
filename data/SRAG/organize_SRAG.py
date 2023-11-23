import pandas as pd

# COLUMNS_TYPES = {
#     "racaCor": str,
#     "sexo": str,
#     "estado": str,
#     "municipio": str,
#     "origem": str,
#     "estadoNotificacao": str,
#     "municipioNotificacao": str,
#     "evolucaoCaso": str,
#     "classificacaoFinal": str,
#     "codigoEstrategiaCovid": int,
#     "codigoBuscaAtivaAssintomatico",
#     "outroBuscaAtivaAssintomatico",
#     "codigoTriagemPopulacaoEspecifica",
#     "outroTriagemPopulacaoEspecifica",
#     "codigoLocalRealizacaoTestagem",
#     "outroLocalRealizacaoTestagem",
#     "codigoRecebeuVacina",
#     "codigoLaboratorioPrimeiraDose",
#     "codigoLaboratorioSegundaDose",
#     "lotePrimeiraDose",
#     "loteSegundaDose",
#     "codigoContemComunidadeTradicional",
#     "source_id",
#     "excluido",
#     "validado",
#     "codigoDosesVacina",
#     "estadoNotificacaoIBGE",
#     "totalTestesRealizados",
#     "dataNotificacao",
#     "dataInicioSintomas",
#     "dataEncerramento",
#     "dataPrimeiraDose",
#     "dataSegundaDose",
#     "codigoEstadoTeste1",
#     "codigoTipoTeste1",
#     "codigoFabricanteTeste1",
#     "codigoResultadoTeste1",
#     "codigoEstadoTeste2",
#     "codigoTipoTeste2",
#     "codigoFabricanteTeste2",
#     "codigoResultadoTeste2",
#     "codigoEstadoTeste3",
#     "codigoTipoTeste3",
#     "codigoFabricanteTeste3",
#     "codigoResultadoTeste3",
#     "codigoEstadoTeste4",
#     "codigoTipoTeste4",
#     "codigoFabricanteTeste4",
#     "codigoResultadoTeste4",
#     "dataColetaTeste1",
#     "dataColetaTeste2",
#     "dataColetaTeste3",
#     "dataColetaTeste4",
#     "idade",
# }


def preprocess():
    df = pd.DataFrame()
    for y in [0, 1, 2]:
        y_df = pd.DataFrame()
        for p in [0, 1]:
            cols = list(pd.read_csv(f"data/SRAG/SRAG_202{y}_{p}.csv", sep=";", nrows=1))
            usecols = [
                c
                for c in cols
                if c not in ["sintomas", "outrosSintomas", "outrasCondicoes"]
            ]
            p_df = pd.read_csv(
                f"data/SRAG/SRAG_202{y}_{p}.csv",
                sep=";",
                low_memory=False,
                usecols=usecols,
            )
            y_df = pd.concat([y_df, p_df], ignore_index=True)

        df = pd.concat([df, y_df], ignore_index=True)

    df.columns = df.columns.str.replace(" - ", "_")
    df.columns = df.columns.str.replace(" ", "_")

    df["CNES"] = df["CNES"].astype(int).astype(str).str.zfill(7)

    for column in df.columns:
        if column not in COLUMNS_TYPES.keys():
            df = df.drop(columns=[column])

    for column, t in COLUMNS_TYPES.items():
        if t == int:
            df[column] = df[column].fillna(0)
            df[column] = df[column].astype(t)

    df.to_csv("data/leitos/Leitos.csv", index=False)


def main():
    preprocess()


if __name__ == "__main__":
    main()
