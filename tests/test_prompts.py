"""
Testes automatizados para validação de prompts.
"""
import re
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure

def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo de prompt não encontrado: {file_path}")
    except yaml.YAMLError as e:
        raise ValueError(f"YAML malformado em '{file_path}': {e}")

class TestPrompts:
    def test_prompt_has_system_prompt(self):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        data = load_prompts("prompts/bug_to_user_story_v2.yml")

        assert 'system_prompt' in data, "Campo 'system_prompt' não encontrado no YAML"
        assert data['system_prompt'], "Campo 'system_prompt' está vazio"
        assert len(data['system_prompt']) > 0, "Campo 'system_prompt' não contém texto"

    def test_prompt_has_role_definition(self):
        """Verifica se o prompt define uma persona (ex: "Você é um Product Manager")."""
        data = load_prompts("prompts/bug_to_user_story_v2.yml")
        system_prompt = data.get('system_prompt', '')

        role_patterns = [
            r'Você é',
            r'Atue como',
            r'Como um',
            r'You are',
            r'Act as',
            r'As a',
        ]

        has_role = any(re.search(pattern, system_prompt, re.IGNORECASE) for pattern in role_patterns)
        assert has_role, "Nenhuma definição de persona/role encontrada no prompt (ex: 'Você é', 'Atue como')"

    def test_prompt_mentions_format(self):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        data = load_prompts("prompts/bug_to_user_story_v2.yml")
        system_prompt = data.get('system_prompt', '')

        format_patterns = [
            r'Markdown',
            r'User Story',
            r'formato',
            r'estrutura',
            r'format',
            r'structure',
            r'template',
        ]

        has_format = any(re.search(pattern, system_prompt, re.IGNORECASE) for pattern in format_patterns)
        assert has_format, "Nenhuma especificação de formato encontrada (ex: 'Markdown', 'User Story', 'formato')"

    def test_prompt_has_few_shot_examples(self):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        data = load_prompts("prompts/bug_to_user_story_v2.yml")
        system_prompt = data.get('system_prompt', '')

        example_patterns = [
            r'Exemplo',
            r'Example',
            r'Input:',
            r'Output:',
            r'Entrada:',
            r'Saída:',
            r'### Exemplo \d+',
        ]

        has_examples = any(re.search(pattern, system_prompt, re.IGNORECASE) for pattern in example_patterns)
        assert has_examples, "Nenhum exemplo de entrada/saída encontrado (técnica Few-shot). Adicione exemplos ao prompt."

    def test_prompt_no_todos(self):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        data = load_prompts("prompts/bug_to_user_story_v2.yml")

        todo_pattern = r'(\[TODO\]|TODO:|FIXME|XXX)'

        system_prompt = data.get('system_prompt', '')
        todos_found = re.findall(todo_pattern, system_prompt, re.IGNORECASE)
        assert not todos_found, f"TODOs encontrados no system_prompt: {todos_found}"

        description = data.get('description', '')
        todos_found = re.findall(todo_pattern, description, re.IGNORECASE)
        assert not todos_found, f"TODOs encontrados em description: {todos_found}"

    def test_minimum_techniques(self):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        data = load_prompts("prompts/bug_to_user_story_v2.yml")

        assert 'techniques_applied' in data, "Campo 'techniques_applied' não encontrado no YAML"

        techniques = data['techniques_applied']

        assert isinstance(techniques, list), (
            f"Campo 'techniques_applied' deve ser lista, encontrado: {type(techniques)}"
        )

        assert len(techniques) >= 2, (
            f"Mínimo de 2 técnicas necessário (PRD), encontradas: {len(techniques)} - {techniques}"
        )

        valid_techniques = [
            'few_shot', 'chain_of_thought', 'tree_of_thought',
            'skeleton_of_thought', 'react', 'role_prompting', 'output_format',
        ]

        for tech in techniques:
            if tech not in valid_techniques:
                print(f"\nWarning: Técnica '{tech}' não é padrão. Técnicas válidas: {valid_techniques}")

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])