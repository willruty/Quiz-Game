import json
import os
import random
from flask import Flask, render_template, redirect, url_for, request, session


app = Flask(__name__)
app.secret_key = 'secret_key'

# Exemplo básico de perguntas e respostas para cada fase
questions = {
    1: [
        {"question": "O que é um Sistema Operacional?", "options": ["Software", "Hardware", "Rede", "Memória"], "answer": "Software"},
        {"question": "Qual é a principal função da memória RAM?", "options": ["Armazenar dados temporários", "Processar dados", "Gerenciar energia", "Executar softwares"], "answer": "Armazenar dados temporários"},
        {"question": "Qual dos itens é um exemplo de hardware?", "options": ["Excel", "Windows", "Teclado", "Chrome"], "answer": "Teclado"},
        {"question": "Qual é a unidade básica de dados na computação?", "options": ["Byte", "Pixel", "Mega", "Bit"], "answer": "Bit"},
        {"question": "O que significa CPU?", "options": ["Unidade de Processamento Central", "Unidade de Controle de Processos", "Central de Programação Unificada", "Centro de Processamento Universal"], "answer": "Unidade de Processamento Central"},
        {"question": "Qual dispositivo é usado para entrada de dados?", "options": ["Impressora", "Teclado", "Monitor", "Caixa de Som"], "answer": "Teclado"},
        {"question": "Qual o nome da memória que mantém dados mesmo sem energia?", "options": ["RAM", "Cache", "ROM", "NVRAM"], "answer": "ROM"},
        {"question": "Qual é a principal função do disco rígido?", "options": ["Processamento", "Armazenamento", "Rede", "Memória"], "answer": "Armazenamento"},
        {"question": "Qual software é usado para navegação na internet?", "options": ["Windows", "Excel", "Chrome", "Python"], "answer": "Chrome"},
        {"question": "Qual sistema operacional é da Microsoft?", "options": ["Linux", "macOS", "Windows", "Android"], "answer": "Windows"},
    ],
    2: [
        {"question": "O que é TCP?", "options": ["Um protocolo de rede", "Um sistema operacional", "Um software", "Um dispositivo de rede"], "answer": "Um protocolo de rede"},
        {"question": "O que significa IP?", "options": ["Protocolo de Internet", "Interface de Rede", "Internet Pessoal", "Internetwork Protocol"], "answer": "Protocolo de Internet"},
        {"question": "Qual dispositivo distribui sinal de internet?", "options": ["Switch", "Modem", "Roteador", "Hub"], "answer": "Roteador"},
        {"question": "Qual protocolo é usado para e-mails?", "options": ["FTP", "SMTP", "HTTP", "TCP"], "answer": "SMTP"},
        {"question": "O que é DNS?", "options": ["Serviço de Nome de Domínio", "Sistema de Rede Local", "Diretório de Nomes", "Servidor de Nome de Dados"], "answer": "Serviço de Nome de Domínio"},
        {"question": "O que significa URL?", "options": ["Localizador de Recursos Uniforme", "Endereço IP", "Localizador de Nome", "Protocolo de Transferência"], "answer": "Localizador de Recursos Uniforme"},
        {"question": "Qual é a função do HTTPS?", "options": ["Proteger a transferência de dados", "Acelerar a rede", "Controlar roteadores", "Codificar senhas"], "answer": "Proteger a transferência de dados"},
        {"question": "Qual protocolo envia arquivos pela internet?", "options": ["FTP", "SMTP", "HTTP", "TCP"], "answer": "FTP"},
        {"question": "Qual porta é usada para HTTP?", "options": ["80", "25", "443", "22"], "answer": "80"},
        {"question": "O que é uma rede LAN?", "options": ["Rede local", "Rede global", "Rede interna", "Rede sem fio"], "answer": "Rede local"},
    ],
    3: [
        {"question": "O que é criptografia?", "options": ["Codificação de dados", "Transferência de dados", "Compilação", "Armazenamento"], "answer": "Codificação de dados"},
        {"question": "O que é um firewall?", "options": ["Proteção contra acesso não autorizado", "Software antivírus", "Sistema operacional", "Dispositivo de rede"], "answer": "Proteção contra acesso não autorizado"},
        {"question": "O que significa HTTPS?", "options": ["Protocolo Seguro de Transferência de Hipertexto", "Protocolo Seguro de Email", "Protocolo de Dados", "Protocolo de Segurança"], "answer": "Protocolo Seguro de Transferência de Hipertexto"},
        {"question": "Qual é a função da autenticação?", "options": ["Verificar identidade", "Armazenar dados", "Transmitir dados", "Compilar programas"], "answer": "Verificar identidade"},
        {"question": "O que é phishing?", "options": ["Tentativa de roubo de dados", "Tipo de firewall", "Software", "Dispositivo"], "answer": "Tentativa de roubo de dados"},
        {"question": "Qual é a função de um antivírus?", "options": ["Proteger contra malware", "Acelerar o sistema", "Armazenar dados", "Distribuir rede"], "answer": "Proteger contra malware"},
        {"question": "O que é uma VPN?", "options": ["Rede Privada Virtual", "Servidor de Backup", "Protocolo de Transferência", "Rede Local"], "answer": "Rede Privada Virtual"},
        {"question": "Qual prática melhora a segurança de uma senha?", "options": ["Usar caracteres variados", "Usar senhas curtas", "Reutilizar senhas", "Salvar em texto plano"], "answer": "Usar caracteres variados"},
        {"question": "Qual o papel da política de segurança?", "options": ["Estabelecer diretrizes de proteção", "Aumentar o desempenho", "Manter usuários conectados", "Desenvolver software"], "answer": "Estabelecer diretrizes de proteção"},
        {"question": "Qual ataque usa força bruta?", "options": ["Brute-force", "Phishing", "Spear-phishing", "Spoofing"], "answer": "Brute-force"},
    ],
    4: [
        {"question": "O que é um algoritmo?", "options": ["Sequência de instruções", "Dispositivo de hardware", "Software de rede", "Código criptográfico"], "answer": "Sequência de instruções"},
        {"question": "Qual a função de uma estrutura de controle?", "options": ["Decidir fluxo do programa", "Armazenar dados", "Compilar código", "Testar variáveis"], "answer": "Decidir fluxo do programa"},
        {"question": "O que significa 'loop' em programação?", "options": ["Repetição de instruções", "Salto condicional", "Função de armazenamento", "Erro de código"], "answer": "Repetição de instruções"},
        {"question": "O que é uma variável?", "options": ["Local para armazenar valor", "Função matemática", "Processo de compilação", "Arquivo de texto"], "answer": "Local para armazenar valor"},
        {"question": "Qual símbolo inicia um comentário em Python?", "options": ["#", "//", "/*", "<!--"], "answer": "#"},
        {"question": "Qual estrutura usa if-else?", "options": ["Estrutura condicional", "Estrutura de repetição", "Variável", "Função"], "answer": "Estrutura condicional"},
        {"question": "O que é uma função?", "options": ["Bloco reutilizável de código", "Estrutura de controle", "Armazenamento", "Comando de saída"], "answer": "Bloco reutilizável de código"},
        {"question": "Qual é a saída de 'print(3 + 4)'?", "options": ["7", "34", "Error", "0"], "answer": "7"},
        {"question": "Qual linguagem é orientada a objetos?", "options": ["Java", "HTML", "CSS", "SQL"], "answer": "Java"},
        {"question": "O que é um operador lógico?", "options": ["E", "Contador", "Texto", "Sequência"], "answer": "E"},
    ],
    5: [
        {"question": "O que é SQL?", "options": ["Linguagem de consulta", "Sistema de rede", "Software antivírus", "Dispositivo de armazenamento"], "answer": "Linguagem de consulta"},
        {"question": "O que significa SGBD?", "options": ["Sistema Gerenciador de Banco de Dados", "Sistema Geral de Backup de Dados", "Servidor de Backup de Dados", "Software de Banco de Dados"], "answer": "Sistema Gerenciador de Banco de Dados"},
        {"question": "O que é uma chave primária?", "options": ["Identificador único", "Campo de armazenamento", "Nome do banco", "Tabela auxiliar"], "answer": "Identificador único"},
        {"question": "Qual comando insere dados no SQL?", "options": ["INSERT", "SELECT", "DELETE", "UPDATE"], "answer": "INSERT"},
        {"question": "Qual cláusula filtra dados em SQL?", "options": ["WHERE", "ORDER BY", "GROUP BY", "JOIN"], "answer": "WHERE"},
        {"question": "O que é uma consulta?", "options": ["Comando SQL para buscar dados", "Forma de salvar dados", "Armazenamento temporário", "Nome de tabela"], "answer": "Comando SQL para buscar dados"},
        {"question": "Qual comando remove dados em SQL?", "options": ["DELETE", "SELECT", "UPDATE", "DROP"], "answer": "DELETE"},
        {"question": "Qual comando modifica dados?", "options": ["UPDATE", "INSERT", "DELETE", "CREATE"], "answer": "UPDATE"},
        {"question": "O que é uma view em SQL?", "options": ["Consulta virtual", "Tabela principal", "Chave estrangeira", "Campo de índice"], "answer": "Consulta virtual"},
        {"question": "Qual função SQL retorna média?", "options": ["AVG", "SUM", "MAX", "COUNT"], "answer": "AVG"},
    ]
}

