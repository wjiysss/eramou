# Browser Prototype Architecture

This document records the current browser prototype structure so future changes
can extend the real ERB/CSV integration without re-discovering the layout from
chat history.

## Goals And Boundaries

- The browser UI is a thin renderer for backend state.
- Frontend code must not store game data, command tables, kojo text, or command
  effects.
- There should be no frontend fallback tables for game behavior.
- Command names, command behavior, parameter changes, and kojo should come from
  the backend reading real `CSV` and `ERB` files.
- Unsupported ERB semantics should stop loudly or be reported as partial, not
  silently replaced with fake behavior.

## Runtime Entry Points

- `web-prototype/server.py` serves the prototype at `http://127.0.0.1:4307/`.
- `web-prototype/index.html` is the static page shell.
- `web-prototype/app.js` fetches backend state and posts user actions.
- `web-prototype/styles.css` controls the Emuera-like blue text layout.

`index.html` uses query-string cache busting on both `styles.css` and `app.js`.
When changing frontend rendering or ability-page layout, bump these versions so
the in-app browser does not keep stale assets.

The backend API currently exposes:

- `GET /api/state`: returns the current render state.
- `POST /api/action`: applies one UI action and returns the new render state.

## Frontend Responsibilities

`app.js` should stay deliberately small:

- Render the state returned by `/api/state` and `/api/action`.
- Send clicked command payloads back to the backend.
- Avoid `localStorage` or any other browser-side game persistence.
- Avoid hardcoded training command lists, kojo text, or command effects.
- Avoid hardcoded character attribute dictionaries or game-specific attribute
  section definitions.

If the UI needs more data, add it to the backend response instead of inventing it
in the frontend.

## Backend Responsibilities

`server.py` contains two major backend pieces:

- `GameSession`: high-level browser-session state and view-model generation.
- `ErbCommandBridge`: a small real ERB runtime used by the prototype.

`GameSession` is responsible for:

- Maintaining the current screen, selected target, recent message lines, day,
  time, money, and prototype characters.
- Dispatching browser actions such as `new-game`, `select-target`, and
  `train-command`.
- Building UI view models for title, shop, target selection, training, and
  ability screens.
- Applying the numeric results produced by real ERB runtime variables to the
  in-memory character state.

`ErbCommandBridge` is responsible for:

- Loading `ERB/**/*.ERB`.
- Indexing command files named like `COMF<number>_*.ERB`.
- Parsing ERB function headers, including headers with argument declarations
  such as `@GET_KOJO_NUM(ARG = -1)`.
- Executing the subset of ERB currently needed by the prototype.
- Stopping/reporting when a required ERB feature is not supported yet.

## Data Sources

Current CSV name tables are loaded on the backend:

- `CSV/Train.csv`: training command labels.
- `CSV/Abl.csv`: ability names.
- `CSV/exp.csv`: experience names.
- `CSV/Mark.csv`: mark names.
- `CSV/Palam.csv`: parameter names.
- `CSV/source.csv`: source names.
- `CSV/Talent.csv`: talent names.

Current character state is loaded from real character CSV files:

- `CSV/Chara/Chara0.csv`: player/master character.
- `CSV/Chara/Chara1.csv`: selectable target `女战士`.
- `CSV/Chara/Chara31.csv`: selectable target `琼`.

`load_character_csv()` currently reads `番号`, `名前`, `呼び名`, `基礎`,
`素質`, `フラグ` / `CFLAG`, `ABL`, `経験` / `EXP`, `JUEL`, and `CSTR`. It
stores the source path on `CharacterState` so the ability screen can show where
the currently rendered character came from.

Important ERB files currently involved in the training flow:

- `ERB/COMF0_愛撫.ERB`: real command implementation for `爱抚[0]`.
- `ERB/EVENT_TRAIN_MESSAGE_B.ERB`: generic command execution text.
- `ERB/SYSTEM_SOURCE.ERB`: source-to-UP/DOWN settlement functions and the
  original full settlement flow.
- `ERB/EVENT_K.ERB`: kojo dispatcher.
- `ERB/EVENT_K0_慈愛.ERB`: K0/Ci-ai kojo implementation used by the current
  minimal prototype target.

## Current ERB Runtime Scope

The prototype runtime currently supports enough ERB to run the `爱抚[0]` command,
generic command text, part of source settlement, and the K0 command kojo hook.

