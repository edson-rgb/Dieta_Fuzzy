import streamlit.web.cli as stcli
import sys
from pathlib import Path

if __name__ == "__main__":
    # Caminho para o arquivo principal da interface
    sys.argv = ["streamlit", "run", str(Path(__file__).parent / "app" / "interface.py")]
    sys.exit(stcli.main())
