import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os

def configurar_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")

    chrome_options.binary_location = "/opt/chrome/chrome"

    driver = webdriver.Chrome(
        service=Service("/opt/chromedriver"),
        options=chrome_options
    )
    return driver

def buscar_producto(sku):
    driver = configurar_driver()
    try:
        url = f"https://www.homedepot.com.mx/search/?q={sku}"
        driver.get(url)
        time.sleep(3)

        resultados = driver.find_elements(By.CLASS_NAME, "product")

        productos = []
        for producto in resultados[:3]:
            try:
                nombre = producto.find_element(By.CLASS_NAME, "product-title").text
                precio = producto.find_element(By.CLASS_NAME, "product-price").text
                enlace = producto.find_element(By.TAG_NAME, "a").get_attribute("href")
                imagen = producto.find_element(By.TAG_NAME, "img").get_attribute("src")

                productos.append({
                    "nombre": nombre,
                    "precio": precio,
                    "enlace": enlace,
                    "imagen": imagen
                })
            except:
                continue
        return productos
    finally:
        driver.quit()

# Interfaz Streamlit
st.title("🔍 Buscador Home Depot por SKU")

sku = st.text_input("Introduce el SKU:", "")

if st.button("Buscar") and sku:
    with st.spinner("Buscando producto..."):
        resultados = buscar_producto(sku.strip())

    if resultados:
        for r in resultados:
            st.subheader(r["nombre"])
            st.image(r["imagen"], width=300)
            st.write(f"💲 Precio: {r['precio']}")
            st.markdown(f"[🔗 Ver producto]({r['enlace']})")
    else:
        st.error("❌ No se encontraron productos.")
