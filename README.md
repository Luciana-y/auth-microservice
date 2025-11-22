# auth-microservice
## 1. Instalación
1.  Clona el repositorio:
    ```bash
    git clone git@github.com:LeonardoMontesinos/cloud-hack-backend.git
    cd cloud-hack-backend
    ```

2.  Instala los plugins de Serverless (especialmente el de Python):
    ```bash
    sls plugin install -n serverless-python-requirements
    ```

3.  Crea un entorno virtual de Python e instala las dependencias:
    ```bash
    # Crea el entorno virtual
    python -m venv .venv
    
    # Actívalo (Linux/macOS)
    source .venv/bin/activate
    # (o en Windows Powershell)
    # .\.venv\Scripts\Activate.ps1
    
    # Instala las librerías
    pip install -r requirements.txt
    ```

4. Ya puedes deployarlo:
```bash
sls deploy
```
