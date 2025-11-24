import sys
import os

# adiciona a raiz ao sys.path
ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.append(ROOT)

from src.metricas.main_metricas import main

if __name__ == "__main__":
    main()