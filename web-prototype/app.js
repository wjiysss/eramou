const ui = {
  debugLine: document.querySelector("#debug-line"),
  screenLabel: document.querySelector("#screen-label"),
  dateStatus: document.querySelector("#date-status"),
  targetInfo: document.querySelector("#target-info"),
  assistantInfo: document.querySelector("#assistant-info"),
  itemInfo: document.querySelector("#item-info"),
  trapInfo: document.querySelector("#trap-info"),
  regionInfo: document.querySelector("#region-info"),
  dailyInfo: document.querySelector("#daily-info"),
  commandGrid: document.querySelector("#command-grid"),
  messageOutput: document.querySelector("#message-output"),
  inputPrompt: document.querySelector("#input-prompt"),
};

async function apiAction(payload) {
  const response = await fetch("/api/action", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  return response.json();
}

async function apiState() {
  const response = await fetch("/api/state", { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  return response.json();
}

function renderView(view) {
  document.body.dataset.mode = view.mode || "normal";
  ui.inputPrompt.textContent = "_";
  clearChrome();

  if (view.mode === "training") {
    ui.commandGrid.innerHTML = `
      <div class="training-room">
        <pre class="training-pre">${escapeHtml(view.trainingText || "")}</pre>
        <div class="train-command-overlay">${renderCommandRows(view.trainingCommands || [], true)}</div>
      </div>
    `;
    return;
  }

  if (view.mode === "ability") {
    ui.commandGrid.innerHTML = `
      <pre class="ability-pre ability-pre--full">${escapeHtml(view.abilityText || "")}</pre>
      <div class="ability-actions">${renderAbilityCommandRows(view.abilityCommands || [])}</div>
    `;
    return;
  }

  ui.debugLine.textContent = view.debugLine || "";
  ui.screenLabel.textContent = view.screenLabel || "";
  ui.dateStatus.textContent = view.dateStatus || "";
  ui.targetInfo.textContent = view.targetInfo || "";
  ui.assistantInfo.textContent = view.assistantInfo || "";
  ui.itemInfo.textContent = view.itemInfo || "";
  ui.trapInfo.textContent = view.trapInfo || "";
  ui.regionInfo.textContent = view.regionInfo || "";
  ui.dailyInfo.textContent = view.dailyInfo || "";
  renderCommands(view.commands || []);
  renderMessages(view.messages || []);
}

function clearChrome() {
  ui.debugLine.textContent = "";
  ui.screenLabel.textContent = "";
  ui.dateStatus.textContent = "";
  ui.targetInfo.textContent = "";
  ui.assistantInfo.textContent = "";
  ui.itemInfo.textContent = "";
  ui.trapInfo.textContent = "";
  ui.regionInfo.textContent = "";
  ui.dailyInfo.textContent = "";
  ui.commandGrid.innerHTML = "";
  ui.messageOutput.innerHTML = "";
}

function renderCommands(columns) {
  ui.commandGrid.innerHTML = columns
    .map(
      (column) => `
        <div class="command-column">
          ${column.map((item) => renderCommand(item, false)).join("")}
        </div>
      `,
    )
    .join("");
}

function renderCommandRows(rows, inline) {
  return rows
    .map(
      (row) => `
        <div class="${inline ? "train-command-row" : "command-column"}">
          ${row.map((item) => renderCommand(item, inline)).join("")}
        </div>
      `,
    )
    .join("");
}

function renderAbilityCommandRows(rows) {
  return rows
    .map(
      (row) => `
        <div class="ability-command-row">
          ${row.map((item) => renderCommand(item, true)).join("")}
        </div>
      `,
    )
    .join("");
}

function renderCommand(item, inline) {
  if (!item || !item.action || !item.name) {
    if (inline) {
      return "<span></span>";
    }
    return `
      <div class="command-button command-button--empty" aria-hidden="true">
        <span class="command-code">[${escapeHtml(item?.code || "")}]</span>
        <span class="command-name"></span>
      </div>
    `;
  }

  const extra = item.extra || {};
  const extraAttrs = Object.entries(extra)
    .map(([key, value]) => `data-${key}="${escapeAttr(value)}"`)
    .join(" ");
  const tone = extra.tone ? ` command-tone-${extra.tone}` : "";

  if (inline) {
    const label =
      extra.layout === "code-first"
        ? `[${escapeHtml(item.code)}] ${escapeHtml(item.name)}`
        : `${escapeHtml(item.name)}[${escapeHtml(formatTrainingCode(item.code))}]`;
    return `
      <button class="inline-command${tone}" type="button" data-action="${escapeAttr(item.action)}" ${extraAttrs}>
        ${label}
      </button>
    `;
  }

  return `
    <button class="command-button" type="button" data-action="${escapeAttr(item.action)}" ${extraAttrs}>
      <span class="command-code">[${escapeHtml(item.code)}]</span>
      <span class="command-name">${escapeHtml(item.name)}</span>
    </button>
  `;
}

function renderMessages(lines) {
  ui.messageOutput.innerHTML = lines
    .slice(0, 8)
    .map((line) => `<div class="message-line">${escapeHtml(line)}</div>`)
    .join("");
}

function renderCharacterDetail(detail) {
  if (!detail) {
    return "";
  }

  return `
    <section class="character-detail" aria-label="Character detail">
      <header class="character-detail__header">
        <span>【${escapeHtml(detail.name || "")}】</span>
        <span>${escapeHtml(detail.posture || "")}</span>
      </header>
      <div class="character-detail__meta">
        ${(detail.metadata || []).map(renderMetadataItem).join("")}
      </div>
      <div class="character-detail__base">
        ${(detail.base || []).map(renderBaseRow).join("")}
      </div>
      <div class="character-detail__grid">
        ${(detail.sections || []).map(renderDetailSection).join("")}
      </div>
    </section>
  `;
}

function renderMetadataItem(item) {
  return `
    <span class="detail-meta-item">
      <span class="detail-meta-label">${escapeHtml(item.label)}</span>
      <span class="detail-meta-value">${escapeHtml(item.value)}</span>
    </span>
  `;
}

function renderBaseRow(row) {
  return `
    <div class="detail-base-row">
      <span class="detail-name">${escapeHtml(row.name)}</span>
      <span class="detail-bar">${escapeHtml(row.bar)}</span>
      <span class="detail-value">${escapeHtml(row.value)}/${escapeHtml(row.max)}</span>
    </div>
  `;
}

function renderDetailSection(section) {
  const title = section?.title || "";
  const variant = section?.variant || "pairs";
  const safeRows = section?.rows || [];
  return `
    <section class="detail-section detail-section--${escapeAttr(variant)}">
      <h3>${escapeHtml(title)}</h3>
      <div class="detail-section__body">
        ${safeRows.length ? safeRows.map((row) => renderDetailRow(row, variant)).join("") : `<span class="detail-empty">无</span>`}
      </div>
    </section>
  `;
}

function renderDetailRow(row, variant) {
  if (variant === "chips") {
    return `<span class="detail-chip">[${escapeHtml(row.name)}]</span>`;
  }
  return `
    <div class="detail-row">
      <span class="detail-name">${escapeHtml(row.name)}</span>
      <span class="detail-value">${escapeHtml(row.value)}</span>
    </div>
  `;
}

function formatTrainingCode(code) {
  return String(code).padStart(3, " ");
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function escapeAttr(value) {
  return escapeHtml(value).replace(/`/g, "&#096;");
}

document.addEventListener("click", async (event) => {
  const target = event.target.closest("[data-action]");
  if (!target) {
    return;
  }

  const payload = { action: target.dataset.action };
  for (const [key, value] of Object.entries(target.dataset)) {
    if (key !== "action" && key !== "tone") {
      payload[key] = numericIfPossible(value);
    }
  }

  try {
    renderView(await apiAction(payload));
  } catch (error) {
    renderView({
      mode: "normal",
      debugLine: "[ERROR] API",
      messages: [`后端请求失败：${error.message}`],
      commands: [],
    });
  }
});

function numericIfPossible(value) {
  if (/^-?\d+$/.test(value)) {
    return Number(value);
  }
  return value;
}

async function init() {
  try {
    renderView(await apiState());
  } catch (error) {
    renderView({
      mode: "normal",
      debugLine: "[ERROR] API",
      messages: [`后端状态读取失败：${error.message}`],
      commands: [],
    });
  }
}

init();
