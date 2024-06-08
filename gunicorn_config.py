import os
from dotenv import load_dotenv
load_dotenv()

port = os.environ.get('PORT', '5000')  # Utilisez 8000 comme port par défaut
bind = f'0.0.0.0:{port}'
# Configuration des logs pour qu'ils s'affichent dans le terminal
accesslog = '-'  # Les logs d'accès s'afficheront dans le terminal
errorlog = '-'   # Les logs d'erreurs s'afficheront dans le terminal
loglevel = 'info'  # Le niveau de log (peut être debug, info, warning, error, critical)