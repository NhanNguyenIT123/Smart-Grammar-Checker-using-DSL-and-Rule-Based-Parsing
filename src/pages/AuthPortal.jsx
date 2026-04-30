import { useEffect, useMemo, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { ArrowLeft, KeyRound, LogIn, Sparkles, UserPlus } from "lucide-react";
import authbg from "@/assets/auth/authbg.svg";
import {
  DEMO_ACCOUNTS,
  fetchCurrentUser,
  loadStoredUser,
  loginWithDemoAccount,
  submitFakeRegistration,
} from "@/lib/api";

function AuthShell({ title, description, children, footer }) {
  return (
    <div
      className="auth-portal"
      style={{
        backgroundImage: `url(${authbg})`,
      }}
    >
      <div className="auth-portal__nav">
        <Link to="/" className="workspace-navbar__brand">
          GrammarDSL
        </Link>
        <div className="workspace-navbar__actions">
          <Link to="/" className="workspace-navbar__link">
            Home
          </Link>
          <Link to="/grammar" className="workspace-navbar__link">
            Grammar Workspace
          </Link>
        </div>
      </div>

      <div className="auth-card">
        <div className="auth-card__header">
          <p className="master-box__eyebrow">Authentication</p>
          <h1>{title}</h1>
          <p>{description}</p>
        </div>
        {children}
        <div className="auth-card__footer">{footer}</div>
      </div>
    </div>
  );
}

export default function AuthPortal() {
  const location = useLocation();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [registerForm, setRegisterForm] = useState({
    fullName: "",
    username: "",
    password: "",
    confirmPassword: "",
  });
  const [forgotEmail, setForgotEmail] = useState("");
  const [forgotSubmitted, setForgotSubmitted] = useState(false);

  const mode = useMemo(() => {
    if (location.pathname === "/register") {
      return "register";
    }
    if (location.pathname === "/forgot-password") {
      return "forgot";
    }
    return "login";
  }, [location.pathname]);

  useEffect(() => {
    const restore = async () => {
      const stored = loadStoredUser();
      if (!stored) {
        return;
      }

      const current = await fetchCurrentUser(stored.id);
      if (current) {
        navigate("/grammar", { replace: true });
      }
    };

    restore();
  }, [navigate]);

  const handleLogin = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError("");
    setMessage("");

    const response = await loginWithDemoAccount(username.trim(), password);

    if (!response.success) {
      setError(response.message);
      setLoading(false);
      return;
    }

    setMessage(response.message);
    setLoading(false);
    navigate("/grammar", { replace: true });
  };

  const handleRegister = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError("");
    setMessage("");

    if (registerForm.password !== registerForm.confirmPassword) {
      setError("Passwords do not match yet.");
      setLoading(false);
      return;
    }

    const response = await submitFakeRegistration(registerForm);
    setLoading(false);

    if (!response.success) {
      setError(response.message);
      return;
    }

    setMessage(response.message);
  };

  const loginFooter = (
    <>
      <div className="auth-demo-row">
        <span>Sample SQLite accounts</span>
        <div className="chip-row">
          {DEMO_ACCOUNTS.map((account) => (
            <button
              type="button"
              key={account.username}
              className="lookup-chip lookup-chip--button"
              onClick={() => {
                setUsername(account.username);
                setPassword(account.password);
              }}
            >
              {account.username} ({account.role})
            </button>
          ))}
        </div>
      </div>
      <p>
        Don&apos;t have an account? <Link to="/register">Create a demo student account</Link>.
      </p>
    </>
  );

  if (mode === "register") {
    return (
      <AuthShell
        title="Create a demo-facing account"
        description="This register flow creates a demo student account in SQLite so you can join classes, generate exercises, and submit quizzes right away."
        footer={
          <p>
            Already have access? <Link to="/login">Go back to log in</Link>.
          </p>
        }
      >
        <form className="auth-form" onSubmit={handleRegister}>
          <label>
            Full Name
            <input
              value={registerForm.fullName}
              onChange={(event) =>
                setRegisterForm((current) => ({ ...current, fullName: event.target.value }))
              }
              placeholder="What should we call you?"
              required
            />
          </label>
          <label>
            Username
            <input
              value={registerForm.username}
              onChange={(event) =>
                setRegisterForm((current) => ({ ...current, username: event.target.value }))
              }
              placeholder="Choose a username"
              required
            />
          </label>
          <label>
            Password
            <input
              type="password"
              value={registerForm.password}
              onChange={(event) =>
                setRegisterForm((current) => ({ ...current, password: event.target.value }))
              }
              placeholder="Create a password"
              required
            />
          </label>
          <label>
            Confirm Password
            <input
              type="password"
              value={registerForm.confirmPassword}
              onChange={(event) =>
                setRegisterForm((current) => ({ ...current, confirmPassword: event.target.value }))
              }
              placeholder="Repeat your password"
              required
            />
          </label>

          {error ? <div className="auth-banner auth-banner--error">{error}</div> : null}
          {message ? <div className="auth-banner auth-banner--success">{message}</div> : null}

          <button type="submit" className="auth-submit" disabled={loading}>
            <UserPlus size={16} />
            {loading ? "Preparing..." : "Sign Up"}
          </button>
        </form>
      </AuthShell>
    );
  }

  if (mode === "forgot") {
    return (
      <AuthShell
        title="Reset password"
        description="This flow is present for the PPL concept, but it stays local and does not touch the backend."
        footer={
          <p>
            <Link to="/login">
              <ArrowLeft size={14} />
              Back to log in
            </Link>
          </p>
        }
      >
        <form
          className="auth-form"
          onSubmit={(event) => {
            event.preventDefault();
            setForgotSubmitted(true);
          }}
        >
          <label>
            Email
            <input
              value={forgotEmail}
              onChange={(event) => setForgotEmail(event.target.value)}
              placeholder="Tell us your email"
              required
            />
          </label>

          {forgotSubmitted ? (
            <div className="auth-banner auth-banner--success">
              Demo note: in a real system we would send the reset link to <strong>{forgotEmail}</strong>.
            </div>
          ) : null}

          <button type="submit" className="auth-submit">
            <KeyRound size={16} />
            Send Reset Link
          </button>
        </form>
      </AuthShell>
    );
  }

  return (
    <AuthShell
      title="Log in to GrammarDSL"
      description="Use a tutor or student SQLite account so grammar history, revision plans, classes, quizzes, and scorebook data stay tied to the right profile."
      footer={loginFooter}
    >
      <form className="auth-form" onSubmit={handleLogin}>
        <label>
          Username
          <input
            value={username}
            onChange={(event) => setUsername(event.target.value)}
            placeholder="alice"
            required
          />
        </label>
        <label>
          Password
          <input
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            placeholder="alice123"
            required
          />
        </label>

        {error ? <div className="auth-banner auth-banner--error">{error}</div> : null}
        {message ? <div className="auth-banner auth-banner--success">{message}</div> : null}

        <button type="submit" className="auth-submit" disabled={loading}>
          <LogIn size={16} />
          {loading ? "Logging In..." : "Log In"}
        </button>

        <div className="auth-inline-links">
          <Link to="/forgot-password">Forgot your password?</Link>
          <span>
            <Sparkles size={14} />
            Demo accounts only
          </span>
        </div>
      </form>
    </AuthShell>
  );
}
