# Generador texto a imagen usando los workers de cloudflare

## Instalacion

Copiar [.streamlit/secrets.toml.example](./.streamlit/secrets.toml.example) a `.streamlit/secrets.toml`.

```bash
python -m venv venv
source ./venv/bin/activate
python -m pip install -r requirements.txt
```

```cmd
python -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
```

## Correr

Correr app de Streamlit:

```bash
python -m streamlit run Inicio.py
```