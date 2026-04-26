import { useMemo, useState } from "react";
import {
  AlertCircle,
  ArrowRight,
  BookOpenText,
  CheckCircle2,
  Clock3,
  History,
  Layers3,
  Lightbulb,
  Search,
  Sparkles,
} from "lucide-react";

function MasterBox({ title, subtitle, children, className = "" }) {
  return (
    <section className={`master-box flex flex-col ${className}`}>
      <header className="master-box__header" style={{ display: title || subtitle ? "flex" : "none" }}>
        <div>
          {title ? <h2 className="master-box__title">{title}</h2> : null}
          {subtitle ? <p className="master-box__subtitle">{subtitle}</p> : null}
        </div>
      </header>
      <div className="master-box__content flex-1 h-full">{children}</div>
    </section>
  );
}



function buildRegexHighlight(text, phrases) {
  const candidates = [...new Set(phrases.map((item) => String(item || "").trim()).filter(Boolean))].sort(
    (left, right) => right.length - left.length
  );

  if (!candidates.length) {
    return [{ text, tone: "plain" }];
  }

  const pattern = new RegExp(
    `(${candidates
      .map((candidate) => {
        const escaped = candidate.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
        const startBoundary = /^\w/.test(candidate) ? "\\b" : "";
        const endBoundary = /\w$/.test(candidate) ? "\\b" : "";
        return `${startBoundary}${escaped}${endBoundary}`;
      })
      .join("|")})`,
    "gi"
  );

  return text
    .split(pattern)
    .filter(Boolean)
    .map((part) => {
      const lowered = part.toLowerCase();
      const matched = candidates.find((candidate) => candidate.toLowerCase() === lowered);
      if (!matched) {
        return { text: part, tone: "plain" };
      }

      return { text: part, tone: "accent" };
    });
}