Currently supported or partially supported semantics include:

- `CALL`
- `CALLFORM`
- `TRYCALLFORM`
- `IF`
- `ELSEIF`
- `ELSE`
- `ENDIF`
- `SIF`
- `FOR`
- `NEXT`
- `RETURN`
- `RETURNF`
- `PRINT`
- `PRINTS`
- `PRINTL`
- `PRINTFORM`
- `PRINTFORML`
- `PRINTFORMW`
- `PRINTV`
- `WAIT`
- `RESETCOLOR`
- `CUSTOMDRAWLINE`
- `DRAWLINE`
- `TIMES`
- scalar assignments
- array/character assignments
- compound assignments such as `+=`, `-=`, `*=`, `/=`, `|=`, and `&=`

Currently important runtime variable families include:

- Global-ish arrays: `DOWN`, `EX`, `EX_FLAG`, `FLAG`, `GOTJUEL`, `GLOBAL`,
  `JUEL`, `LOCAL`, `LOCALS`, `NO`, `PALAMLV`, `RELATION`, `SAVESTR`, `TFLAG`,
  `UP`.
- Character arrays: `ABL`, `TALENT`, `CFLAG`, `MARK`, `BASE`, `MAXBASE`,
  `EXP`, `SOURCE`, `PALAM`, `TEQUIP`, `STAIN`.
- Special target-scoped array: `LOSEBASE`.

Known missing or incomplete ERB semantics include:

- `REPEAT` / `REND`
- `CONTINUE`
- `BREAK`
- full function argument lists beyond the current `ARG` handling
- proper scoped local stacks for `LOCAL`
- full `CALL` argument passing
- full `CALLFORM` / `TRYCALLFORM` compatibility
- full string functions such as `UNICODE(...)`, `SELF_CALL(...)`,
  `STRLENSU(...)`, and related helpers
- full character creation and save/load state
- full `SYSTEM_SOURCE.ERB @SOURCE_CHECK` execution

## Training Command Flow

For the current `爱抚[0]` smoke path:

1. The frontend posts `{"action": "train-command", "command": 0}`.
2. `GameSession._run_train_command(0)` resets the ERB bridge with the current
   character list and target index.
3. `ErbCommandBridge.execute_command(0)` finds `ERB/COMF0_愛撫.ERB`.
4. The bridge calls `COM0`.
5. `COM0` produces real command output and source values through ERB.
6. If the command returns non-zero, `execute_command()` calls
   `KOJO_MESSAGE_COM`.
7. `GameSession` then calls `run_source_settlement()` to execute the currently
   supported real source-settlement helper chain.
8. If source settlement succeeds, `GameSession` calls
   `KOJO_MESSAGE_PALAMCNG` while `UP` still contains the current command's
   parameter changes.
9. If parameter-change kojo succeeds, `GameSession` calls the real
   `MARK_GOT_CHECK`.
10. If `MARK_GOT_CHECK` sets `TFLAG:21..24`, `GameSession` calls
   `KOJO_MESSAGE_MARKCNG`.
11. `GameSession._apply_train_result()` applies `LOSEBASE`, `UP`, `DOWN`,
   `SOURCE`, and `EXP` values to the target and renders the result text.

Verified current output for `爱抚[0]` with `CSV/Chara/Chara31.csv` selected as
the target includes real kojo and real settlement:

```text
[0] 爱抚
爱抚
「你的爱是虚假的」
琼紧锁眉头、蜷缩着身体………
体力... -5
气力... -50
阴核快感 +1
乳房快感 +2
百合经验 +5
阴核 0 +1 = 1
乳房 0 +2 = 2
欲情 0 +2 = 2
习得 0 +27 = 27
耻情 0 +200 = 200
反感 0 +45 = 45
```

## Kojo Flow

Kojo means character/personality-specific dialogue and reactions. It should come
from ERB kojo hooks, not from frontend text.

Current command kojo flow:

1. `ErbCommandBridge.execute_command()` calls `COM<number>`.
2. If the command returns non-zero, the bridge calls `KOJO_MESSAGE_COM`.
3. `ERB/EVENT_K.ERB @KOJO_MESSAGE_COM` checks `FLAG:7`.
4. It calls `GET_KOJO_NUM()`.
5. `GET_KOJO_NUM()` scans `TALENT:ARG:160..179`.
6. For `CSV/Chara/Chara31.csv`, `素質,160;慈爱` sets `TALENT:160 = 1`, so
   the kojo number becomes `100`.
