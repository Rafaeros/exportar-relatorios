"""This script automates the process of logging into a website,
retrieving sales data, and exporting it to an Excel file."""

import os
import requests
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup

SALES_PATH = "C:/Users/{}/Documents/VendasEmitidas_{}.xlsx"

def get_sales_data(
    username: str,
    password: str,
    start_date: str = "01/04/2025",
    end_date: str = "15/04/2025",
) -> None:
    """
    Automates the process of logging into a website using Selenium,
    retrieves sales data from a specified URL using aiohttp, and returns
    the data as a pandas DataFrame. If the data retrieval fails, returns None.

    Returns:
        None | pd.DataFrame: A DataFrame containing the sales data or None
                             if the retrieval fails.
    """
    driver = webdriver.Chrome()
    driver.get("https://app.cargamaquina.com.br/site/login?c=31.1~78%2C8%5E56%2C8")
    driver.find_element("name", "LoginForm[username]").send_keys(username)
    driver.find_element("name", "LoginForm[password]").send_keys(password)
    driver.find_element("name", "yt0").click()
    cookies = driver.get_cookies()

    data_url: str = (
        "https://app.cargamaquina.com.br/relatorio/venda/renderGridExportacaoVendasEmitidas"
    )
    params: dict = {
        "RelatorioVendasEmitidas[dataInicio]": f"{start_date}",
        "RelatorioVendasEmitidas[dataFim]": f"{end_date}",
        "RelatorioVendasEmitidas[tipoData]": "FAT",
        "RelatorioVendasEmitidas[emissorFiscalId]": "",
        "RelatorioVendasEmitidas[detalhar]": "0",
        "RelatorioVendasEmitidas[considerarCanceladas]": "0",
    }
    cookies: dict = {cookie["name"]: cookie["value"] for cookie in cookies}
    response = requests.get(data_url, params=params, cookies=cookies, timeout=15)
    if not response.ok:
        print("Error: ", response.status_code)
        return
    data: str = response.text
    soup = BeautifulSoup(data, "html.parser")
    table = soup.find("table", {"id": "tableExpo"})
    if not table:
        print("Error: Table not found")
        return None
    req_df: pd.DataFrame = pd.read_html(str(table))[0]
    driver.quit()

    user: str = os.getlogin()
    period = f"{start_date.replace('/', '-')}_{end_date.replace('/', '-')}"
    formatted_path: str = SALES_PATH.format(user, period)
    print("Formatted path: ", formatted_path)
    req_df.to_excel(formatted_path, index=False)
    print(f"Sales data exported to {formatted_path}")

    bi_script: str = f"""import pandas as pd\ndf = pd.read_excel(r"{formatted_path}")\nprint(df)"""
    print("--------------------")
    print("PowerBI Script:\n")
    print(bi_script)
    print("--------------------")
