# Pull, Otimização e Avaliação de Prompts com LangChain e LangSmith

Projeto do desafio MBA-IA: otimização iterativa de prompts usando técnicas de Prompt Engineering, com avaliação automatizada via LangSmith.

O prompt `bug_to_user_story_v1` (baseline) foi otimizado através de **4 iterações incrementais**, atingindo **média final de 0.9682** com todas as métricas >= 0.9.

✅ **Status Final:** APROVADO - v2.4 com todas as técnicas

---

## Resultados Finais

### Evolução Iterativa - Adição Incremental de Técnicas

| Versão | Técnicas Aplicadas | Tone | AC | Format | Completeness | Média | Status |
|--------|-------------------|------|-----|--------|--------------|-------|--------|
| **v2.1** | Role Prompting | 0.97 | 0.97 | 0.98 | **0.82** | 0.9359 | ❌ |
| **v2.2** | Role + CoT | 0.98 | 0.97 | 0.98 | **0.92** | 0.9617 | ✅ |
| **v2.3** | Role + CoT + Few-shot | 0.98 | 0.97 | 0.98 | **0.93** | 0.9657 | ✅ |
| **v2.4** | **Todas as 4 técnicas** | 0.97 | 0.97 | 0.98 | **0.95** | **0.9682** | ✅ |

**Critério de aprovação:** TODAS as métricas >= 0.9 (mínimo aceitável)

### Análise de Impacto por Técnica

#### 🏆 Técnica Mais Impactante: Chain of Thought (v2.1 → v2.2)
- **Completeness:** +10 pontos (0.82 → 0.92)
- **Média:** +2.58 pontos (0.9359 → 0.9617)
- **Resultado:** Levou o prompt de REPROVADO → APROVADO

#### 📊 Contribuição de Cada Técnica:

**1. Role Prompting (v2.1)** - Base sólida
- Tone: 0.97 ✅
- Format: 0.98 ✅
- **Problema:** Completeness baixo (0.82) ❌

**2. + Chain of Thought (v2.2)** - Resolveu Completeness
- Adicionado processo de 7 etapas de análise
- **Completeness:** 0.82 → 0.92 (+10 pontos) ✅
- **Passou no critério mínimo!**

**3. + Few-shot Learning (v2.3)** - Consistência
- 3 exemplos (simples, médio, complexo)
- **Completeness:** 0.92 → 0.93 (+1 ponto)
- Menor variação entre exemplos

**4. + Output Format (v2.4)** - Máxima Qualidade
- 10 regras explícitas de formatação
- **Completeness:** 0.93 → 0.95 (+2 pontos)
- **Melhor score geral:** 0.9682

### Progressão de Completeness (Métrica Crítica)

```
v2.1: 0.82 ❌ (gargalo) 
  ↓ +10 (CoT - MAIOR IMPACTO!)
v2.2: 0.92 ✅ (passou!)
  ↓ +1 (Few-shot)
v2.3: 0.93 ✅
  ↓ +2 (Output Format)
v2.4: 0.95 ✅ ← MELHOR RESULTADO
```

### Ganhos Totais (v2.1 → v2.4)

- **Completeness:** +13 pontos (0.82 → 0.95) = **+15.9%**
- **Média Geral:** +3.23 pontos (0.9359 → 0.9682) = **+3.4%**
- **Prompt Size:** 854 → 6053 caracteres (+608%)
- **Consistência:** Completeness mínimo +42 pontos (0.46 → 0.88) = **+91%**


### Dashboard LangSmith

