import os
import time
import requests

def exibir_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=" * 50)
    print("        FACE THE HELL - by @lorzcc_        ")
    print("=" * 50)
    print("Status: ONLINE | Modo: Conexão via API")
    print("=" * 50)

def buscar_cep_real():
    exibir_banner()
    cep = input("Digite o CEP que deseja puxar (somente números): ").strip()
    print("\n[+] Conectando aos servidores externos...")
    time.sleep(1)
    
    url = f"https://viacep.com.br/ws/{cep}/json/"
    try:
        resposta = requests.get(url)
        dados = resposta.json()
        if "erro" not in dados:
            print("\n[!] DADOS ENCONTRADOS [!]")
            print(f"-> CEP: {dados.get('cep')}")
            print(f"-> Logradouro: {dados.get('logradouro')}")
            print(f"-> Bairro: {dados.get('bairro')}")
            print(f"-> Cidade: {dados.get('localidade')}")
            print(f"-> Estado: {dados.get('uf')}")
        else:
            print("\n[-] Este CEP não existe na base de dados nacional.")
    except Exception:
        print("\n[-] Erro de conexão. Verifique sua internet.")
    input("\nPressione Enter para voltar ao menu...")

def puxar_info_site():
    exibir_banner()
    dominio = input("Digite o domínio do site (ex: google.com): ").strip()
    print(f"\n[+] Realizando varredura WHOIS em {dominio}...")
    time.sleep(1)
    
    url = f"https://rdap.org/domain/{dominio}"
    try:
        resposta = requests.get(url)
        if resposta.status_code == 200:
            dados = resposta.json()
            print("\n[!] INFORMAÇÕES DE REGISTRO PÚBLICO [!]")
            print(f"-> Domínio pesquisado: {dados.get('ldhName')}")
            entities = dados.get('entities', [])
            if entities:
                print(f"-> ID do Registrante: {entities[0].get('handle', 'Não listado')}")
            nameservers = dados.get('nameservers', [])
            if nameservers:
                print("-> Servidores de DNS:")
                for ns in nameservers[:2]:
                    print(f"   [- ] {ns.get('ldhName')}")
        else:
            print("\n[-] Não foi possível encontrar dados para este domínio.")
    except Exception:
        print("\n[-] Falha ao conectar com o servidor de registros.")
    input("\nPressione Enter para voltar ao menu...")

def geolocalizar_ip():
    exibir_banner()
    print("Deixe em BRANCO (aperte Enter) para buscar o SEU próprio IP")
    alvo = input("Ou digite o IP de destino que deseja rastrear: ").strip()
    print(f"\n[+] Rastreando rota de rede para: {alvo if alvo else 'Seu IP Público'}...")
    time.sleep(1)
    
    url = f"http://ip-api.com/json/{alvo}"
    try:
        resposta = requests.get(url)
        dados = resposta.json()
        if dados.get("status") == "success":
            print("\n[!] GEOLOCALIZAÇÃO DE IP ENCONTRADA [!]")
            print(f"-> IP Alvo: {dados.get('query')}")
            print(f"-> País: {dados.get('country')} ({dados.get('countryCode')})")
            print(f"-> Estado/Região: {dados.get('regionName')}")
            print(f"-> Cidade: {dados.get('city')}")
            print(f"-> Provedor (ISP): {dados.get('isp')}")
        else:
            print("\n[-] Falha ao rastrear IP. Verifique o formato.")
    except Exception:
        print("\n[-] Erro ao se conectar com a API de Geolocalização.")
    input("\nPressione Enter para voltar ao menu...")

def osint_busca_publica():
    exibir_banner()
    print("1. Buscar Nome Completo ")
    print("2. Rastrear User ")
    print("-" * 50)
    sub_opcao = input("Escolha o tipo de busca OSINT: ").strip()
    
    if sub_opcao == "1":
        exibir_banner()
        nome = input("Digite o NOME COMPLETO para buscar: ").strip()
        if not nome:
            print("\n[-] Nome inválido.")
            time.sleep(1)
            return
            
        print(f"\n[+] Gerando indexadores de registros públicos para: {nome}...")
        time.sleep(0.5)
        
        # Formata o nome para os padrões de URL de busca
        nome_url_escavador = nome.replace(" ", "+")
        nome_url_jusbrasil = nome.replace(" ", "%20")
        
        url_escavador = f"https://www.escavador.com/busca?q={nome_url_escavador}"
        url_jusbrasil = f"https://www.jusbrasil.com.br/busca?q={nome_url_jusbrasil}"
        
        print("\n[!] LINKS DE BUSCA OSINT GERADOS COM SUCESSO [!]")
        print(f"-> Alvo: {nome}")
        print("\nPressione e segure em cima do link no Termux para abrir no navegador:")
        print(f"\n[\033[92m+\033[0m] Diários Oficiais (Escavador):")
        print(f"   >> {url_escavador}")
        print(f"\n[\033[92m+\033[0m] Processos e Consultas Jurídicas (Jusbrasil):")
        print(f"   >> {url_jusbrasil}")
            
    elif sub_opcao == "2":
        exibir_banner()
        user = input("Digite o @ / Username para rastrear (sem o @): ").strip()
        if not user:
            print("\n[-] Username inválido.")
            time.sleep(1)
            return
            
        print(f"\n[+] Mapeando pegada digital de '{user}' nas redes sociais...\n")
        time.sleep(1)
        
        redes = {
            "GitHub": f"https://github.com/{user}",
            "Twitter/X": f"https://twitter.com/{user}",
            "Instagram": f"https://instagram.com/{user}",
            "Reddit": f"https://www.reddit.com/user/{user}",
            "Twitch": f"https://www.twitch.tv/{user}",
            "Pinterest": f"https://pinterest.com/{user}",
            "TikTok": f"https://www.tiktok.com/{user}",
            "Facebook": f"https://facebook.com/{user}",
        }
        
        encontrados = 0
        for nome_rede, url in redes.items():
            try:
                resposta = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=3)
                if resposta.status_code == 200:
                    print(f"[\033[92m+\033[0m] {nome_rede}: ENCONTRADO -> {url}")
                    encontrados += 1
                else:
                    print(f"[\033[91m-\033[0m] {nome_rede}: Não encontrado")
            except Exception:
                print(f"[-] {nome_rede}: Erro ao checar")
                
        print(f"\n[!] Varredura concluída. Total de perfis ativos achados: {encontrados}")
    else:
        print("\n[-] Opção inválida!")
        
    input("\nPressione Enter para voltar ao menu...")

while True:
    exibir_banner()
    print("1. Consultar CEP")
    print("2. Mapear Registro de Site")
    print("3. Rastrear IP")
    print("4. Investigação de Dados (OSINT) ")
    print("5. Sair")
    print("=" * 50)
    
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        buscar_cep_real()
    elif opcao == "2":
        puxar_info_site()
    elif opcao == "3":
        geolocalizar_ip()
    elif opcao == "4":
        osint_busca_publica()
    elif opcao == "5":
        print("\nDesconectando o Face the hell... ")
        break
    else:
        print("\nOpção inválida!")
        time.sleep(1)

