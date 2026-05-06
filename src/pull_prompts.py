"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

"""

import os
import sys
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from langsmith import Client
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()


def pull_prompts_from_langsmith():
    """
    Faz pull do prompt do LangSmith Hub e salva localmente em YAML.
    
    Returns:
        bool: True se sucesso, False se falha
    """
    # T2: Logging de início
    print("\n🔄 Conectando ao LangSmith Hub...")
    
    # T3: Implementar pull com Client.pull_prompt()
    prompt_identifier = "leonanluppi/bug_to_user_story_v1"
    print(f"   Fazendo pull do prompt: {prompt_identifier}")
    
    try:
        # pull_prompt usando Client.pull_prompt() conforme doc oficial
        client = Client()
        prompt = client.pull_prompt(prompt_identifier)
        print(f"   ✓ Prompt baixado com sucesso")
        
    # T7: Tratamento de erros específicos
    except Exception as e:
        error_msg = str(e).lower()
        
        print(f"\n{'=' * 70}")
        if "not found" in error_msg or "404" in error_msg:
            print(f"❌ ERRO: Prompt não encontrado no Hub")
            print(f"{'=' * 70}\n")
            print(f"O prompt '{prompt_identifier}' não existe no LangSmith Hub.")
            print(f"Verifique:")
            print(f"1. O nome está correto: {prompt_identifier}")
            print(f"2. Você tem acesso ao prompt")
            print(f"3. O prompt foi publicado no Hub")
        elif "connection" in error_msg or "network" in error_msg:
            print(f"❌ ERRO: Problema de conexão")
            print(f"{'=' * 70}\n")
            print(f"Não foi possível conectar ao LangSmith Hub.")
            print(f"Verifique sua conexão com a internet.")
        elif "api key" in error_msg or "unauthorized" in error_msg or "401" in error_msg or "403" in error_msg or "forbidden" in error_msg:
            print(f"❌ ERRO: API Key inválida ou sem permissão")
            print(f"{'=' * 70}\n")
            print(f"A LANGSMITH_API_KEY está inválida ou não tem permissão.")
            print(f"Verifique o valor no arquivo .env")
        else:
            print(f"❌ ERRO: Falha inesperada")
            print(f"{'=' * 70}\n")
            print(f"Detalhes: {e}")
        
        return False
    
    # T4: Extrair dados do ChatPromptTemplate
    print(f"\n📦 Extraindo dados do prompt...")
    
    system_prompt = ""
    input_variables = []
    
    # ChatPromptTemplate geralmente tem messages
    if hasattr(prompt, 'messages'):
        for message in prompt.messages:
            if hasattr(message, 'prompt') and hasattr(message.prompt, 'template'):
                system_prompt = message.prompt.template
                break
    
    # Extrair variáveis de entrada
    if hasattr(prompt, 'input_variables'):
        input_variables = prompt.input_variables
    
    # Validação básica
    if not system_prompt:
        print(f"   ❌ Erro: Não foi possível extrair system_prompt do template")
        return False
    
    print(f"   ✓ Extraídos {len(system_prompt)} caracteres do prompt")
    print(f"   ✓ Variáveis de entrada: {input_variables}")
    
    # T5: Estruturar dados em dict Python
    print(f"\n🔧 Estruturando dados...")
    
    prompt_data = {
        'description': 'Converte relatórios de bugs em user stories formatadas',
        'version': '1.0',
        'source': prompt_identifier,
        'pulled_at': datetime.now().isoformat(),
        'system_prompt': system_prompt,
        'input_variables': input_variables,
        'techniques_applied': [],  # Vazio no v1, será preenchido no v2
        'metadata': {
            'original_author': 'leonanluppi',
            'domain': 'bug_to_user_story'
        }
    }
    
    print(f"   ✓ Estrutura YAML preparada")
    
    # T6: Salvar YAML em arquivo
    output_path = "prompts/bug_to_user_story_v1.yml"
    
    # Verificar se já existe
    if Path(output_path).exists():
        print(f"\n⚠️  Arquivo já existe: {output_path}")
        print(f"   Pulando para não sobrescrever.")
        print(f"   Para baixar novamente, delete o arquivo primeiro.")
        return True
    
    print(f"\n💾 Salvando arquivo...")
    print(f"   Destino: {output_path}")
    
    if save_yaml(prompt_data, output_path):
        print(f"   ✓ Arquivo salvo com sucesso!")
        print(f"   📄 {Path(output_path).absolute()}")
        return True
    else:
        print(f"   ❌ Erro ao salvar arquivo")
        return False


def main():
    """Função principal"""
    print_section_header("Pull de Prompts do LangSmith")
    
    # T1: Validar credenciais do arquivo .env
    if not check_env_vars(['LANGSMITH_API_KEY']):
        print("\n💡 Dica: Copie .env.example para .env e configure suas credenciais")
        return 1
    
    # T2-T7: Executar pull
    success = pull_prompts_from_langsmith()
    
    if not success:
        print("\n❌ Pull falhou. Veja os erros acima.")
        return 1
    
    # T8: Resumo final
    print("\n" + "=" * 70)
    print("RESUMO")
    print("=" * 70)
    print("✓ Pull concluído com sucesso")
    print("📄 Arquivo: prompts/bug_to_user_story_v1.yml")
    print("\nPróximos passos:")
    print("1. Revisar o prompt em: prompts/bug_to_user_story_v1.yml")
    print("2. Criar versão otimizada: prompts/bug_to_user_story_v2.yml")
    print("3. Fazer push: python src/push_prompts.py")
    print("=" * 70)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