# Funções
def read_ranking():
    if os.path.exists('ranking.json'):
        with open('ranking.json', 'r') as file:
            return json.load(file)
    return []

def write_ranking(ranking_data):
    with open('ranking.json', 'w') as file:
        json.dump(ranking_data, file)

def get_ranking():
    # Lê os dados do ranking do arquivo
    ranking_data = read_ranking()
    
    # Adiciona o jogador atual ao ranking, se ele não estiver lá
    if 'name' in session and 'score' in session:
        # Verifica se o jogador já existe no ranking
        existing_player = next((player for player in ranking_data if player['name'] == session['name']), None)
        if existing_player:
            existing_player['score'] = max(existing_player['score'], session['score'])  # Atualiza a pontuação se maior
        else:
            ranking_data.append({"name": session['name'], "score": session['score']})

    # Ordena pela pontuação (maior para menor)
    sorted_ranking = sorted(ranking_data, key=lambda x: x['score'], reverse=True)
    
    # Salva o ranking atualizado no arquivo
    write_ranking(sorted_ranking)

    return sorted_ranking

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    session['name'] = request.form['player_name']
    session['score'] = 0
    session['current_phase'] = 1
    session['current_question_index'] = 0
    session['correct_answers_streak'] = 0
    return redirect(url_for('question'))