7. `TRYCALLFORM KOJO_MESSAGE_COM_{LOCAL - 100}` resolves to
   `KOJO_MESSAGE_COM_0`.
8. `ERB/EVENT_K0_慈愛.ERB @KOJO_MESSAGE_COM_0` emits the visible text.

Current visible K0 first-time `爱抚[0]` kojo comes from
`ERB/EVENT_K0_慈愛.ERB`:

```text
「你的爱是虚假的」
琼紧锁眉头、蜷缩着身体………
```

The current K0 kojo route comes from the selected character's real CSV talent
data plus real `EVENT_K.ERB`/`EVENT_K0_慈愛.ERB` dispatch. It is not frontend
text and is not a backend fallback table.

Other real kojo dispatcher hooks in `ERB/EVENT_K.ERB` that still need fuller
integration:

- `KOJO_EVENT_COM`: command-end event kojo.
- `SELF_KOJO`: event-start kojo.

Currently integrated kojo hooks:

- `KOJO_MESSAGE_COM`: command execution kojo.
- `KOJO_MESSAGE_PALAMCNG`: parameter-change kojo. For current `爱抚[0]`, this
  executes successfully but emits no extra text because the real `UP` values do
  not cross the K0 thresholds such as `PALAMLV:2`.
- `KOJO_MESSAGE_MARKCNG`: mark-change kojo. This is called only when the real
  `MARK_GOT_CHECK` sets one of `TFLAG:21`, `TFLAG:22`, `TFLAG:23`, or
  `TFLAG:24`.

Current mark flow:

1. Source settlement computes `UP` values from real ERB helper functions.
2. `MARK_GOT_CHECK` in `ERB/SYSTEM_SOURCE_SUB1.ERB` checks `UP`, `MARK`, and
   `TFLAG` values.
3. If a mark is acquired, `MARK_GOT_CHECK` updates `MARK` and sets a
   `TFLAG:21..24` value.
4. Only then does the prototype call `KOJO_MESSAGE_MARKCNG`.

For current `爱抚[0]`, `MARK_GOT_CHECK` runs without unsupported statements but
does not set a mark because the real values are below mark thresholds.

## Character CSV Loading

`GameSession._new_characters()` currently builds the browser prototype roster by
calling `load_character_csv()` for:

- `Chara0.csv`: `番号,0`, `名前,你`, `呼び名,你`.
- `Chara1.csv`: `番号,1`, `名前,女战士`, `呼び名,女战士`.
- `Chara31.csv`: `番号,31`, `名前,琼`, `呼び名,琼`.

The target-selection screen is generated from `self.characters` and skips only
index `0` (the master/player). It does not contain a frontend or backend
fallback list of visible target names.

Currently parsed character arrays:

- `BASE` / `MAXBASE`: from `基礎`.
- `TALENT`: from `素質`, including comment-bearing values such as
  `160;慈爱`.
- `CFLAG`: from `フラグ`.
- `ABL`: from `ABL`.

Full `CHARA_MAKE.ERB` and save/load state are still not implemented. Until
those exist, this prototype uses static real `CSV/Chara/*.csv` files rather than
invented character data.

## Ability Display API

The ability screen is now rendered as an Emuera-style paged text screen rather
than a browser-native attribute card. The frontend still does not define game
attribute names, sections, values, command lists, or fallbacks.

The backend response for `mode: "ability"` contains:

- `abilityText`: the full preformatted text page generated by `GameSession`.
- `abilityPage`: current page number, matching the original
  `CHARA_INFO_SHOW.ERB @SHOW_CHARA_INFO(ARG, ARG:1)` page model.
- `abilityCommands`: backend-built bottom command rows such as `[101] 前页`,
  `[100] 返回`, and `[102] 后页`.
- `characterDetail`: a compatibility/debug object. It is no longer the primary
  ability layout.

Current page mapping follows `ERB/CHARA_INFO_SHOW.ERB`:

- Page `0` / `CASE 0`: header, basic block, talent groups, abilities, marks.
- Page `1` / `CASE 1`: marks and experience/level information.
- Page `2` / `CASE 2`: equipment and appearance/background text.
- Page `3` / `CASE 3`: talent acquisition conditions. This page currently
  parses real `ERB/CHARA_INFO_SHOW_TALENT.ERB @SHOW_TALENT_CONDITION` rows with
  a backend-only minimal renderer instead of inventing conditions in the
  frontend.

