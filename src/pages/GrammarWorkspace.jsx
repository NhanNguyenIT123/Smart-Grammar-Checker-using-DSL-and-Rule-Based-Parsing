import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { HelpCircle, SendHorizontal } from "lucide-react";
import checkerbg from "@/assets/mainpage/mainpagebg.svg";
import WorkspaceNavbar from "@/components/WorkspaceNavbar";
import ResultTemplates from "@/components/grammar/ResultTemplates";
import {
  executeDslCommand,
  fetchCurrentUser,
  loadStoredUser,
  logoutCurrentUser,
} from "@/lib/api";

const DEFAULT_COMMAND = "help";

function formatPanelTitle(command) {
  if (!command) {
    return "Command Output";
  }

  return String(command)
    .split(/\s+/)
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}

export default function GrammarWorkspace() {
  const navigate = useNavigate();
  const [currentUser, setCurrentUser] = useState(loadStoredUser());
  const [input, setInput] = useState(DEFAULT_COMMAND);
  const [submittedInput, setSubmittedInput] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [banner, setBanner] = useState("");

  useEffect(() => {
    const restore = async () => {
      const stored = loadStoredUser();
      if (!stored) {
        navigate("/login", { replace: true });
        return;
      }

      const user = await fetchCurrentUser(stored.id);
      if (!user) {
        navigate("/login", { replace: true });
        return;
      }

      setCurrentUser(user);
    };

    restore();
  }, [navigate]);

  const quickMetrics = useMemo(() => {
    if (!result?.data) {
      return [
        { label: "Commands", value: "9" },
        { label: "Pipeline", value: "ANTLR + Rules" },
        { label: "Start Here", value: "help" },
      ];
    }

    const data = result.data;
    if (result.command === "check grammar") {
      return [
        { label: "Sentences", value: data.sentence_count || 0 },
        { label: "Grammar", value: data.grammar_errors?.length || 0 },
        { label: "Semantic", value: data.semantic_warnings?.length || 0 },
      ];
    }

    if (result.command === "show tokens") {
      return [
        { label: "Tokens", value: data.token_count || 0 },
        { label: "Parsable", value: data.parsable ? "Yes" : "No" },
        { label: "Command", value: data.command_type || "Lexer only" },
      ];
    }

    if (result.command === "revision plan") {
      return [
        { label: "Checked Runs", value: data.summary?.reviewed_submissions || 0 },
        { label: "Tracked Issues", value: data.summary?.tracked_issues || 0 },
        { label: "Main Focus", value: data.summary?.main_focus || "Balanced" },
      ];
    }

    if (result.command === "history") {
      return [
        { label: "History", value: data.total_commands || 0 },
        { label: "Recent", value: data.entries?.length || 0 },
        { label: "Mode", value: "Timeline" },
      ];
    }

    if (result.command === "help") {
      const stats = data.pipeline_summary?.knowledge_stats || {};
      return [
        { label: "Commands", value: data.commands?.length || 0 },
        { label: "Imported Packs", value: stats.imported_sources || 0 },
        { label: "Rules", value: stats.phrase_index_entries || 0 },
      ];
    }

    return [
      { label: "Status", value: result.success ? "Ready" : "Invalid" },
      { label: "Command", value: result.command || "Unknown" },
      { label: "Mode", value: "Workspace" },
    ];
  }, [result]);

  const runCommand = async (value) => {
    if (!currentUser?.id) {
      setBanner("Please log in first.");
      navigate("/login", { replace: true });
      return;
    }

    setLoading(true);
    setBanner("");
    setSubmittedInput(value);

    const response = await executeDslCommand(value, currentUser.id);

    if (!response.success && response.command === "auth_required") {
      setBanner(response.message);
      navigate("/login", { replace: true });
      return;
    }

    setResult(response);
    setLoading(false);
  };

  const handleLogout = async () => {
    if (currentUser?.id) {
      await logoutCurrentUser(currentUser.id);
    }
    setCurrentUser(null);
    setInput(DEFAULT_COMMAND);
    setSubmittedInput("");
    setResult(null);
    setBanner("");
    navigate("/login", { replace: true });
  };

  return (
    <div className="workspace-page">
      <WorkspaceNavbar currentUser={currentUser} onLogout={handleLogout} />

      <main className="workspace-page__body" style={{ position: "relative", zIndex: 1 }}>
        <img
          src={checkerbg}
          alt="background"
          className="absolute pointer-events-none"
          style={{
            top: 0,
            left: 0,
            width: "100%",
            height: "100%",
            objectFit: "cover",
            zIndex: -1,
          }}
        />
        <section className="workspace-shell">
          <div className="workspace-shell__left">
            <div className="input-panel">
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "flex-start",
                  marginBottom: "1.75rem",
                }}
              >
                <div>
                  <p className="master-box__eyebrow">Workspace</p>
                  <h1
                    style={{
                      fontSize: "clamp(2rem, 3vw, 3.2rem)",
                      lineHeight: 1,
                      marginBottom: "0.55rem",
                    }}
                  >
                    DSL Input
                  </h1>
                  <p style={{ color: "rgba(25, 26, 35, 0.72)", maxWidth: "44rem", lineHeight: 1.6 }}>
                    Start with <code>help</code> to inspect the supported commands, then move into{" "}
                    <code>show tokens</code>, <code>check grammar</code>, <code>history</code>, or{" "}
                    <code>revision plan</code>.
                  </p>
                </div>

                <button
                  type="button"
                  onClick={() => runCommand(input)}
                  disabled={loading}
                  className="hover:translate-x-[2px] hover:translate-y-[2px] hover:shadow-[1px_1px_0px_0px_#191A23]"
                  style={{
                    backgroundColor: "#B9FF66",
                    color: "#191A23",
                    fontWeight: "bold",
                    fontSize: "1rem",
                    padding: "10px 24px",
                    borderRadius: "8px",
                    border: "2px solid #191A23",
                    boxShadow: "3px 3px 0px 0px #191A23",
                    cursor: loading ? "not-allowed" : "pointer",
                    transition: "all 0.2s",
                    display: "flex",
                    alignItems: "center",
                    gap: "8px",
                    height: "fit-content",
                  }}
                >
                  <SendHorizontal size={16} />
                  {loading ? "Running..." : "Run Command"}
                </button>
              </div>

              <textarea
                value={input}
                onChange={(event) => setInput(event.target.value)}
                className="dsl-textarea"
                placeholder="Type your DSL command here..."
              />

              {banner ? <div className="auth-banner auth-banner--error">{banner}</div> : null}
            </div>
          </div>

          <div className="workspace-shell__right">
            <div className="response-header" style={{ backgroundColor: "#B9FF66" }}>
              <div>
                <h2 style={{ fontSize: "2rem", color: "#191A23", marginBottom: 0 }}>
                  {formatPanelTitle(result?.command)}
                </h2>
              </div>

              <div className="response-header__metrics">
                {quickMetrics.map((item) => (
                  <div key={item.label} className="response-metric" style={{ border: "2px solid #191A23" }}>
                    <span>{item.label}</span>
                    <strong>{item.value}</strong>
                  </div>
                ))}
              </div>
            </div>

            <ResultTemplates
              result={result}
              submittedInput={submittedInput}
              onApplySuggestion={(suggestion) => {
                setInput(suggestion);
                runCommand(suggestion);
              }}
            />

            {result?.message ? (
              <div className="message-strip">
                <HelpCircle size={16} />
                <span>{result.message}</span>
              </div>
            ) : null}
          </div>
        </section>
      </main>
    </div>
  );
}