function escapeRegExp(value) {
  return String(value || "").replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function replaceTokenOnce(text, token, replacement) {
  if (!text || !token || !replacement) {
    return text;
  }

  const pattern = new RegExp(`\\b${escapeRegExp(token)}\\b`, "i");
  return text.replace(pattern, replacement);
}

function buildSpellingCommandSuggestions(result, issue, submittedInput) {
  const originalParagraph =
    result?.data?.original_text || String(submittedInput || "").replace(/^check\s+grammar\s+/i, "").trim();
  const alternatives = issue?.alternatives?.length ? issue.alternatives : [issue?.suggestion].filter(Boolean);

  return alternatives
    .map((candidate) => {
      const updatedParagraph = replaceTokenOnce(originalParagraph, issue?.token, candidate);
      return updatedParagraph && updatedParagraph !== originalParagraph ? `check grammar ${updatedParagraph}` : null;
    })
    .filter(Boolean);
}

function HighlightedParagraph({ text, phrases, tone }) {
  const segments = useMemo(() => buildRegexHighlight(text, phrases), [text, phrases]);

  return (
    <div className={`highlighted-paragraph highlighted-paragraph--${tone}`}>
      {segments.map((segment, index) => (
        <span
          key={`${segment.text}-${index}`}
          className={segment.tone === "accent" ? `highlight highlight--${tone}` : ""}
        >
          {segment.text}
        </span>
      ))}
    </div>
  );
}

function MetricCard({ label, value, icon: Icon, active = false, onClick }) {
  return (
    <button
      type="button"
      className={`metric-card ${active ? "metric-card--active" : ""}`}
      onClick={onClick}
    >
      <span className="metric-card__icon">{Icon ? <Icon size={18} /> : null}</span>
      <span className="metric-card__label">{label}</span>
      <strong className="metric-card__value">{value}</strong>
    </button>
  );
}

function ReviewWorkflowBox({ result, submittedInput, onApplySuggestion }) {
  const data = result?.data || {};
  const [showAllRewrites, setShowAllRewrites] = useState(false);

  const originalPhrases = [
    ...(data.spelling_issues || []).map((issue) => issue.token),
    ...(data.grammar_errors || []).map((issue) => issue.evidence || issue.token),
    ...(data.semantic_warnings || []).map((issue) => issue.evidence || issue.token),
  ].filter(Boolean);

  const correctedPhrases = [
    ...(data.corrections || []).map((entry) => entry.corrected),
    ...(data.grammar_errors || []).map((issue) => issue.suggestion),
  ].filter(Boolean);

  const topReasons = [
    ...(data.grammar_errors || []).slice(0, 4).map((issue) => ({
      tone: "grammar",
      text: issue.message,
    })),
    ...(data.semantic_warnings || []).slice(0, 4).map((issue) => ({
      tone: "semantic",
      text: issue.replacement || issue.suggestion || issue.message,
    })),
  ].slice(0, 8);

  const rewrites = data.corrections || [];
  const visibleRewrites = showAllRewrites ? rewrites : rewrites.slice(0, 6);
  const hasIssues =
    (data.spelling_issues || []).length ||
    (data.grammar_errors || []).length ||
    (data.semantic_warnings || []).length;

  return (
    <MasterBox>
      <div className="review-stack">
        <div className={`review-block ${!hasIssues ? "review-block--clean" : ""}`}>
          <div className="review-block__header">
            <div>
              <h3>{hasIssues ? "Analysis" : "No issues found"}</h3>
            </div>
            {!hasIssues ? (
              <span className="success-pill">
                <CheckCircle2 size={16} />
                Clean paragraph
              </span>
            ) : null}
          </div>

          {hasIssues ? (
            <>
              <HighlightedParagraph text={data.original_text || ""} phrases={originalPhrases} tone="issue" />
              <div className="review-legend">
                <span className="legend-chip legend-chip--issue">Red = issue to review</span>
                <span className="legend-chip legend-chip--semantic">Amber = semantic warning</span>
              </div>
              <div className="error-card-grid">
                {(data.spelling_issues || []).map((issue) => (
                  <article key={`spell-${issue.position}-${issue.token}`} className="error-card error-card--spelling">
                    <span className="error-card__badge">Spelling:</span>
                    <strong>
                      {issue.token} <ArrowRight size={14} /> {issue.suggestion}
                    </strong>
                    {issue.alternatives?.length ? (
                      <div className="chip-row" style={{ marginTop: "0.75rem" }}>
                        {buildSpellingCommandSuggestions(result, issue, submittedInput).map((command) => {
                          const candidate = command.replace(/^check\s+grammar\s+/i, "");
                          return (
                            <button
                              type="button"
                              key={command}
                              className="lookup-chip lookup-chip--soft"
                              onClick={() => onApplySuggestion?.(command)}
                            >
                              Try: {candidate}
                            </button>
                          );
                        })}
                      </div>
                    ) : null}
                  </article>
                ))}
                {(data.grammar_errors || []).map((issue, index) => (
                  <article key={`grammar-${index}-${issue.rule_id}`} className="error-card">
                    <span className="error-card__badge">{issue.category}:</span>
                    <strong>{issue.message}</strong>
                    {issue.suggestion ? <p>Suggestion: {issue.suggestion}</p> : null}
                  </article>
                ))}
                {(data.semantic_warnings || []).map((issue, index) => (
                  <article key={`semantic-${index}-${issue.rule_id}`} className="error-card error-card--semantic">
                    <span className="error-card__badge">Semantic:</span>
                    <strong>{issue.message}</strong>
                    {issue.suggestion ? <p>{issue.suggestion}</p> : null}
                  </article>
                ))}
              </div>
            </>
          ) : (
            <div className="clean-state">
              <CheckCircle2 size={22} />
              <p>No issues found. The paragraph already looks consistent under the current rule set.</p>
            </div>
          )}
        </div>

        <div className="review-block">
          <div className="review-block__header">
            <div>
              <h3>Final Result</h3>
            </div>
            <span className="success-pill success-pill--soft">Green = corrected rewrite</span>
          </div>

          <HighlightedParagraph
            text={data.corrected_text || data.normalized_text || ""}
            phrases={correctedPhrases}
            tone="correction"
          />
        </div>

        <details className="review-block review-block--details">
          <summary>
            <span>Why did we suggest this?</span>
            <Lightbulb size={16} />
          </summary>
          <div className="details-grid">
            <div className="details-section">
              <h4>Key Reasons</h4>
              <ul className="stack-list">
                {topReasons.length ? (
                  topReasons.map((reason, index) => (
                    <li key={`${reason.text}-${index}`} className={`stack-list__item stack-list__item--${reason.tone}`}>
                      {reason.text}
                    </li>
                  ))
                ) : (
                  <li className="stack-list__item">No rewrite explanation was needed for this run.</li>
                )}
              </ul>
            </div>

            <div className="details-section">
              <h4>Key Rewrites</h4>
              <ul className="stack-list">
                {visibleRewrites.length ? (
                  visibleRewrites.map((entry, index) => (
                    <li key={`${entry.original}-${entry.corrected}-${index}`} className="stack-list__item">
                      <strong>
                        {entry.original} <ArrowRight size={14} /> {entry.corrected}
                      </strong>
                      <span className="stack-list__meta">[{entry.kind}]</span>
                      {entry.reason ? <p>{entry.reason}</p> : null}
                    </li>
                  ))
                ) : (
                  <li className="stack-list__item">No deterministic rewrite was applied.</li>
                )}
              </ul>
              {rewrites.length > 6 ? (
                <button
                  type="button"
                  className="show-more-button"
                  onClick={() => setShowAllRewrites((current) => !current)}
                >
                  {showAllRewrites ? "Show fewer rewrites" : `+ ${rewrites.length - 6} more rewrite(s)`}
                </button>
              ) : null}
            </div>
          </div>
        </details>
      </div>
    </MasterBox>
  );
}

function UtilityLookupBox({ result, submittedInput, onApplySuggestion }) {
  const data = result?.data || {};
  const command = result?.command || "";
  const lookupWord = submittedInput.split(/\s+/).slice(1).join(" ") || "Lookup";

  return (
    <MasterBox title={`Lookup | ${lookupWord}`}>
      <div className="utility-box">
        {command === "verb" ? (
          <div className="verb-grid">
            {[
              { label: "V1", value: data.forms?.base || data.v1 || "—" },
              { label: "V2", value: data.forms?.past || data.v2 || "—" },
              { label: "V3", value: data.forms?.participle || data.v3 || "—" },
            ].map((entry) => (
              <article key={entry.label} className="verb-cell">
                <span>{entry.label}</span>
                <strong>{entry.value}</strong>
              </article>
            ))}
          </div>
        ) : null}

        {command === "synonym" ? (
          <div className="chip-row">
            {(data.synonyms || []).map((item) => (
              <span key={item} className="lookup-chip">
                {item}
              </span>
            ))}
          </div>
        ) : null}

        {command === "spell" ? (
          <div className="spell-box">
            {data.is_correct ? (
              <div className="clean-state">
                <CheckCircle2 size={20} />
                <p>
                  <strong>{data.closest_match || lookupWord}</strong> is already spelled correctly.
                </p>
              </div>
            ) : (
              <>
                <p className="utility-helper">Closest dictionary match</p>
                <button
                  type="button"
                  className="suggestion-cta"
                  onClick={() => onApplySuggestion?.(`spell ${data.closest_match}`)}
                >
                  Did you mean: {data.closest_match}?
                </button>
              </>
            )}
          </div>
        ) : null}

        {!result.success && result.suggestions?.length > 0 && (
          <div className="spell-box" style={{ marginTop: "1rem", paddingTop: "1rem", borderTop: "1px dashed rgba(25, 26, 35, 0.1)" }}>
            <p className="utility-helper">Did you mean one of these?</p>
            <div className="chip-row">
              {result.suggestions.map((suggestion) => (
                <button
                  key={suggestion}
                  type="button"
                  className="lookup-chip lookup-chip--button"
                  onClick={() => onApplySuggestion?.(suggestion)}
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
    </MasterBox>
  );
}

function TokenInspectorBox({ result, submittedInput }) {
  const data = result?.data || {};
  const tokens = data.tokens || [];

  return (
    <MasterBox
      title="Lexer / Parser Inspector"
      subtitle="ANTLR token stream for the DSL snippet you asked to inspect."
    >
      <div className="dashboard-list">
        <article className="dashboard-list__item">
          <div className="dashboard-list__heading">
            <h3>Inspected snippet</h3>
            <span>{data.parsable ? "Parses successfully" : "Lexer-only preview"}</span>
          </div>
          <div className="bad-input-box" style={{ marginTop: "0.5rem", padding: "0.5rem 0.8rem" }}>
            <code>{data.source_text || submittedInput.replace(/^show\s+tokens\s+/i, "")}</code>
          </div>
          {data.command_type ? <p style={{ marginTop: "0.75rem" }}>Parsed node: {data.command_type}</p> : null}
          {data.parse_error ? <p style={{ marginTop: "0.75rem" }}>Parse note: {data.parse_error}</p> : null}
        </article>

        {tokens.map((token) => (
          <article key={`${token.index}-${token.type}-${token.column}`} className="dashboard-list__item">
            <div className="dashboard-list__heading">
              <h3>
                {token.index}. {token.type}
              </h3>
              <span>
                line {token.line}, col {token.column}
              </span>
            </div>
            <div className="bad-input-box" style={{ marginTop: "0.5rem", padding: "0.5rem 0.8rem" }}>
              <code>{token.lexeme}</code>
            </div>
          </article>
        ))}
      </div>
    </MasterBox>
  );
}

function DashboardBox({ result, submittedInput, onApplySuggestion }) {
  const data = result?.data || {};
  const [filterKey, setFilterKey] = useState("overview");
  const [visibleCount, setVisibleCount] = useState(5);
  const isError = !result?.success;

  const metrics = [];
  const listItems = [];

  if (isError) {
    metrics.push({ key: "invalid", label: "Status", value: "Invalid", icon: AlertCircle });
    metrics.push({
      key: "suggestions",
      label: "Closest Matches",
      value: result?.suggestions?.length || 0,
      icon: Sparkles,
    });
    listItems.push({
      title: "Friendly Guidance",
      detail: result?.message || "The command could not be parsed.",
    });
  } else if (result.command === "revision plan") {
    const summary = data.summary || {};
    metrics.push({
      key: "submissions",
      label: "Checked Runs",
      value: summary.reviewed_submissions || 0,
      icon: ClipboardMetric,
    });
    metrics.push({
      key: "issues",
      label: "Tracked Issues",
      value: summary.tracked_issues || 0,
      icon: Layers3,
    });
    metrics.push({
      key: "focus",
      label: "Main Focus",
      value: summary.main_focus || "Balanced",
      icon: Lightbulb,
    });

    (data.recurring_patterns || []).forEach((pattern) => {
      listItems.push({
        title: `${pattern.title} (${pattern.count} time(s))`,
        detail: pattern.description,
        examples: pattern.examples || [],
      });
    });
  } else if (result.command === "history") {
    metrics.push({ key: "history", label: "Total Commands", value: data.total_commands || 0, icon: History });
    metrics.push({
      key: "checks",
      label: "Checked Paragraphs",
      value: (data.entries || []).filter((entry) => entry.command_name === "check grammar").length,
      icon: BookOpenText,
    });
    metrics.push({
      key: "latest",
      label: "Latest",
      value: data.entries?.[0]?.created_at ? new Date(data.entries[0].created_at).toLocaleDateString() : "—",
      icon: Clock3,
    });

    (data.entries || []).forEach((entry) => {
      listItems.push({
        title: entry.command_name,
        detail: entry.command,
        meta: entry.created_at ? new Date(entry.created_at).toLocaleString() : "",
        action: entry.command,
        examples: entry.message && (entry.command_name === "invalid" || !entry.success) ? [entry.message] : [],
      });
    });
  } else if (result.command === "help" || filterKey !== "overview") {
    const summary = data.pipeline_summary?.knowledge_stats || {};
    metrics.push({ key: "dictionary", label: "Dictionary", value: summary.dictionary_entries || 0, icon: BookOpenText });
    metrics.push({ key: "rules", label: "Pattern Rules", value: summary.phrase_index_entries || 0, icon: Layers3 });
    metrics.push({ key: "sources", label: "Imported Packs", value: summary.imported_sources || 0, icon: Sparkles });

    if (filterKey === "rules") {
      (data.coverage_matrix || []).forEach((entry) => {
        listItems.push({
          title: `${entry.units} | ${entry.label}`,
          detail: `${entry.support_level} support`,
          examples: entry.capabilities || [],
        });
      });
    } else {
      (data.commands || []).forEach((entry) => {
        listItems.push({
          title: entry.usage,
          detail: entry.description,
        });
      });
    }
  } else if (result.command === "reset history") {
    metrics.push({ key: "deleted", label: "Deleted Runs", value: data.deleted_runs || 0, icon: History });
    listItems.push({
      title: "History Reset",
      detail: result.message,
    });
  }

  const visibleItems = listItems.slice(0, visibleCount);

  return (
    <MasterBox title={isError ? "Unknown Command" : "Dashboard / Analytics"}>
      {isError ? (
        <div className="suggestion-card">
          <div className="suggestion-card__icon">
            <AlertCircle size={20} />
          </div>
          <div className="suggestion-card__copy">
            <h3>Did you mean this command?</h3>
            <p>The command prefix does not match a supported GrammarDSL form.</p>
            {submittedInput ? (
              <div className="bad-input-box">
                <span className="bad-input-box__label">Your Input</span>
                <code>{submittedInput}</code>
              </div>
            ) : null}
          </div>
          <div className="suggestion-card__actions">
            {(result.suggestions || []).slice(0, 2).map((suggestion) => (
              <button
                type="button"
                key={suggestion}
                className="suggestion-cta"
                onClick={() => onApplySuggestion?.(suggestion)}
              >
                {suggestion}
              </button>
            ))}
          </div>
        </div>
      ) : null}

      <div className="metrics-row">
        {metrics.map((metric) => (
          <MetricCard
            key={metric.key}
            label={metric.label}
            value={metric.value}
            icon={metric.icon}
            active={filterKey === metric.key}
            onClick={() => {
              if (result.command === "help") {
                setFilterKey(metric.key === "rules" ? "rules" : "overview");
              }
            }}
          />
        ))}
        {result.command === "help" ? (
          <MetricCard
            label="Rules"
            value={(data.coverage_matrix || []).length}
            icon={Search}
            active={filterKey === "rules"}
            onClick={() => setFilterKey((current) => (current === "rules" ? "overview" : "rules"))}
          />
        ) : null}
      </div>

      <div className="dashboard-list">
        {visibleItems.length ? (
          visibleItems.map((item, index) => (
            <article
              key={`${item.title}-${index}`}
              className={`dashboard-list__item ${item.action ? "cursor-pointer hover:border-black hover:shadow-sm" : ""}`}
              onClick={() => item.action && onApplySuggestion?.(item.action)}
              title={item.action ? "Click to run this command again" : undefined}
            >
              <div className="dashboard-list__heading">
                <h3 style={{ textTransform: "capitalize", fontWeight: "bold" }}>{item.title}</h3>
                {item.meta ? <span>{item.meta}</span> : null}
              </div>
              <div className="bad-input-box" style={{ marginTop: "0.5rem", padding: "0.5rem 0.8rem" }}>
                <code>{item.detail}</code>
              </div>
              {item.examples?.length ? (
                <div className="chip-row">
                  {item.examples.map((example) => (
                    <span key={example} className="lookup-chip lookup-chip--soft">
                      {example}
                    </span>
                  ))}
                </div>
              ) : null}
            </article>
          ))
        ) : (
          <article className="dashboard-list__item">
            <h3>No records yet</h3>
            <p>Run a few commands first, then this dashboard will fill in automatically.</p>
          </article>
        )}
      </div>

      {listItems.length > visibleCount ? (
        <button type="button" className="load-more-button" onClick={() => setVisibleCount((count) => count + 5)}>
          Load More
        </button>
      ) : null}
    </MasterBox>
  );
}

function ClipboardMetric() {
  return <BookOpenText size={18} />;
}

export default function ResultTemplates({ result, submittedInput, onApplySuggestion }) {
  if (!result) {
    return (
      <MasterBox>
        <div
          className="clean-state"
          style={{ minHeight: "400px", display: "flex", alignItems: "center", justifyContent: "center" }}
        >
          <p style={{ color: "rgba(25, 26, 35, 0.6)", fontSize: "1.2rem" }}>Run a command to see the output here.</p>
        </div>
      </MasterBox>
    );
  }

  const command = String(result.command || "").toLowerCase();

  if (command === "check grammar") {
    return <ReviewWorkflowBox result={result} submittedInput={submittedInput} onApplySuggestion={onApplySuggestion} />;
  }

  if (command === "show tokens") {
    return <TokenInspectorBox result={result} submittedInput={submittedInput} />;
  }

  if (["spell", "verb", "synonym"].includes(command)) {
    return <UtilityLookupBox result={result} submittedInput={submittedInput} onApplySuggestion={onApplySuggestion} />;
  }

  return <DashboardBox result={result} submittedInput={submittedInput} onApplySuggestion={onApplySuggestion} />;
}
