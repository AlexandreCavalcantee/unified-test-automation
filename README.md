# unified-test-automation

https://github.com/AlexandreCavalcantee/unified-test-automation

[![CI](https://github.com/AlexandreCavalcantee/unified-test-automation/actions/workflows/ci.yml/badge.svg)](https://github.com/AlexandreCavalcantee/unified-test-automation/actions/workflows/ci.yml)

Projeto unificado de automação de testes cobrindo dois cenários:

- **API** — Swagger Petstore (`https://petstore.swagger.io/v2`), endpoints **Pet**, **Store** e **User**.
- **Web** — SauceDemo (`https://www.saucedemo.com/`), fluxo E2E de login → carrinho → checkout.

Ambas as suítes rodam em uma única pipeline de CI no GitHub Actions.

---

## Tecnologias

| Camada | Stack |
|---|---|
| Linguagem | Python 3.11 |
| Test runner | pytest 8 + pytest-html |
| API client | requests + jsonschema |
| Web automation | Selenium 4 (Selenium Manager nativo, sem driver manual) |
| Padrões | Page Object Model, Factories de payload |
| CI | GitHub Actions (2 jobs paralelos) |

---

## Estrutura

```
unified-test-automation/
├── .github/workflows/ci.yml      # pipeline com jobs api-tests e web-tests
├── api/
│   ├── client.py                 # PetstoreClient (wrapper de requests.Session)
│   ├── conftest.py               # fixtures: client, unique_id
│   ├── data/payloads.py          # factories: pet_payload, order_payload, user_payload
│   ├── data/schemas.py           # JSON schemas + assert_schema helper
│   └── tests/                    # test_pet, test_store, test_user (23 testes)
├── web/
│   ├── utils/driver_factory.py   # Chrome headless com opções para CI
│   ├── conftest.py               # fixture driver + screenshot em falha
│   ├── pages/                    # POM: base/login/inventory/cart/checkout/side_menu
│   └── tests/                    # checkout_e2e, cart, sort, validation, logout, images (16 testes)
├── pytest.ini                    # markers: api, web, smoke
└── requirements.txt
```

---

## Pré-requisitos

- Python 3.11+
- Google Chrome (para os testes web)

---

## Instalação

```bash
git clone https://github.com/AlexandreCavalcantee/unified-test-automation.git
cd unified-test-automation
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Execução

```bash
# Toda a suíte
pytest

# Só API (Petstore)
pytest -m api

# Só Web (SauceDemo)
pytest -m web

# Web com browser visível (debug local)
HEADLESS=false pytest -m web

# Gerar relatório HTML
pytest --html=report.html --self-contained-html
```

---

## Estratégia de testes

### API — Petstore (23 cenários)

| Endpoint | Cobertura |
|---|---|
| **Pet** (9 testes) | criar, buscar por ID, atualizar, listar por status, listar por tag, deletar, idempotência de DELETE, 404 em ID inexistente, payload inválido |
| **Store** (6 testes) | criar pedido, buscar pedido, deletar pedido, inventário, 404 em ID inválido, payload inválido |
| **User** (8 testes) | criar, buscar, atualizar, login, logout, batch via createWithList, deletar, 404 em usuário inexistente |

Além de asserções de campo, respostas dos endpoints `/pet`, `/store/order` e `/user/{username}` são validadas contra **JSON Schemas** (`api/data/schemas.py`), garantindo o contrato e não só o comportamento.

Cada teste isola seus dados via fixture `unique_id` (timestamp em ms) — Petstore é mock e não limpa estado entre runs, então reutilizar IDs causa flakiness.

### Web — SauceDemo (16 cenários)

| Arquivo | O que valida |
|---|---|
| `test_checkout_e2e.py` | Fluxo completo de checkout + erros de login (locked_out_user, credenciais inválidas) |
| `test_cart.py` | Remover item via inventory (limpa o badge) e remover via página do carrinho |
| `test_inventory_sort.py` | Ordenação A→Z, Z→A, preço asc, preço desc |
| `test_checkout_validation.py` | Campos obrigatórios (nome, sobrenome, CEP) + cancelar no step-one volta ao carrinho |
| `test_logout.py` | Logout pelo menu lateral retorna à tela de login |
| `test_inventory_images.py` | `standard_user` exibe 6 imagens distintas; `problem_user` reproduz o bug de imagens duplicadas (regressão) |

Asserções intermediárias em cada etapa do fluxo principal — falha aponta o passo exato que quebrou, não só o resultado final.

---

## Decisões técnicas (Web)

SauceDemo é uma SPA React. Em Chrome headless, alguns padrões de Selenium "puro" se mostraram instáveis e foram resolvidos com pequenos desvios documentados aqui:

- **`BasePage.click()` vs `BasePage.js_click()`** — o click nativo do Selenium é o padrão e funciona para a maioria dos elementos. Para botões/links com handler React (cart link `<a>` sem `href`, botão Add to cart, Checkout, Continue, Finish), o click nativo às vezes registra como no-op em headless. `js_click()` dispara `element.click()` via `execute_script`, contornando problemas de coordenada e re-render do React.
- **`BasePage.type()` com setter nativo do `HTMLInputElement`** — `send_keys` engolia silenciosamente as teclas nos inputs do `Checkout: Your Information` (mesmo Selenium funcionando perfeitamente nos inputs de login). A solução padrão para inputs controlados por React é setar o `value` pelo setter do prototype (`Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set`) e disparar `input` + `change` events, garantindo que o estado React seja atualizado.
- **`wait_for_url()` após cada navegação** — todas as transições de página esperam explicitamente a mudança de URL antes do próximo passo, eliminando race conditions onde o teste age antes do React montar a próxima página.
- **`wait_for_remove_button()` após cada add to cart** — confirma de forma determinística que o clique registrou (botão muda de "Add to cart" para "Remove"), em vez de checar o badge do carrinho que atualiza com leve atraso.
- **Screenshot + URL/title em falha** — fixture `driver` em `web/conftest.py` salva print da tela em `screenshots/` quando um teste falha. O CI sobe esses prints como artifact `web-screenshots`.

---

## CI/CD

Pipeline definida em `.github/workflows/ci.yml` com **2 jobs paralelos**:

- `api-tests` — Python 3.11 + `pytest -m api`
- `web-tests` — Python 3.11 + Chrome stable + `pytest -m web`

Roda em `push` e `pull_request` para `main`. Cada job sobe um relatório HTML como artifact (`api-report` / `web-report`). Em falha do job web, screenshots são salvos no artifact `web-screenshots` para diagnóstico.

Acompanhe em: <https://github.com/AlexandreCavalcantee/unified-test-automation/actions>

---

## Prints do funcionamento

Coloque os screenshots em `assets/` e referencie aqui:

```markdown
![CI verde](assets/ci.png)
![API report](assets/api-report.png)
![Web report](assets/web-report.png)
```

> `assets/` está no `.gitignore` por padrão. Para versionar prints, remova essa linha do `.gitignore` ou adicione cada arquivo individualmente com `git add -f assets/<arquivo>`.
