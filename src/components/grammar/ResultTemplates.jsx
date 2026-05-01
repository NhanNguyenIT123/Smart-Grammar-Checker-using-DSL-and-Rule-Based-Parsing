import { useMemo, useState } from "react";
import {
  AlertCircle,
  ArrowRight,
  BarChart3,
  BookOpenText,
  CheckCircle2,
  Clock3,
  GraduationCap,
  History,
  Layers3,
  Lightbulb,
  Search,
  Sparkles,
  UserCheck,
  Users,
} from "lucide-react";

function MasterBox({ title, subtitle, children, className = "", headerActions = null }) {
  return (
    <section className={`master-box flex flex-col ${className}`}>
      <header className="master-box__header" style={{ 
        display: title || subtitle || headerActions ? "block" : "none",
        minHeight: title ? "auto" : "100px"
      }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", minHeight: "3.5rem" }}>
          <div>
            {title ? (
              <h2 className="master-box__title" style={{ marginBottom: subtitle ? "4px" : "0" }}>{title}</h2>
            ) : (
              <div style={{ height: "3rem", width: "18rem", backgroundColor: "rgba(0,0,0,0.08)", borderRadius: "8px", marginBottom: "0.5rem" }} className="animate-pulse"></div>
            )}
            {subtitle ? (
              <p className="master-box__subtitle">{subtitle}</p>
            ) : (
              !title && <div style={{ height: "1.2rem", width: "24rem", backgroundColor: "rgba(0,0,0,0.04)", borderRadius: "4px" }} className="animate-pulse"></div>
            )}
          </div>
        </div>
        {headerActions && <div className="header-actions" style={{ marginTop: "1rem", paddingTop: "1rem", borderTop: "2px solid var(--ink)" }}>{headerActions}</div>}
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
            <div className="details-section" style={{ borderBottom: "1px dashed var(--stroke)", marginBottom: "0.5rem", paddingBottom: "0.5rem" }}>
              <p style={{ fontWeight: 600, fontSize: "0.95rem", color: "var(--ink)" }}>
                Analyzed {data.sentence_count || 1} sentence(s) and found {originalPhrases.length} issue(s).
              </p>
            </div>
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
          <div className="chip-row synonym-chip-row">
            {(data.synonyms || []).map((item) => (
              <span key={item} className="lookup-chip lookup-chip--synonym">
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


function GenerateExerciseBox({ result, onApplySuggestion }) {
  const data = result?.data || {};
  const items = data.items || [];

  return (
    <MasterBox title="Exercise Generator" subtitle="Local NLP-style generation powered by compiled grammar blueprints.">
      <div className="review-stack">
        <div className="review-block">
          <div className="review-block__header">
            <div>
              <h3>Requested Features</h3>
            </div>
            <span className="success-pill success-pill--soft">{items.length} item(s)</span>
          </div>
          <div className="chip-row">
            {(data.features || []).map((feature) => (
              <span key={feature} className="lookup-chip">{feature}</span>
            ))}
          </div>
        </div>

        <div className="review-block">
          <div className="review-block__header">
            <div>
              <h3>Generated Exercises</h3>
            </div>
          </div>
          <div className="dashboard-list">
            {items.map((item, index) => (
              <article 
                key={item.id || index} 
                className="dashboard-list__item cursor-pointer hover:border-black hover:shadow-sm"
                onClick={() => {
                  let textToSolve = item.prompt;
                  if (textToSolve.toLowerCase().startsWith("fill in the missing")) {
                    textToSolve = textToSolve.split(":").slice(1).join(":").trim();
                  }
                  if (textToSolve.toLowerCase().startsWith("rewrite")) {
                    textToSolve = textToSolve.split(":").slice(1).join(":").trim();
                  }
                  onApplySuggestion?.(`check grammar ${textToSolve}`, false);
                }}
                title="Click to load this exercise into the input box"
              >
                <div className="dashboard-list__heading">
                  <h3>{index + 1}. {item.type?.replace(/_/g, " ") || "exercise"}</h3>
                  <span>{item.difficulty}</span>
                </div>
                <div className="bad-input-box" style={{ marginTop: "0.5rem", padding: "0.65rem 0.8rem" }}>
                  <code>{item.prompt}</code>
                </div>
                <div className="chip-row">
                  {(item.features || []).map((feature) => (
                    <span key={`${item.id}-${feature}`} className="lookup-chip lookup-chip--soft">{feature}</span>
                  ))}
                </div>
              </article>
            ))}
          </div>
        </div>
      </div>
    </MasterBox>
  );
}

function CreateQuizBox({ result }) {
  const data = result?.data || {};
  return (
    <MasterBox title="Quiz Created" subtitle="Tutor command compiled into a classroom-ready quiz set.">
      <div className="review-stack">
        <div className="review-block">
          <div className="review-block__header">
            <div>
              <h3>{data.title}</h3>
            </div>
            <span className="success-pill">Quiz #{data.quiz_id}</span>
          </div>
          <p>Class #{data.class_id} | {data.exercise_count} exercise(s)</p>
          <div className="chip-row" style={{ marginTop: "0.75rem" }}>
            <span className="lookup-chip">{data.feature_expr_text}</span>
          </div>
        </div>
        <div className="review-block">
          <div className="review-block__header">
            <div>
              <h3>Quiz Preview</h3>
            </div>
          </div>
          <div className="dashboard-list">
            {(data.items || []).map((item, index) => (
              <article key={item.id || index} className="dashboard-list__item">
                <h3>{index + 1}. {item.prompt}</h3>
                <p>{item.type} | {item.difficulty}</p>
              </article>
            ))}
          </div>
        </div>
      </div>
    </MasterBox>
  );
}

function SubmitAnswersBox({ result }) {
  const data = result?.data || {};
  return (
    <MasterBox title="Quiz Feedback" subtitle="Answer-key first scoring, with grammar feedback when an answer misses the target.">
      <div className="review-stack">
        <div className={`review-block ${data.status === "passed" ? "review-block--clean" : ""}`}>
          <div className="review-block__header">
            <div>
              <h3>Score Summary</h3>
            </div>
            <span className="success-pill">{data.score || 0}/{data.max_score || 0}</span>
          </div>
          <p>{data.feedback_summary}</p>
        </div>
        <div className="dashboard-list">
          {(data.item_results || []).map((item) => (
            <article key={item.question_id} className="dashboard-list__item">
              <div className="dashboard-list__heading">
                <h3>Question {item.question_id}</h3>
                <span>{item.is_correct ? "Correct" : "Review needed"}</span>
              </div>
              <p>{item.prompt}</p>
              <div className="bad-input-box" style={{ marginTop: "0.5rem", padding: "0.65rem 0.8rem" }}>
                <code>Your answer: {item.student_answer || "—"}</code>
              </div>
              <p style={{ marginTop: "0.5rem" }}>Expected: {item.expected_answer}</p>
              
              {item.feedback && !item.is_correct && (
                <div style={{ marginTop: "0.75rem", padding: "0.75rem", backgroundColor: "#EFF6FF", borderRadius: "6px", borderLeft: "4px solid #3B82F6" }}>
                  <div style={{ fontSize: "0.8rem", fontWeight: "bold", color: "#1D4ED8", marginBottom: "0.25rem" }}>Feedback & Hints</div>
                  {typeof item.feedback === "string" ? (
                    !item.feedback.toLowerCase().includes("capitalized letter") && (
                      <p style={{ fontSize: "0.85rem", color: "#1E40AF" }}>{item.feedback}</p>
                    )
                  ) : (
                    <div style={{ fontSize: "0.85rem", color: "#1E40AF" }}>
                      {(item.feedback.grammar_errors || [])
                        .filter(msg => !msg.toLowerCase().includes("capitalized letter"))
                        .map((msg, mIdx) => (
                          <div key={mIdx} style={{ marginBottom: "0.25rem" }}>• {msg}</div>
                        ))
                      }
                    </div>
                  )}
                </div>
              )}
            </article>
          ))}
        </div>
      </div>
    </MasterBox>
  );
}

function StudentRowsBox({ result }) {
  const data = result?.data || {};
  return (
    <MasterBox title="Scorebook Query" subtitle="Tutor-only filtered rows from the selected quiz context.">
      <div className="review-stack">
        <div className="review-block">
          <div className="review-block__header">
            <div>
              <h3>Matched Students</h3>
            </div>
            <span className="success-pill success-pill--soft">{data.matched_rows || 0}/{data.total_rows || 0}</span>
          </div>
          <p>Quiz #{data.quiz_id}</p>
        </div>
        <div className="dashboard-list">
          {(data.rows || []).map((row) => (
            <article key={row.username} className="dashboard-list__item">
              <div className="dashboard-list__heading">
                <h3>{row.student_name}</h3>
                <span>{row.status}</span>
              </div>
              <p>{row.score ?? "—"}/{row.max_score ?? "—"}</p>
              {row.submitted_at ? <p>{new Date(row.submitted_at).toLocaleString()}</p> : null}
            </article>
          ))}
          {!data.rows?.length ? (
            <article className="dashboard-list__item">
              <h3>No students matched this filter</h3>
              <p>Try a broader score or status expression.</p>
            </article>
          ) : null}
        </div>
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

    if (!result?.suggestions?.length) {
      listItems.push({
        title: "Pro-Tip",
        detail: "If you're unsure of the syntax, type 'help' to see a full list of available commands and examples.",
        action: "help",
      });
    }
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
    const sourceCount = (data.pipeline_summary?.sources || data.source_manifest || []).length;
    metrics.push({ key: "sources", label: "Imported Packs", value: sourceCount, icon: Sparkles });

    if (filterKey === "rules") {
      (data.coverage_matrix || []).forEach((entry) => {
        listItems.push({
          title: `${entry.units} | ${entry.label}`,
          detail: `${entry.support_level} support`,
          examples: entry.capabilities || [],
        });
      });
    } else if (filterKey === "dictionary") {
      // For dictionary, we don't want to list 11k words at once.
      // We show a note and provide a few samples or a link to search.
      listItems.push({
        title: "Dictionary Contents",
        detail: `The local lexicon contains ${summary.dictionary_entries || 0} valid English words and phrases.`,
      });
      (data.commands || []).filter(c => c.usage.startsWith("spell") || c.usage.startsWith("verb")).forEach(c => {
        listItems.push({
          title: `Related Command: ${c.usage}`,
          detail: c.description,
          action: c.usage
        });
      });
    } else if (filterKey === "sources") {
      (data.pipeline_summary?.sources || []).forEach((source) => {
        listItems.push({
          title: source.id || source.origin || "Unknown Pack",
          detail: `Type: ${source.type} | Origin: ${source.origin}`,
          meta: source.description
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

  const isSyntaxError = !result.command || result.command === "unknown" || result.command === "invalid" || result.command === "request_failed";

  return (
    <MasterBox title={isError ? (isSyntaxError ? "Unknown Command" : "Execution Error") : "Dashboard / Analytics"}>
      {isError ? (
        <div className="suggestion-card">
          <div className="suggestion-card__icon">
            <AlertCircle size={20} />
          </div>
          <div className="suggestion-card__copy">
            <h3>{isSyntaxError ? "Did you mean this command?" : "Command Execution Failed"}</h3>
            <p>
              {isSyntaxError 
                ? "The command prefix does not match a supported GrammarDSL form." 
                : "The command syntax is correct, but it could not be completed."}
            </p>
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
                setFilterKey(current => current === metric.key ? "overview" : metric.key);
                setVisibleCount(5);
              }
            }}
          />
        ))}
      </div>

      {result.command === "help" && filterKey !== "overview" ? (
        <div style={{ marginBottom: "1rem", display: "flex", justifyContent: "flex-end" }}>
          <button
            type="button"
            className="suggestion-cta"
            onClick={() => setFilterKey("overview")}
            style={{ fontSize: "0.85rem", padding: "4px 12px" }}
          >
            ← Back to Commands
          </button>
        </div>
      ) : null}

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

export function QuizScore({ data }) {
  if (!data || !data.item_results) {
    return (
      <div className="clean-state" style={{ padding: "1rem" }}>
        <p style={{ color: "#6B7280" }}>No detailed result data available for this attempt.</p>
      </div>
    );
  }

  return (
    <div style={{ display: "grid", gap: "1.25rem" }}>
      {data.item_results.map((item, idx) => (
        <div 
          key={idx} 
          style={{ 
            padding: "1rem", 
            border: "2px solid var(--ink)", 
            backgroundColor: "#fff",
            borderRadius: "8px"
          }}
        >
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "0.5rem" }}>
            <span style={{ fontWeight: "bold", color: "#111827" }}>Question {item.item_index || idx + 1}</span>
            <span 
              className={`lookup-chip ${item.is_correct ? "lookup-chip--button" : "lookup-chip--soft"}`}
              style={{ backgroundColor: item.is_correct ? "#D1FAE5" : "#FEE2E2", color: item.is_correct ? "#065F46" : "#991B1B" }}
            >
              {item.is_correct ? "Correct" : "Incorrect"}
            </span>
          </div>
          <p style={{ fontSize: "1rem", color: "#374151", marginBottom: "0.75rem" }}>{item.prompt}</p>
          
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "1rem", marginTop: "0.5rem" }}>
            <div className="bad-input-box" style={{ padding: "0.5rem" }}>
              <div style={{ fontSize: "0.7rem", textTransform: "uppercase", color: "#6B7280", marginBottom: "0.25rem" }}>Student Answer</div>
              <code style={{ color: item.is_correct ? "#065F46" : "#991B1B" }}>{item.student_answer || "(No answer)"}</code>
            </div>
            {!item.is_correct && (
              <div className="bad-input-box" style={{ padding: "0.5rem", borderColor: "#B9FF66" }}>
                <div style={{ fontSize: "0.7rem", textTransform: "uppercase", color: "#6B7280", marginBottom: "0.25rem" }}>Expected Answer</div>
                <code>{item.expected_answer}</code>
              </div>
            )}
          </div>

          {item.feedback && !item.is_correct && (
            <div style={{ marginTop: "0.75rem", padding: "0.75rem", backgroundColor: "#EFF6FF", borderRadius: "6px", borderLeft: "4px solid #3B82F6" }}>
              <div style={{ fontSize: "0.8rem", fontWeight: "bold", color: "#1D4ED8", marginBottom: "0.25rem" }}>Feedback & Hints</div>
              {typeof item.feedback === "string" ? (
                !item.feedback.toLowerCase().includes("capitalized letter") && (
                  <p style={{ fontSize: "0.85rem", color: "#1E40AF" }}>{item.feedback}</p>
                )
              ) : (
                <div style={{ fontSize: "0.85rem", color: "#1E40AF" }}>
                  {(item.feedback.grammar_errors || [])
                    .filter(msg => !msg.toLowerCase().includes("capitalized letter"))
                    .map((msg, mIdx) => (
                      <div key={mIdx} style={{ marginBottom: "0.25rem" }}>• {msg}</div>
                    ))
                  }
                </div>
              )}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}

function ScorebookVisualization({ result, onRunCommand, quizDetail, quizAttempts, questionStats }) {
  const [expandedStudent, setExpandedStudent] = useState(null);

  return (
    <div style={{ display: "grid", gap: "1.5rem" }}>
      <MasterBox 
        title="Question Success Heatmap" 
        subtitle="Hover for question details"
        className="border-2 border-black"
      >
        <div style={{ padding: "1.5rem" }}>
          {questionStats.items.length ? (
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(110px, 1fr))", gap: "1rem" }}>
              {questionStats.items.map((stat, idx) => {
                const successRate = Math.round((stat.correct / stat.total) * 100);
                let bgColor = "#fff";
                let textColor = "var(--ink)";
                
                if (successRate >= 90) { bgColor = "#B9FF66"; }
                else if (successRate >= 75) { bgColor = "#D9F99D"; }
                else if (successRate >= 50) { bgColor = "#FEF08A"; }
                else if (successRate >= 25) { bgColor = "#FED7AA"; }
                else { bgColor = "#FEE2E2"; textColor = "#991B1B"; }

                return (
                  <div 
                    key={idx} 
                    className="bad-input-box transition-all hover:shadow-md hover:-translate-y-1" 
                    title={`Prompt: ${stat.prompt}`}
                    style={{ 
                      padding: "1rem", 
                      backgroundColor: bgColor,
                      borderColor: "var(--ink)",
                      textAlign: "center",
                      cursor: "help"
                    }}
                  >
                    <div style={{ fontSize: "0.75rem", fontWeight: "bold", opacity: 0.6, textTransform: "uppercase" }}>Q{idx + 1}</div>
                    <div style={{ fontSize: "1.5rem", fontWeight: "black", margin: "4px 0", color: textColor }}>{successRate}%</div>
                    <div style={{ fontSize: "0.65rem", textTransform: "uppercase", letterSpacing: "0.05em", opacity: 0.8 }}>Success</div>
                  </div>
                );
              })}
            </div>
          ) : (
            <div className="clean-state">
              <p style={{ fontStyle: "italic", color: "#6B7280" }}>No submission data available for this quiz yet.</p>
            </div>
          )}
        </div>
      </MasterBox>

      <MasterBox 
        title="Student Performance"
        subtitle={quizDetail?.title || "Quiz Results"}
        className="border-2 border-black bg-white"
        headerActions={
          <div className="flex gap-2 items-center">
            <span style={{ fontSize: "0.75rem", color: "#6B7280", fontWeight: 800, textTransform: "uppercase" }}>Filters:</span>
            {[
              { label: "Submitted", cmd: "show students with submitted" },
              { label: "Top Scorers", cmd: "show students with score >= 80%" },
              { label: "Needs Help", cmd: "show students with failed OR not submitted" },
            ].map((filter) => (
              <button
                key={filter.label}
                type="button"
                className="px-3 py-1.5 bg-white hover:bg-[#B9FF66] border-2 border-black text-[10px] font-black transition-all uppercase tracking-tight"
                style={{ boxShadow: "2px 2px 0px 0px #000" }}
                onClick={() => onRunCommand?.(filter.cmd, { mode: "scorebook", quizId: quizDetail.id })}
              >
                {filter.label}
              </button>
            ))}
          </div>
        }
      >
        <div style={{ padding: "1rem" }}>
          {((result.data?.rows) || quizAttempts || []).length ? (
            <div style={{ display: "grid", gap: "0.75rem" }}>
              {((result.data?.rows) || quizAttempts || []).map((row) => {
                const isExpanded = expandedStudent === row.username;
                const grading = row.submission_payload?.grading || row.submission_payload;
                
                return (
                  <div 
                    key={row.username} 
                    className="dashboard-list__item"
                    style={{ 
                      border: "2px solid var(--ink)", 
                      borderRadius: "12px", 
                      overflow: "hidden",
                      padding: 0
                    }}
                  >
                    <div 
                      style={{ 
                        padding: "1.25rem", 
                        cursor: "pointer",
                        display: "flex", 
                        justifyContent: "space-between", 
                        alignItems: "center",
                        backgroundColor: isExpanded ? "#f8fafc" : "#fff",
                        transition: "background-color 0.2s"
                      }}
                      onClick={() => {
                        setExpandedStudent(isExpanded ? null : row.username);
                        const cmd = `show results for student ${row.username} for quiz ${quizDetail.id}`;
                        onRunCommand?.(cmd, { mode: "scorebook", studentUsername: row.username, quizId: quizDetail.id });
                      }}
                    >
                      <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
                        <div style={{ 
                          width: "40px", 
                          height: "40px", 
                          borderRadius: "50%", 
                          backgroundColor: "#f1f5f9", 
                          display: "flex", 
                          alignItems: "center", 
                          justifyContent: "center",
                          border: "2px solid var(--ink)"
                        }}>
                          <Users size={20} />
                        </div>
                        <div>
                          <strong style={{ fontSize: "1.1rem", display: "block" }}>{row.student_name || row.username}</strong>
                          <span style={{ fontSize: "0.85rem", color: "#64748b" }}>@{row.username}</span>
                        </div>
                      </div>

                      <div style={{ textAlign: "right" }}>
                        {row.status === "submitted" ? (
                          <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                            <div style={{ textAlign: "right" }}>
                              <div style={{ fontSize: "1.2rem", fontWeight: "900", color: row.score >= row.max_score * 0.8 ? "#059669" : "#191A23" }}>
                                {row.score}/{row.max_score}
                              </div>
                              <div style={{ fontSize: "0.75rem", textTransform: "uppercase", fontWeight: "bold", opacity: 0.5 }}>Points</div>
                            </div>
                            <ArrowRight size={18} className="opacity-30" />
                          </div>
                        ) : (
                          <span className="lookup-chip lookup-chip--soft" style={{ backgroundColor: "#f1f5f9", color: "#64748b" }}>
                            Not submitted
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          ) : (
            <p style={{ padding: "2rem", textAlign: "center", color: "#6B7280", fontStyle: "italic" }}>
              No students have joined this class yet.
            </p>
          )}
        </div>
      </MasterBox>

      <div className="auth-banner" style={{ backgroundColor: "#f8fafc", color: "#64748b", border: "1px dashed #cbd5e1" }}>
        <div style={{ display: "flex", alignItems: "center", gap: "8px", fontSize: "0.85rem" }}>
          <Lightbulb size={16} />
          <span>Interactive Tip: Click any student above to automatically run the <code>show results</code> command for them.</span>
        </div>
      </div>
    </div>
  );
}

function ClassListPreview({ result, onRunCommand }) {
  const data = result?.data || {};
  const classes = data.classes || [];

  return (
    <MasterBox 
      title="Managed Classes" 
      subtitle="Overview of all active clinical sessions"
      className="border-2 border-black"
    >
      <div style={{ padding: "1.5rem" }}>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))", gap: "1.5rem" }}>
          {classes.map((cls) => (
            <div 
              key={cls.id} 
              className="dashboard-list__item"
              style={{ 
                border: "2px solid var(--ink)", 
                borderRadius: "16px", 
                padding: "1.5rem",
                display: "flex",
                flexDirection: "column",
                gap: "1rem",
                backgroundColor: "#fff",
                transition: "all 0.2s"
              }}
            >
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
                <div>
                  <div style={{ fontSize: "0.7rem", fontWeight: "900", textTransform: "uppercase", opacity: 0.4, marginBottom: "4px" }}>
                    ID: #{cls.id}
                  </div>
                  <h3 style={{ fontSize: "1.25rem", margin: 0 }}>{cls.name}</h3>
                </div>
                <div style={{ backgroundColor: "#B9FF66", padding: "4px 8px", borderRadius: "6px", border: "1px solid var(--ink)", fontSize: "0.75rem", fontWeight: "bold" }}>
                  Active
                </div>
              </div>

              <div style={{ display: "flex", gap: "1rem", fontSize: "0.85rem", opacity: 0.8 }}>
                <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
                  <Users size={16} />
                  {cls.roster_count} Students
                </div>
                <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
                  <LayoutList size={16} />
                  {cls.quiz_count} Quizzes
                </div>
              </div>

              <div style={{ marginTop: "0.5rem" }}>
                <button 
                  className="lookup-chip lookup-chip--button w-full"
                  onClick={() => onRunCommand?.(`show class ${cls.id}`)}
                  style={{ display: "flex", justifyContent: "center", padding: "10px" }}
                >
                  Inspect Roster
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </MasterBox>
  );
}

function ClassRosterBox({ result }) {
  const data = result?.data || {};
  const rows = data.rows || [];

  return (
    <MasterBox 
      title={`Class Roster: #${data.class_id}`} 
      subtitle="Full list of students enrolled in this clinical session"
      className="border-2 border-black"
    >
      <div style={{ padding: "1.5rem" }}>
        <div style={{ marginBottom: "1.5rem", display: "flex", alignItems: "center", gap: "10px" }}>
          <div style={{ backgroundColor: "var(--ink)", color: "#fff", padding: "8px 16px", borderRadius: "8px" }}>
            <span style={{ fontSize: "1.2rem", fontWeight: "bold" }}>{data.total_students}</span>
          </div>
          <span style={{ fontWeight: "bold", textTransform: "uppercase", fontSize: "0.8rem", opacity: 0.6 }}>Enrolled Students</span>
        </div>

        <div style={{ display: "grid", gap: "1rem" }}>
          {rows.map((row) => (
            <div 
              key={row.username} 
              className="dashboard-list__item"
              style={{ 
                border: "2px solid var(--ink)", 
                borderRadius: "12px", 
                padding: "1rem",
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                backgroundColor: "#fff"
              }}
            >
              <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
                <div style={{ 
                  width: "48px", 
                  height: "48px", 
                  borderRadius: "50%", 
                  backgroundColor: "#f1f5f9", 
                  display: "flex", 
                  alignItems: "center", 
                  justifyContent: "center",
                  border: "2px solid var(--ink)"
                }}>
                  <Users size={24} />
                </div>
                <div>
                  <strong style={{ fontSize: "1.1rem", display: "block" }}>{row.student_name}</strong>
                  <span style={{ fontSize: "0.85rem", color: "#64748b" }}>@{row.username}</span>
                </div>
              </div>
              <div style={{ textAlign: "right", maxWidth: "250px" }}>
                <div style={{ fontSize: "0.75rem", textTransform: "uppercase", fontWeight: "bold", opacity: 0.5, marginBottom: "4px" }}>Focus Hint</div>
                <div style={{ fontSize: "0.85rem", fontStyle: "italic", lineHeight: "1.2" }}>{row.focus_hint || "General study"}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </MasterBox>
  );
}

function ResultTemplates({ result, submittedInput, onApplySuggestion, onRunCommand, quizDetail, quizAttempts, questionStats }) {
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


  if (command === "generate") {
    return <GenerateExerciseBox result={result} onApplySuggestion={onApplySuggestion} />;
  }

  if (command === "create quiz" && result.success) {
    return <CreateQuizBox result={result} />;
  }

  if (command === "submit answers" && result.success) {
    return <SubmitAnswersBox result={result} />;
  }

  if (command === "show students" && result.success) {
    return (
      <ScorebookVisualization 
        result={result} 
        onRunCommand={onRunCommand}
        quizDetail={quizDetail}
        quizAttempts={quizAttempts}
        questionStats={questionStats}
      />
    );
  }

  if (command === "show results" && result.success) {
    const data = result?.data || {};
    return (
      <MasterBox 
        title={`Results: ${data.student_name}`} 
        subtitle="Detailed grading and feedback from the grammar engine"
        className="border-2 border-black"
      >
        <div style={{ padding: "1.5rem" }}>
          <div style={{ marginBottom: "1.5rem", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
              <div style={{ backgroundColor: "#B9FF66", padding: "8px 16px", border: "2px solid var(--ink)", borderRadius: "8px" }}>
                <span style={{ fontSize: "1.5rem", fontWeight: "900" }}>{data.score}/{data.max_score}</span>
              </div>
              <span style={{ fontWeight: "bold", textTransform: "uppercase", fontSize: "0.8rem", opacity: 0.6 }}>Final Score</span>
            </div>
            <button 
              className="suggestion-cta" 
              onClick={() => onRunCommand?.("show students")}
              style={{ fontSize: "0.85rem" }}
            >
              ← Back to Scorebook
            </button>
          </div>
          <QuizScore data={data.grading} />
        </div>
      </MasterBox>
    );
  }

  // Special case: show results for a student who hasn't submitted yet
  if (command === "show results" && !result.success && result.message?.includes("No submission found")) {
    return (
      <MasterBox 
        title="Student Status" 
        subtitle="Analytical drill-down"
        className="border-2 border-black"
      >
        <div style={{ padding: "3rem 1.5rem", textAlign: "center" }}>
          <div style={{ 
            width: "64px", 
            height: "64px", 
            backgroundColor: "#f1f5f9", 
            borderRadius: "50%", 
            display: "flex", 
            alignItems: "center", 
            justifyContent: "center",
            margin: "0 auto 1.5rem"
          }}>
            <Clock3 size={32} className="text-slate-400" />
          </div>
          <h3 style={{ fontSize: "1.25rem", fontWeight: "bold", marginBottom: "0.5rem" }}>No Submission Yet</h3>
          <p style={{ color: "#64748b", maxWidth: "300px", margin: "0 auto 1.5rem" }}>
            {result.message}
          </p>
          <button 
            className="suggestion-cta" 
            onClick={() => onRunCommand?.("show students")}
          >
            Return to Scorebook
          </button>
        </div>
      </MasterBox>
    );
  }

  if (command === "show quiz" && result.success) {
    const data = result?.data || {};
    return (
      <MasterBox 
        title={`Quiz Details: ${data.title} (#${data.id})`} 
        subtitle="Structure and target grammar features for this exercise set"
        className="border-2 border-black"
      >
        <div className="review-stack" style={{ padding: "1.5rem" }}>
          <div className="review-block">
            <div className="review-block__header">
              <h3>Target Grammar</h3>
            </div>
            <div className="chip-row">
              <span className="lookup-chip">{data.feature_expr_text}</span>
            </div>
          </div>
          <div className="review-block">
            <div className="review-block__header">
              <h3>Exercise List ({data.exercise_count})</h3>
            </div>
            <div className="dashboard-list">
              {(data.items || []).map((item, index) => (
                <article key={item.id || index} className="dashboard-list__item">
                  <div className="dashboard-list__heading">
                    <h3>{index + 1}. {item.prompt}</h3>
                    <span>{item.type}</span>
                  </div>
                  <div style={{ marginTop: "0.5rem", fontSize: "0.85rem", display: "flex", gap: "1rem" }}>
                    <span style={{ opacity: 0.7 }}>Difficulty: {item.difficulty}</span>
                    {item.expected_answer && (
                      <span style={{ color: "#059669", fontWeight: "bold" }}>
                        Key: {item.expected_answer}
                      </span>
                    )}
                  </div>
                </article>
              ))}
            </div>
          </div>
        </div>
      </MasterBox>
    );
  }

  if (command === "show class" && result.success) {
    return <ClassRosterBox result={result} />;
  }

  if (command === "show classes" && result.success) {
    return <ClassListPreview result={result} onRunCommand={onRunCommand} />;
  }

  if (["spell", "verb", "synonym"].includes(command)) {
    return <UtilityLookupBox result={result} submittedInput={submittedInput} onApplySuggestion={onApplySuggestion} />;
  }

  return <DashboardBox result={result} submittedInput={submittedInput} onApplySuggestion={onApplySuggestion} />;
}

ResultTemplates.QuizScore = QuizScore;
export default ResultTemplates;
