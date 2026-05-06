"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

"""

import os
import sys
import re
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from langsmith import Client
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, save_yaml, check_env_vars, print_section_header

load_dotenv()


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    errors = []
    
    # T2: Campos obrigatórios
    required_fields = ['system_prompt', 'input_variables', 'version', 'description']
    for field in required_fields:
        if field not in prompt_data:
            errors.append(f"Campo obrigatório ausente: '{field}'")
    
    # Validações específicas
    if 'system_prompt' in prompt_data:
        if not isinstance(prompt_data['system_prompt'], str):
            errors.append("'system_prompt' deve ser string")
        elif len(prompt_data['system_prompt']) < 50:
            errors.append(f"'system_prompt' muito curto: {len(prompt_data['system_prompt'])} caracteres (mínimo 50)")
    
    if 'input_variables' in prompt_data:
        if not isinstance(prompt_data['input_variables'], list):
            errors.append("'input_variables' deve ser lista")
        elif len(prompt_data['input_variables']) == 0:
            errors.append("'input_variables' não pode estar vazia")
    
    if 'version' in prompt_data:
        version = str(prompt_data['version'])
        if not re.match(r'^\d+\.\d+$', version):
            errors.append(f"'version' com formato inválido: '{version}' (espera X.Y)")
    
    # Validação específica para v2+: techniques_applied não vazio
    if 'version' in prompt_data:
        version_num = float(str(prompt_data['version']))
        if version_num >= 2.0:
            if 'techniques_applied' not in prompt_data or not prompt_data['techniques_applied']:
                errors.append("v2+ deve ter 'techniques_applied' com pelo menos 1 técnica")
    
    return (len(errors) == 0, errors)


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict, yaml_path: str) -> tuple:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).
    
    Conforme doc oficial: https://docs.langchain.com/langsmith/manage-prompts-programmatically#push-a-prompt
    Usa apenas o nome do prompt. O LangSmith associa automaticamente ao workspace via API Key.
    
    Args:
        prompt_name: Nome do prompt (ex: "bug_to_user_story")
        prompt_data: Dados do prompt do YAML
        yaml_path: Caminho do arquivo YAML para atualizar timestamp
        
    Returns:
        (success, url, updated_data)
    """
    # T4: Converter para ChatPromptTemplate
    print(f"\n🔧 Convertendo para ChatPromptTemplate...")
    
    try:
        # Criar template com system + human messages
        # Human message é necessário para compatibilidade com Gemini
        human_template = prompt_data.get('human_template', '{bug_report}')
        template = ChatPromptTemplate.from_messages([
            ("system", prompt_data['system_prompt']),
            ("human", human_template),
        ])
        
        # Definir variáveis de entrada
        template.input_variables = prompt_data['input_variables']
        
        print(f"   ✓ Template criado")
        print(f"   ✓ System prompt: {len(prompt_data['system_prompt'])} caracteres")
        print(f"   ✓ Input variables: {prompt_data['input_variables']}")
        
    except Exception as e:
        print(f"\n❌ Erro ao criar ChatPromptTemplate: {e}")
        return False
    
    # T5: Push usando langsmith.Client (conforme doc oficial)
    version = str(prompt_data.get('version', '2.0'))
    # Identificador: apenas o nome do prompt (API Key define o owner)
    prompt_identifier = prompt_name
    
    print(f"\n🚀 Publicando no LangSmith Hub...")
    print(f"   Identificador: {prompt_identifier}")
    print(f"   Versão: v{version}")
    print(f"   Visibilidade: PÚBLICA")
    
    try:
        # Criar client e fazer push - doc: https://docs.langchain.com/langsmith/manage-prompts-programmatically
        client = Client()
        url = client.push_prompt(
            prompt_identifier,
            object=template,
            is_public=True  # Tornar prompt público conforme requisito
        )
        
        print(f"\n✅ Prompt publicado com sucesso!")
        print(f"   � Repositório: {url if url else prompt_identifier}")
        
        # T6: Atualizar YAML local com timestamp
        prompt_data['pushed_at'] = datetime.now().isoformat()
        if url:
            prompt_data['hub_url'] = url
        
        if save_yaml(prompt_data, yaml_path):
            print(f"   ✓ Timestamp registrado no YAML local")
        
        return (True, url, prompt_data)
        
    # T7: Tratamento de erros específicos
    except Exception as e:
        error_msg = str(e).lower()
        
        print(f"\n{'=' * 70}")
        
        if "cannot create a public prompt" in error_msg or "hub handle" in error_msg:
            print(f"❌ ERRO: Não foi possível criar prompt público")
            print(f"{'=' * 70}\n")
            print(f"Para resolver:")
            print(f"1. Acesse: https://smith.langchain.com/prompts")
            print(f"2. Clique em 'New Prompt' e crie um prompt público")
            print(f"3. Isso cria automaticamente seu handle no Hub")
            print(f"4. Execute novamente: python src/push_prompts.py")
            print(f"\nDoc oficial: https://docs.langchain.com/langsmith/manage-prompts-programmatically")
            
        elif "not found" in error_msg or "404" in error_msg:
            print(f"❌ ERRO: Recurso não encontrado")
            print(f"{'=' * 70}\n")
            print(f"Prompt não encontrado no LangSmith Hub.")
            print(f"Verifique se LANGSMITH_API_KEY está correto no .env")
            
        elif "unauthorized" in error_msg or "401" in error_msg or "403" in error_msg or "forbidden" in error_msg:
            print(f"❌ ERRO: API Key sem permissão de escrita")
            print(f"{'=' * 70}\n")
            print(f"A LANGSMITH_API_KEY não tem permissão para publicar prompts.")
            print(f"Verifique:")
            print(f"1. API Key está correta no .env")
            print(f"2. API Key tem permissão de WRITE no LangSmith")
            
        elif "connection" in error_msg or "network" in error_msg:
            print(f"❌ ERRO: Problema de conexão")
            print(f"{'=' * 70}\n")
            print(f"Não foi possível conectar ao LangSmith Hub.")
            print(f"Verifique sua conexão com a internet.")
            
        else:
            print(f"❌ ERRO: Falha inesperada")
            print(f"{'=' * 70}\n")
            print(f"Detalhes: {e}")
        
        return (False, None, None)


