# Premier League Match Predictor - Demonstração
# Este notebook demonstra o uso da package pl-match-predictor

# 1. INSTALAÇÃO DA PACKAGE
# Execute no terminal: pip install pl-match-predictor
# Ou para instalar com dependências de desenvolvimento: pip install pl-match-predictor[dev]

# 2. IMPORTAR MÓDULOS
import sys
print(f"Python version: {sys.version}\n")

# Importar módulos da package
try:
    # Exemplo de importação - ajuste conforme a estrutura real da sua package
    from server.data.getdata.get_data import main as fetch_data
    from server.modelbuild.predictor import main as train_model
    from server.modelbuild.make_prediction import main as make_prediction
    
    print("✅ Package importada com sucesso")
except ImportError as e:
    print(f"⚠️ Erro ao importar: {e}")
    print("Certifique-se de que a package está instalada corretamente")

# 3. OBTER DADOS (usando o comando CLI)
print("\n" + "="*60)
print("1. OBTENÇÃO DE DADOS")
print("="*60)

print("""
Para obter os dados mais recentes, execute no terminal:
$ pl-fetch-data

Ou programaticamente:
""")

# Exemplo de como chamar a função programaticamente
# fetch_data()  # Descomente para executar

# 4. TREINAR O MODELO
print("\n" + "="*60)
print("2. TREINAMENTO DO MODELO")
print("="*60)

print("""
Para treinar o modelo com os dados disponíveis:
$ pl-train

Ou programaticamente:
""")

# Exemplo de como chamar a função programaticamente
# train_model()  # Descomente para executar

# 5. FAZER PREVISÕES
print("\n" + "="*60)
print("3. FAZER PREVISÕES")
print("="*60)

print("""
Para fazer previsões para próximos jogos:
$ pl-predict

Ou programaticamente:
""")

# Exemplo de como chamar a função programaticamente
# make_prediction()  # Descomente para executar

# 6. USO PROGRAMÁTICO AVANÇADO
print("\n" + "="*60)
print("4. USO PROGRAMÁTICO AVANÇADO")
print("="*60)

print("""\n
# Exemplo de uso direto dos módulos
from server.model.modelbuild.predictor import PremierLeaguePredictor
from server.data.preprocessing import DataProcessor

# 1. Processar dados
# processor = DataProcessor()
# processed_data = processor.load_and_preprocess('dados.csv')

# 2. Treinar modelo
# predictor = PremierLeaguePredictor()
# predictor.train(processed_data)
# predictor.save_model('modelo.joblib')

# 3. Fazer previsão
# next_matches = [...]  # Lista de próximos jogos
# predictions = predictor.predict(next_matches)
# print(predictions)
""")

# 7. VERIFICAR CONFIGURAÇÃO
print("\n" + "="*60)
print("5. INFORMAÇÕES DA PACKAGE")
print("="*60)

# Verificar informações da package instalada
import subprocess
import sys

def check_package_info():
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "show", "pl-match-predictor"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("Informações da package instalada:")
            print(result.stdout)
        else:
            print("Package não encontrada. Execute: pip install pl-match-predictor")
    except Exception as e:
        print(f"Erro ao verificar package: {e}")

check_package_info()

# 8. EXEMPLO PRÁTICO COMPLETO
print("\n" + "="*60)
print("6. EXEMPLO DE FLUXO COMPLETO")
print("="*60)

print("""\n
# Fluxo completo de uso:
# 1. Configurar ambiente
# 2. Executar pl-fetch-data para obter dados atualizados
# 3. Executar pl-train para treinar modelo
# 4. Executar pl-predict para gerar previsões
# 5. Analisar resultados

# Para desenvolvimento:
# $ pip install pl-match-predictor[dev]
# $ pytest  # Executar testes
# $ black . # Formatar código
# $ flake8  # Verificar estilo
""")

print("\n" + "="*60)
print("RECURSOS ADICIONAIS")
print("="*60)

print("""
📚 Documentação: https://miguelvila02.github.io/pl-match-predictor
🐛 Reportar bugs: https://github.com/miguelvila02/pl-match-predictor/issues
📦 Código fonte: https://github.com/miguelvila02/pl-match-predictor

Comandos disponíveis:
- pl-fetch-data: Obtém dados atualizados
- pl-train: Treina o modelo de machine learning
- pl-predict: Gera previsões para próximos jogos
""")# %% [markdown]
# 

# %%