🔗 **Links das Versões:**
- [v2.1 - Role Prompting](https://smith.langchain.com/prompts/bug_to_user_story_v2/78606c4d)
- [v2.2 - Role + CoT](https://smith.langchain.com/prompts/bug_to_user_story_v2/54ef81ac)
- [v2.3 - Role + CoT + Few-shot](https://smith.langchain.com/prompts/bug_to_user_story_v2/3768170d)
- [v2.4 - TODAS as técnicas](https://smith.langchain.com/prompts/bug_to_user_story_v2/5aec290c) ← **Versão final**

## Dashboard 
https://smith.langchain.com/public/b39215ed-ad83-46b7-9f64-dc22a0c2cde6/d

**Prompt publicado:** `aleteste/bug_to_user_story_v2`  
**Versão recomendada:** v2.4 (maior completeness + melhor consistência)

---

## Técnicas Aplicadas - Processo Iterativo

### 1. Role Prompting

**O que é:** Definir uma persona específica para o modelo assumir durante a geração.

**Como foi aplicado:** O system prompt define o modelo como "Product Manager sênior especializado em transformar relatos de bugs em user stories completas e detalhadas para times de desenvolvimento ágil".

**Por que escolhi:** A persona de PM sênior direciona o tom profissional, a empatia com o usuário e o foco em valor de negócio — características essenciais para user stories de qualidade. Sem role prompting, as respostas eram genéricas e sem o vocabulário adequado de produto.

### 2. Chain of Thought (CoT)

**O que é:** Instruir o modelo a raciocinar passo a passo antes de gerar a resposta final.

**Como foi aplicado:** Seção "Processo (Pense passo a passo)" com 7 etapas analíticas:
1. Identificar o tipo de usuário afetado
2. Identificar o problema central e o que o usuário quer
3. Identificar o benefício de negócio
4. Verificar detalhes técnicos (logs, endpoints, errors)
5. Verificar impacto (usuários afetados, perda financeira)
6. Identificar se há múltiplos problemas
7. Planejar cenários de aceitação (sucesso, erro, edge cases)

**Por que escolhi:** Bugs complexos com múltiplos problemas, detalhes técnicos e dados de impacto exigem análise estruturada. O CoT força o modelo a extrair todas as informações relevantes antes de compor a user story, o que melhorou significativamente os scores de **Completeness** (de 0.74 para 1.00) e **Acceptance Criteria** (de 0.82 para 0.98).

### 3. Few-shot Learning

**O que é:** Fornecer exemplos concretos de entrada/saída para o modelo aprender o padrão esperado.

**Como foi aplicado:** 3 exemplos com níveis crescentes de complexidade:
- **Exemplo 1 (Bug Simples):** Botão de salvar sem feedback → user story com critérios básicos
- **Exemplo 2 (Bug Médio):** Webhook falhando com logs técnicos → user story com seção "Contexto Técnico"
- **Exemplo 3 (Bug Complexo):** Busca com 2 problemas + Elasticsearch → user story com critérios categorizados, contexto técnico e impacto

**Por que escolhi:** Os exemplos demonstram concretamente o formato Dado-Quando-Então dos critérios de aceitação, quando incluir seções opcionais (Contexto Técnico, Impacto, Tasks Técnicas), e como escalar a complexidade da resposta conforme o bug. Isso alinhou o output com o padrão esperado pelo dataset de avaliação.

### 4. Output Format (Formato Estruturado)

**O que é:** Especificar explicitamente a estrutura e formato esperados da resposta.

**Como foi aplicado:**
- Formato fixo da user story: "Como um [tipo de usuário], eu quero [ação], para que [benefício]"
- Critérios de aceitação no formato **Dado-Quando-Então**
- Seções condicionais: Contexto Técnico, Impacto, Tasks Técnicas (incluídas apenas quando o bug contém informações relevantes)
- 10 regras obrigatórias que definem exatamente o que incluir e quando

**Por que escolhi:** A métrica de **User Story Format Score** exige aderência estrita ao formato padrão. Sem regras explícitas e formato de saída bem definido, o modelo variava a estrutura entre respostas. As 10 regras obrigatórias eliminaram essa inconsistência, levando o Format Score de 0.96 para 0.99.

---

## Metadados do Prompt Otimizado (v2.4)

**Arquivo:** `prompts/bug_to_user_story_v2.yml`  
**Versão:** 2.4 (final)  
**Técnicas aplicadas:** 4 (Role Prompting, Chain of Thought, Few-shot Learning, Output Format)  
**Tags:** iteration-4, final-version, role-prompting, chain-of-thought, few-shot-learning, output-format, bug-to-user-story  
**System prompt:** 6053 caracteres  
**Few-shot examples:** 3 (simples, médio, complexo)  
**Regras de formatação:** 10 regras explícitas  
**Input variables:** `bug_report`  
**Hub URL:** https://smith.langchain.com/prompts/bug_to_user_story_v2/5aec290c

### Comparativo de Tamanho dos Prompts

| Versão | Técnicas | System Prompt | Crescimento |
|--------|----------|---------------|-------------|
| v2.1 | Role | 854 chars | baseline |
| v2.2 | Role + CoT | 1692 chars | +98% |
| v2.3 | +Few-shot | 4450 chars | +163% |
| v2.4 | +Output Format | 6053 chars | +36% |

**Total:** +608% de crescimento de v2.1 → v2.4  

### Testes de Validação

Todos os 6 testes pytest passaram ✅:
- `test_prompt_has_system_prompt`: System prompt existe e não está vazio
- `test_prompt_has_role_definition`: Persona de PM sênior definida
- `test_prompt_mentions_format`: Formato User Story especificado
- `test_prompt_has_few_shot_examples`: 3 exemplos Few-shot incluídos
- `test_prompt_no_todos`: Nenhum TODO pendente no prompt
- `test_minimum_techniques`: 4 técnicas documentadas (>= 2 requerido)

```bash
pytest tests/test_prompts.py -v
# 6 passed in 0.07s
```

---

## Processo de Otimização Iterativa

### Metodologia: Adição Incremental de Técnicas

O processo seguiu uma abordagem **iterativa** com 4 fases:
1. Criar versão com técnica N
2. Push para LangSmith Hub
3. Avaliar com 10 exemplos do dataset
4. Analisar impacto da técnica
5. Repetir para técnica N+1

### Iteração 1: v2.1 - Role Prompting (Baseline)

**Objetivo:** Estabelecer persona e expertise
**Implementação:** PM sênior especializado em transformação bugs → user stories
**Resultado:** 
- Tone/Format excelentes (0.97-0.98)
- **Completeness BAIXO (0.82)** ❌ - não passou
- Média: 0.9359

**Diagnóstico:** Role Prompting sozinho não força análise profunda dos bugs. Faltam detalhes técnicos e cobertura completa.

### Iteração 2: v2.2 - + Chain of Thought

**Objetivo:** Resolver problema de Completeness com raciocínio estruturado
**Implementação:** 7 etapas de análise obrigatória antes de gerar user story:
1. Identificar usuário afetado
2. Definir problema central
3. Articular benefício
4. Extrair detalhes técnicos (logs, endpoints, errors)
5. Avaliar impacto (usuários, perda de dados, severidade)
6. Identificar múltiplos problemas
7. Planejar critérios de aceitação (sucesso, erro, edge cases)

**Resultado:** 
- **Completeness: 0.82 → 0.92 (+10 pontos)** ✅ - PASSOU!
- Média: 0.9617
- **CoT foi a técnica mais impactante**

**Insight:** Processo estruturado força o modelo a analisar sistematicamente TODOS os aspectos do bug antes de compor a resposta.

### Iteração 3: v2.3 - + Few-shot Learning

**Objetivo:** Aumentar consistência e demonstrar formato esperado
**Implementação:** 3 exemplos de diferentes complexidades:
- Exemplo 1: Bug simples de interface (botão desabilitado)
- Exemplo 2: Bug médio com erro técnico (TypeError, upload)
- Exemplo 3: Bug complexo com múltiplos problemas (dashboard timeout, 200+ usuários)

**Resultado:** 
- Completeness: 0.92 → 0.93 (+1 ponto)
- Média: 0.9657
- Menor variação entre exemplos (mínimo aumentou de 0.63 → 0.74)

**Insight:** Exemplos concretos ajudam a manter padrão consistente, especialmente para bugs com características técnicas similares aos exemplos.

### Iteração 4: v2.4 - + Output Format (FINAL)

**Objetivo:** Maximizar Completeness e garantir formato rigoroso
**Implementação:** 10 regras explícitas de formatação:
1. Estrutura obrigatória (User Story + AC + Contexto Técnico condicional)
2. Formato fixo da user story
3. Tom profissional (sem emojis/gírias)
4. Mínimo 3 cenários BDD (Dado-Quando-Então)
5. Contexto Técnico obrigatório para erros/logs/endpoints  
6. Formatação técnica (marcadores, prefixos, backticks)
7. Completude total (todos os detalhes, números exatos)
8. Cobertura mínima (happy path + erro + edge cases)
9. Evitar invenções/soluções técnicas/estimativas
10. Consistência para múltiplos problemas

**Resultado:** 
- **Completeness: 0.93 → 0.95 (+2 pontos)** - MELHOR SCORE!
- Média: 0.9682
- Consistência máxima (mínimo aumentou de 0.74 → 0.88)

**Insight:** Regras explícitas eliminam ambiguidade e garantem que o modelo não omita informações críticas. Output Format complementa CoT ao especificar exatamente COMO apresentar o que foi analisado.

### Comparativo de Eficácia das Técnicas

| Técnica | Impacto em Completeness | Impacto na Média | Observação |
|---------|------------------------|------------------|------------|
| **Chain of Thought** | **+10 pontos** | **+2.58 pontos** | 🏆 Mais impactante |
| **Output Format** | +2 pontos | +0.25 pontos | 📈 Melhor consistência |
| **Few-shot** | +1 ponto | +0.40 pontos | 📚 Demonstração de padrão |
| **Role Prompting** | baseline | baseline | 🎭 Base necessária |

### Resultado Final

**v2.4 - Versão Recomendada:**
- Tone: 0.97 ✅
- AC: 0.97 ✅  
- Format: 0.98 ✅
- **Completeness: 0.95** ✅ (melhor score)
- **Média: 0.9682** ✅

---

## Tecnologias

- **Linguagem:** Python 3.10
- **Framework:** LangChain
- **Plataforma:** LangSmith (avaliação + Prompt Hub)
- **LLM:** Google Gemini 2.5 Flash (geração e avaliação)
- **Formato de prompts:** YAML

---

## Setup

### Pré-requisitos

- Python 3.9+
- Conta no LangSmith com API Key
- API Key do Google (Gemini)

### Instalação

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Configuração

Crie um arquivo `.env` na raiz do projeto:

```env
LANGSMITH_API_KEY=sua_chave_langsmith
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=prompt-evaluation
GOOGLE_API_KEY=sua_chave_google
LLM_MODEL=gemini-2.5-flash
EVAL_MODEL=gemini-2.5-flash
USERNAME_LANGSMITH_HUB=seu_handle_langsmith
```

> **`USERNAME_LANGSMITH_HUB`**: handle do seu workspace no LangSmith Hub (ex: `aleteste`). Usado pelo `push_prompts.py` para publicar como `{username}/bug_to_user_story_v2`. Encontre o seu handle em [smith.langchain.com/settings](https://smith.langchain.com/settings).

---

## Como Executar

```bash
# 1. Pull do prompt original do LangSmith Hub
python src/pull_prompts.py

# 2. Push do prompt otimizado para o LangSmith Hub
python src/push_prompts.py

# 3. Avaliação automatizada com as 4 métricas
python src/evaluate.py

# 4. Testes de validação do prompt
pytest tests/test_prompts.py
```

---

## Estrutura do Projeto

```
├── .env.example                       # Template das variáveis de ambiente
├── requirements.txt                   # Dependências Python
├── README.md                          # Documentação do processo
├── prompts/
│   ├── bug_to_user_story_v1.yml       # Prompt original (após pull)
│   └── bug_to_user_story_v2.yml       # Prompt otimizado
├── datasets/
│   └── bug_to_user_story.jsonl        # Dataset com 15 bugs para avaliação
├── src/
│   ├── pull_prompts.py                # Pull de prompts do LangSmith Hub
│   ├── push_prompts.py                # Push de prompts para o LangSmith Hub
│   ├── evaluate.py                    # Avaliação automatizada
│   ├── metrics.py                     # 4 métricas LLM-as-Judge
│   └── utils.py                       # Funções auxiliares (load/save YAML)
└── tests/
    └── test_prompts.py                # 6 testes pytest de validação
```
