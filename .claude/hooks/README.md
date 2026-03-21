# Hooks

Скрипты, которые Claude Code запускает автоматически в ключевые моменты работы агента.
Конфигурация хуков — `hooks.json` (читается Claude Code из корня проекта или `.claude/`).

## Структура

```
hooks/
├── hooks.json                        ← конфиг для Claude Code
├── pre_tool_call/
│   ├── block_delete.py               ← запрет удаления/очистки защищённых файлов
│   └── require_tests.py              ← предупреждение если нет тест-файла
├── post_tool_call/
│   └── skill_eval.py                 ← self-improvement loop для SKILL.md
├── pre_compact/
│   └── save_context.py               ← снапшот состояния перед сжатием контекста
└── stop/
    └── session_report.py             ← итоговый отчёт сессии
```

## Хуки

### `pre_tool_call/block_delete.py`
**Триггер:** до любого `Write`, `Edit`, `MultiEdit`

Блокирует (`exit 2`) попытки перезаписать защищённые файлы пустым или почти пустым содержимым.

Защищённые файлы: `AGENT.md`, `SKILL.md`, `create-prd.md`, `PRD.md`, `ARCHITECTURE.md`, `README.md`
Защищённые директории: `skills/`, `commands/`, `hooks/`

---

### `pre_tool_call/require_tests.py`
**Триггер:** до любого `Write`, `Edit`, `MultiEdit`

Если агент пишет в файл реализации (`src/**/*.ts`, `src/**/*.py` и т.д.) и рядом нет тест-файла — выводит предупреждение в `stderr`. Не блокирует (`exit 0`), но агент должен создать тест до завершения задачи.

---

### `post_tool_call/skill_eval.py`
**Триггер:** после любого `Write`, `Edit`, `MultiEdit` на файл `SKILL.md`

Запускает набор **binary assertions** на изменённый скилл:
- Наличие frontmatter с обязательными полями
- Все обязательные секции присутствуют
- ≥ 5 принципов, каждый с примером `Violation:`
- ≥ 3 PATTERN-блока с полями Context / DO / DON'T / Reason
- ≥ 8 пунктов в Review Checklist
- Отсутствие расплывчатых фраз ("best practices", "be careful" и т.п.)
- Наличие секции Integration Points

Результат пишется в `.skill_eval_report.json` рядом со скиллом.
Если есть blocking failures — агент должен исправить и пересохранить (цикл повторяется).

---

### `pre_compact/save_context.py`
**Триггер:** перед сжатием контекстного окна

Сохраняет снапшот в `.context_snapshot.json`:
- Инferred pipeline stage
- Open questions из PRD
- [ASSUMED] маркеры
- TODO-комментарии в коде (до 20)
- [STUB] файлы
- Статус планов из `plans/`
- Resume hint для следующей сессии

---

### `stop/session_report.py`
**Триггер:** при остановке агента

Дописывает в `.session_log.md` краткий отчёт:
- Какие файлы были изменены за сессию
- Открытые вопросы из PRD
- Оставшиеся стабы и TODO
- Текущий pipeline stage
- Resume hint

## Коды выхода

| Код | Значение |
|-----|---------|
| `0` | Разрешить / продолжить |
| `2` | Заблокировать инструмент, показать сообщение агенту |

## Добавление нового хука

1. Создай скрипт в нужной директории (`pre_tool_call/`, `post_tool_call/`, `pre_compact/`, `stop/`)
2. Читай входные данные из `stdin` как JSON
3. Пиши сообщения агенту в `stderr`
4. Завершай с кодом `0` (allow) или `2` (block)
5. Добавь запись в `hooks.json`
6. Задокументируй здесь
