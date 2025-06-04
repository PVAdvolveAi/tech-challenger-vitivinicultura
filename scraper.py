import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
from io import StringIO


def encontrar_link_csv(base_url: str) -> str | None:
    """
    Busca, em base_url, o primeiro <a href="..."> que termine em '.csv' e devolve a URL absoluta.
    Se não encontrar, retorna None.
    """
    resp = requests.get(base_url)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'html.parser')

    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.lower().endswith('.csv'):
            return urljoin(base_url, href)
    return None


def detectar_separador_e_carregar(texto: str) -> pd.DataFrame:
    """
    Recebe o conteúdo bruto do CSV como string e detecta se há '\t' na(s) primeira(s) linha(s).
    Se houver '\t', usa sep='\t'; elif houver ';', usa sep=';'; senão usa sep=','.
    """
    sniff = texto[:2048]
    if '\t' in sniff:
        sep = '\t'
    elif ';' in sniff:
        sep = ';'
    else:
        sep = ','

    df = pd.read_csv(StringIO(texto), sep=sep,
                     encoding='utf-8', low_memory=False)
    return df


def carregar_aba_por_csv(opcao: int) -> pd.DataFrame:
    """
    1) Monta a URL com duas casas (opt_02, opt_03, ..., opt_06).
    2) Encontra o link .csv dentro daquele HTML.
    3) Baixa e lê o CSV, detectando automaticamente separador.
    4) Remove 'id' e 'control' (se existirem), “derrete” anos em linhas e converte tipos.
    Retorna um DataFrame com colunas ['categoria', 'ano', 'valor'].
    """
    base_url = f'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_{opcao:02d}'
    print(f"\n— Buscando link CSV em: {base_url}")

    link_csv = encontrar_link_csv(base_url)
    if not link_csv:
        raise ValueError(
            f"Não encontrei link CSV para opt_{opcao:02d} em {base_url}")

    print(f"→ Link CSV encontrado para opt_{opcao:02d}: {link_csv}")

    resp_csv = requests.get(link_csv)
    resp_csv.raise_for_status()
    try:
        texto = resp_csv.content.decode('utf-8')
    except UnicodeDecodeError:
        texto = resp_csv.content.decode('latin1')

    # 1) Baixa o DataFrame “raw”
    df_raw = detectar_separador_e_carregar(texto)

    # 2) Remove colunas “id” e “control” (erros='ignore' caso não existam)
    df = df_raw.drop(columns=['id', 'control'], errors='ignore')

    # 3) Identifica colunas de anos (nomes que são dígitos sem ponto)
    colunas_anos = [c for c in df.columns if c.isdigit()]

    # 4) Define qual coluna é a “categoria” (depende da aba opt_02..opt_06)
    if opcao == 2:
        id_col = 'produto'
    elif opcao == 3:
        id_col = 'cultivar'
    elif opcao == 4:
        id_col = 'Produto'
    else:  # 5 ou 6
        id_col = 'País'

    # 5) “Derrete” (melt) anos em linhas
    df_long = df.melt(
        id_vars=[id_col],
        value_vars=colunas_anos,
        var_name='ano',
        value_name='quantidade'
    )

    # 6) Converter “ano” para int
    df_long['ano'] = df_long['ano'].astype(int)

    # 7) Converter “quantidade” para numérico:
    #    - substitui vírgula decimal por ponto
    #    - troca “nd” e “*” por NaN
    #    - converte para float e preenche NaN com 0
    df_long['quantidade'] = (
        df_long['quantidade']
        .astype(str)
        .str.replace(',', '.', regex=False)
        .replace({'nd': pd.NA, '*': pd.NA})
    )
    df_long['quantidade'] = pd.to_numeric(
        df_long['quantidade'], errors='coerce').fillna(0)

    # 8) Padroniza valores na coluna de categoria:
    #    - remove prefixos “vm_” e “ti_”
    #    - tira espaços extras e coloca em caixa alta
    df_long[id_col] = (
        df_long[id_col]
        .astype(str)
        .str.replace(r'^(vm_|ti_)', '', regex=True)
        .str.strip()
        .str.upper()
    )

    # 9) Renomeia colunas para ['categoria', 'ano', 'valor']
    df_long = df_long.rename(
        columns={id_col: 'categoria', 'quantidade': 'valor'})
    return df_long


if __name__ == "__main__":
    for opcao in range(2, 7):
        try:
            df = carregar_aba_por_csv(opcao)
            print(f"\n→ opt_{opcao:02d} (primeiras linhas):")
            print(df.head(), "\n")
        except Exception as e:
            print(f"Erro ao carregar opt_{opcao:02d}:", e)
