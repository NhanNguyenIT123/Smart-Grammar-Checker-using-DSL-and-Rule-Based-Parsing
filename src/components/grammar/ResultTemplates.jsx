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

function tokenizePhrase(value) {
  return String(value || "")
    .toLowerCase()
    .split(/[^a-z0-9']+/i)
    .map((token) => token.trim())
    .filter(Boolean);
}

function buildRegexHighlight(text, phrases) {
  const candidates = [...new Set(phrases.map((item) => String(item || "").trim()).filter(Boolean))]
    .sort((left, right) => right.length - left.length);

  if (!candidates.length) {
    return [{ text, tone: "plain" }];
  }

  const pattern = new RegExp(
    `(${candidates
      .map((candidate) => candidate.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"))
      .join("|")})`,
    "gi"
  );

  return text.split(pattern).filter(Boolean).map((part) => {
    const lowered = part.toLowerCase();
    const matched = candidates.find((candidate) => candidate.toLowerCase() === lowered);
    if (!matched) {
      return { text: part, tone: "plain" };
    }

    return { text: part, tone: "accent" };
  });
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

function ReviewWorkflowBox({ result, isExplain }) {
  const data = result?.data || {};
  const [showAllRewrites, setShowAllRewrites] = useState(false);

  const originalPhrases = [
    ...(data.spelling_issues || []).map((issue) => issue.token),
    ...(data.grammar_errors || []).flatMap((issue) => tokenizePhrase(issue.evidence || issue.message)),
    ...(data.semantic_warnings || []).flatMap((issue) => tokenizePhrase(issue.evidence || issue.message)),
  ];

  const correctedPhrases = [
    ...(data.corrections || []).flatMap((entry) => tokenizePhrase(entry.corrected)),
    ...(data.grammar_errors || []).flatMap((issue) => tokenizePhrase(issue.suggestion)),
  ];

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
              <HighlightedParagraph
                text={data.original_text || ""}
                phrases={originalPhrases}
                tone="issue"
              />
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
                  {showAllRewrites
                    ? "Show fewer rewrites"
                    : `+ ${rewrites.length - 6} more rewrite(s)`}
                </button>
              ) : null}
            </div>

            {isExplain ? (
              <div className="details-section">
                <h4>Detected Signals</h4>
                <ul className="stack-list">
                  {(data.detected_tenses || []).length ? (
                    data.detected_tenses.map((signal, index) => (
                      <li key={`${signal.name}-${signal.evidence}-${index}`} className="stack-list__item">
                        {signal.evidence} <ArrowRight size={14} /> {signal.name.replaceAll("_", " ")}
                      </li>
                    ))
                  ) : (
                    <li className="stack-list__item">No tense signal was recorded.</li>
                  )}
                </ul>
              </div>
            ) : null}
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
    <MasterBox
      title={`Lookup · ${lookupWord}`}
    >
      <div className="utility-box">
        {command === "verb" ? (
          <div className="verb-grid">
            {["v1", "v2", "v3"].map((key, index) => (
              <article key={key} className="verb-cell">
                <span>{["V1", "V2", "V3"][index]}</span>
                <strong>{data[key] || data.forms?.[index] || "—"}</strong>
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
    metrics.push({ key: "submissions", label: "Checked Runs", value: summary.reviewed_submissions || 0, icon: ClipboardMetric });
    metrics.push({ key: "issues", label: "Tracked Issues", value: summary.tracked_issues || 0, icon: Layers3 });
    metrics.push({ key: "focus", label: "Main Focus", value: summary.main_focus || "Balanced", icon: Lightbulb });

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
          title: `${entry.units} · ${entry.label}`,
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
    <MasterBox
      title={isError ? "Unknown Command" : "Dashboard / Analytics"}
    >
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
        <div className="clean-state" style={{ minHeight: "400px", display: "flex", alignItems: "center", justifyContent: "center" }}>
          <p style={{ color: "rgba(25, 26, 35, 0.6)", fontSize: "1.2rem" }}>
            Run a command to see the output here.
          </p>
        </div>
      </MasterBox>
    );
  }

  const command = String(result.command || "").toLowerCase();

  if (command === "check grammar" || command === "explain") {
    return <ReviewWorkflowBox result={result} isExplain={command === "explain"} />;
  }

  if (["spell", "verb", "synonym"].includes(command)) {
    return (
      <UtilityLookupBox
        result={result}
        submittedInput={submittedInput}
        onApplySuggestion={onApplySuggestion}
      />
    );
  }

  return (
    <DashboardBox
      result={result}
      submittedInput={submittedInput}
      onApplySuggestion={onApplySuggestion}
    />
  );
}