def main():
    """Função principal"""
    # T8: Output formatado
    print_section_header("Push de Prompts para o LangSmith Hub")
    
    # T1: Validar credenciais
    required_vars = ['LANGSMITH_API_KEY', 'USERNAME_LANGSMITH_HUB']
    if not check_env_vars(required_vars):
        print("\n💡 Configure no .env:")
        print("   LANGSMITH_API_KEY  → Obtenha em: https://smith.langchain.com/settings")
        print("   USERNAME_LANGSMITH_HUB → Seu handle no LangSmith Hub")
        return 1

    hub_username = os.environ.get('USERNAME_LANGSMITH_HUB', '').strip()
    if not hub_username:
        print("\n❌ USERNAME_LANGSMITH_HUB está vazio no .env")
        return 1
    
    # T3: Carregar arquivo YAML v2
    yaml_path = "prompts/bug_to_user_story_v2.yml"
    
    print(f"\n📂 Carregando prompt de: {yaml_path}")
    
    if not Path(yaml_path).exists():
        print(f"\n❌ Arquivo não encontrado: {yaml_path}")
        print("\n💡 Dica:")
        print("   1. Execute: python src/pull_prompts.py (gera v1)")
        print("   2. Copie v1 para v2: cp prompts/bug_to_user_story_v1.yml prompts/bug_to_user_story_v2.yml")
        print("   3. Edite v2 aplicando técnicas de otimização")
        print("   4. Execute novamente este script")
        return 1
    
    prompt_data = load_yaml(yaml_path)
    if not prompt_data:
        print(f"❌ Erro ao carregar YAML. Verifique sintaxe.")
        return 1
    
    print(f"   ✓ Arquivo carregado")
    
    # T2 & T3: Validar estrutura
    print(f"\n🔍 Validando estrutura do prompt...")
    is_valid, errors = validate_prompt(prompt_data)
    
    if not is_valid:
        print(f"\n❌ Prompt inválido. Erros encontrados:")
        for i, error in enumerate(errors, 1):
            print(f"   {i}. {error}")
        print(f"\nCorrija os erros no arquivo {yaml_path} e tente novamente.")
        return 1
    
    print(f"   ✓ Estrutura válida")
    
    # T4-T7: Push para o Hub — nome versionado conforme PRD: {username}/bug_to_user_story_v2
    prompt_identifier = f"{hub_username}/bug_to_user_story_v2"
    result = push_prompt_to_langsmith(prompt_identifier, prompt_data, yaml_path)
    
    if isinstance(result, tuple):
        success, hub_url, updated_data = result
    else:
        success = result
        hub_url = None
        updated_data = prompt_data
    
    if not success:
        print("\n❌ Push falhou. Veja os erros acima.")
        return 1
    
    # T8: Resumo final
    version = str(updated_data.get('version', '2.0'))
    print("\n" + "=" * 70)
    print("RESUMO")
    print("=" * 70)
    print(f"✓ Push concluído com sucesso")
    print(f"📄 Arquivo: prompts/bug_to_user_story_v{version}.yml")
    if hub_url:
        print(f"🔗 Hub: {hub_url}")
    print(f"🏷️  Técnicas aplicadas: {', '.join(updated_data.get('techniques_applied', []))}")
    print(f"\nPróximos passos:")
    if hub_url:
        print(f"1. Verificar prompt no Hub: {hub_url}")
    print(f"2. Avaliar v{version}: python src/evaluate.py")
    print(f"3. Se score < 0.9, criar v{float(version) + 1.0} e repetir")
    print("=" * 70)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