@app.route('/question', methods=['GET', 'POST'])
def question():
    if request.method == 'POST':
        user_answer = request.form['answer']
        correct_answer = questions[session['current_phase']][session['current_question_index']]['answer']
        
        if user_answer == correct_answer:
            session['score'] += 10
            session['correct_answers_streak'] += 1
            # Verifica se é a última pergunta da fase
            if session['current_question_index'] == 9:
                session['score'] += 100  # Bônus por completar a fase
        else:
            session['score'] -= 20 if session['current_phase'] > 3 else 0  # Penalidade após a fase 3
            session['correct_answers_streak'] = 0  # Reinicia a sequência de acertos

        # Bônus por acertos consecutivos
        if session['correct_answers_streak'] == 5:
            session['score'] += 50
        
        # Avança para a próxima pergunta
        session['current_question_index'] += 1
        
        # Se terminar todas as perguntas da fase, avança para a próxima fase
        if session['current_question_index'] >= len(questions[session['current_phase']]):
            session['current_phase'] += 1
            session['current_question_index'] = 0  # Reinicia o índice da pergunta
        
        # Redireciona para a página de perguntas
        return redirect(url_for('question'))

    # Se ainda houver perguntas na fase atual
    if session['current_phase'] <= len(questions):
        current_question = questions[session['current_phase']][session['current_question_index']]
        return render_template('question.html', phase=session['current_phase'], score=session['score'], question=current_question['question'], options=current_question['options'])
    else:
        return redirect(url_for('final'))

@app.route('/final')
def final():
    ranking_data = get_ranking()  # Pega o ranking
    position = next((i+1 for i, score in enumerate(ranking_data) if score['name'] == session['name']), None)  # Verifica a posição do jogador
    return render_template('final.html', score=session['score'], name=session['name'], position=position, ranking=ranking_data)

@app.route('/ranking')
def ranking():
    scores = get_ranking()
    # Ordena os jogadores pela pontuação em ordem decrescente
    sorted_scores = sorted(scores, key=lambda x: x['score'], reverse=True)
    # Enumera a lista ordenada
    enumerated_scores = [{'position': i + 1, 'name': player['name'], 'score': player['score']} for i, player in enumerate(sorted_scores)]
    return render_template('ranking.html', scores=enumerated_scores)

@app.route('/skip_question', methods=['POST'])
def skip_question():
    session['current_question_index'] += 1
    # Se terminar todas as perguntas da fase, avança para a próxima fase
    if session['current_question_index'] >= len(questions[session['current_phase']]):
        session['current_phase'] += 1
        session['current_question_index'] = 0  # Reinicia o índice da pergunta
    return redirect(url_for('question'))

@app.route('/eliminate_options', methods=['POST'])
def eliminate_options():
    current_question = questions[session['current_phase']][session['current_question_index']]
    if len(current_question['options']) > 2:
        current_question['options'].remove(current_question['answer'])
        incorrect_options = [opt for opt in current_question['options'] if opt != current_question['answer']]
        eliminated = random.sample(incorrect_options, 2)  # Elimina 2 opções incorretas
        for opt in eliminated:
            current_question['options'].remove(opt)
    return redirect(url_for('question'))

@app.route('/give_up', methods=['POST'])
def give_up():
    session.pop('name', None)
    session.pop('score', None)
    session.pop('current_phase', None)
    session.pop('current_question_index', None)
    session.pop('correct_answers_streak', None)
    return redirect(url_for('ranking'))

if __name__ == '__main__':
    app.run(debug=True)