Current ability display data sources:

- Header/base stats: `CharacterState`, `BASE`, `MAXBASE`, and `CFLAG`.
- Body metrics (`年龄`, `身高`, `体重`, `B/W/H`): generated on the backend from
  the real `ERB/CHARA_BODY.ERB` / `ERB/CHARA_BODY2.ERB` formulas when the
  static character CSV does not already provide `CFLAG:451..457`.
- Bust display details such as cup size are derived from the same real body
  generation path plus the original `UNDER_BUST` / `CUP_SIZE` logic, not from
  frontend lookup tables.
- Talent groups: `TALENT` loaded from `CSV/Chara/*.csv`, names from
  `CSV/Talent.csv`, grouped according to the broad structure of
  `SHOW_TALENT`.
- Ability rows: `ABL`, names from `CSV/Abl.csv`.
- Marks: `MARK`, names and ordering from the original mark display.
- Experience rows: `EXP` / `経験`, names from `CSV/exp.csv`.
- Point-based checks: `JUEL`, loaded from real character CSV when present.
- Experience-level thresholds: `EXPLV`, loaded from real `CSV/_replace.csv`
  initial values when present and otherwise falling back to Emuera defaults.
- Appearance/background: `TALENT:300..317` from `CSV/Chara/*.csv`, mapped by
  parsing simple `SELECTCASE` tables from `ERB/LOOK.ERB @GET_LOOK_INFO` and
  `@LOVE_LIKE_BASE`. The frontend does not contain appearance dictionaries.

Current page `3` talent-condition integration:

- `server.py` loads raw ERB lines from
  `ERB/CHARA_INFO_SHOW_TALENT.ERB @SHOW_TALENT_CONDITION`.
- `TalentConditionRenderer` linearly evaluates the currently needed subset of
  that file for display purposes.
- The renderer currently supports the common helper calls used by the visible
  condition list:
  `STC_LAB_TAL`, `STC_PRINTC`, `STC_SAY_ABL`, `STC_SAY_EXP`,
  `STC_SAY_MARK`, `STC_SAYNO_MARK`, `STC_SAY_TAL`, `STC_SAYNO_TAL`,
  `STC_SAYSUM_EXP`, `STC_SAY_ABCV`, and `STC_SEIIN_CHECK`.
- The renderer also evaluates simple `IF` / `ELSEIF` / `ELSE` / `ENDIF`,
  `SIF`, and scalar / array assignments that those condition blocks use.
- Unsupported expressions are surfaced on the page as partial integration
  notes. They are not silently replaced with invented requirements.

Fields produced by full character creation or save state but absent from the
static character CSV, such as age, height, weight, and B/W/H for `Chara31.csv`,
are now generated from the real body-generation ERB path on the backend. If a
field still remains unavailable after that path, it should stay explicit rather
than be guessed in the frontend.

The real talent-condition page lives in
`ERB/CHARA_INFO_SHOW_TALENT.ERB @SHOW_TALENT_CONDITION`. The current browser
prototype does not execute that function through the full ERB runtime yet, but
it now renders the supported `STC_*` condition rows from that real source on
the backend and explicitly surfaces unresolved pieces instead of fabricating
them.

## Verification Commands

Compile the backend:

```bash
python -m py_compile web-prototype/server.py
```

Smoke the browser API by starting the server and exercising:

```text
POST /api/action {"action":"new-game"}
POST /api/action {"action":"go-target-select"}
POST /api/action {"action":"select-target","target":2}
POST /api/action {"action":"train-command","command":0}
```

Expected response text should contain:

```text
「你的爱是虚假的」
琼紧锁眉头、蜷缩着身体………
```

After `show-characters`, the ability response should include metadata similar
to:

```text
编号 31
呼名 琼
来源 CSV/Chara/Chara31.csv
```

## Near-Term Extension Plan

The next safest extensions are:

- Parse more `CSV/Chara/*.csv` fields that the original game surfaces in
  `CHARA_INFO_SHOW.ERB`.
- Connect full character creation/state through `CHARA_MAKE.ERB` and save/load
  data.
- Gradually execute more of `SYSTEM_SOURCE.ERB @SOURCE_CHECK` directly instead
  of manually selecting helper functions.
- Keep every newly supported ERB statement small, tested, and documented here.
