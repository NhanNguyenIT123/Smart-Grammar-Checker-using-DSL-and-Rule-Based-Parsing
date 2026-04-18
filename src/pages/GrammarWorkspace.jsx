import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Bot,
  CheckCircle2,
  ClipboardList,
  HelpCircle,
  RotateCcw,
  SendHorizontal,
} from "lucide-react";
import checkerbg from "@/assets/mainpage/mainpagebg.svg";
import WorkspaceNavbar from "@/components/WorkspaceNavbar";
import ResultTemplates from "@/components/grammar/ResultTemplates";
import {
  executeDslCommand,
  fetchCurrentUser,
  loadStoredUser,
  logoutCurrentUser,
} from "@/lib/api";

const MODE_CONFIG = {
  check: {
    label: "Check",
    helper: "Use Check to see the paragraph, the flagged parts, and a corrected rewrite.",
    defaultInput: "check grammar I go to chracter yesterday.",
  },
  explain: {
    label: "Explain",
    helper: "Use Explain to inspect the strongest reasons, rewrites, and tense signals behind the result.",
    defaultInput:
      "explain grammar Yesterday the coordinator do a report after we make research for the conference.",
  },
  coverage: {
    label: "Coverage",
    helper: "Use Coverage to inspect commands, rule support, and the compiled knowledge pipeline.",
    defaultInput: "help",
  },
};


export default function GrammarWorkspace() {
  const navigate = useNavigate();
  const [currentUser, setCurrentUser] = useState(loadStoredUser());
  const [activeMode, setActiveMode] = useState("check");
  const [input, setInput] = useState(MODE_CONFIG.check.defaultInput);
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

  useEffect(() => {
    setInput(MODE_CONFIG[activeMode].defaultInput);
    setResult(null);
    setSubmittedInput("");
    setBanner("");
  }, [activeMode]);

  const quickMetrics = useMemo(() => {
    if (!result?.data) {
      return [
        { label: "Commands", value: "9" },
        { label: "Templates", value: "3" },
        { label: "Mode", value: MODE_CONFIG[activeMode].label },
      ];
    }

    const data = result.data;
    if (result.command === "check grammar" || result.command === "explain") {
      return [
        { label: "Sentences", value: data.sentence_count || 0 },
        { label: "Grammar", value: data.grammar_errors?.length || 0 },
        { label: "Semantic", value: data.semantic_warnings?.length || 0 },
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

    return [
      { label: "Status", value: result.success ? "Ready" : "Invalid" },
      { label: "Command", value: result.command || "Unknown" },
      { label: "Mode", value: MODE_CONFIG[activeMode].label },
    ];
  }, [activeMode, result]);

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
    setResult(null);
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
            zIndex: -1
          }}
        />
        <section className="workspace-shell">
          <div className="workspace-shell__left">
            <div className="input-panel">
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "1.75rem" }}>
                <div>
                  <p className="master-box__eyebrow">Workspace</p>
                  <h1 style={{ fontSize: "clamp(2rem, 3vw, 3.2rem)", lineHeight: 1, marginBottom: "0.55rem" }}>DSL Input</h1>
                  <p style={{ color: "rgba(25, 26, 35, 0.72)", maxWidth: "44rem", lineHeight: 1.6 }}>{MODE_CONFIG[activeMode].helper}</p>
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
                    height: "fit-content"
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
                <h2 style={{ fontSize: "2rem", color: "#191A23", marginBottom: 0 }}>{MODE_CONFIG[activeMode].label}</h2>
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
