const API_BASE = "/api";
const USER_STORAGE_KEY = "grammardsl-demo-user";

function buildHeaders(userId, extraHeaders = {}) {
  const headers = { ...extraHeaders };

  if (userId) {
    headers["X-GrammarDSL-User-Id"] = String(userId);
  }

  return headers;
}

async function parseJsonResponse(response) {
  const raw = await response.text();

  try {
    return raw ? JSON.parse(raw) : {};
  } catch (error) {
    return {
      success: false,
      message: raw || "The server returned an unreadable response.",
    };
  }
}

function toDisplayName(userLike) {
  const username = String(userLike?.username || "").trim();
  if (!username) {
    return "GrammarDSL User";
  }

  return username
    .split(/[\s._-]+/)
    .filter(Boolean)
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}

const SESSION_TIMEOUT_MS = 15 * 60 * 1000; // 15 minutes

export function normalizeUser(payload) {
  const rawUser =
    payload?.user ??
    payload?.data?.user ??
    payload?.data ??
    payload;

  if (!rawUser || (!rawUser.id && !rawUser.username && !rawUser.user_id)) {
    return null;
  }

  return {
    id: String(rawUser.id ?? rawUser.user_id ?? rawUser.userId ?? rawUser.username),
    username: String(rawUser.username ?? rawUser.user_name ?? rawUser.name ?? "guest"),
    displayName: String(
      rawUser.display_name ??
        rawUser.displayName ??
        rawUser.full_name ??
        rawUser.fullName ??
        toDisplayName(rawUser)
    ),
    lastActivity: payload.lastActivity || Date.now(),
  };
}

export function loadStoredUser() {
  try {
    const raw = window.localStorage.getItem(USER_STORAGE_KEY);
    if (!raw) {
      return null;
    }

    const data = JSON.parse(raw);
    const now = Date.now();

    if (data.lastActivity && now - data.lastActivity > SESSION_TIMEOUT_MS) {
      window.localStorage.removeItem(USER_STORAGE_KEY);
      return null;
    }

    return normalizeUser(data);
  } catch (error) {
    return null;
  }
}

export function persistUser(user) {
  if (!user) {
    return;
  }
  const data = { ...user, lastActivity: Date.now() };
  window.localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(data));
}

export function updateActivity() {
  const user = loadStoredUser();
  if (user) {
    persistUser(user);
  }
}

export function clearStoredUser() {
  window.localStorage.removeItem(USER_STORAGE_KEY);
}

export async function fetchCurrentUser(userId) {
  const response = await fetch(`${API_BASE}/auth/me`, {
    credentials: "include",
    headers: buildHeaders(userId),
  });

  const payload = await parseJsonResponse(response);

  if (!response.ok || payload?.authenticated === false) {
    return null;
  }

  return normalizeUser(payload);
}

export async function loginWithDemoAccount(username, password) {
  const response = await fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    credentials: "include",
    headers: buildHeaders(null, {
      "Content-Type": "application/json",
    }),
    body: JSON.stringify({ username, password }),
  });

  const payload = await parseJsonResponse(response);

  if (!response.ok) {
    return {
      success: false,
      message: payload?.message || "Login failed.",
    };
  }

  const user = normalizeUser(payload);

  if (!user) {
    return {
      success: false,
      message: "Login succeeded, but the user profile could not be resolved.",
    };
  }

  persistUser(user);

  return {
    success: true,
    user,
    message: payload?.message || "Logged in successfully.",
  };
}

export async function logoutCurrentUser(userId) {
  try {
    await fetch(`${API_BASE}/auth/logout`, {
      method: "POST",
      credentials: "include",
      headers: buildHeaders(userId),
    });
  } finally {
    clearStoredUser();
  }
}

export async function submitFakeRegistration(formData) {
  const response = await fetch(`${API_BASE}/auth/register`, {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(formData),
  });

  const payload = await parseJsonResponse(response);

  return {
    success: response.ok,
    message:
      payload?.message ||
      "Registration is in demo mode. Please use one of the sample SQLite accounts.",
  };
}

export async function executeDslCommand(input, userId) {
  let response;
  let payload;
  try {
    response = await fetch(`${API_BASE}/command`, {
      method: "POST",
      credentials: "include",
      headers: buildHeaders(userId, {
        "Content-Type": "application/json",
      }),
      body: JSON.stringify({ input }),
    });
    payload = await parseJsonResponse(response);
  } catch (error) {
    return {
      success: false,
      command: "network_error",
      message: "Could not connect to the GrammarDSL server. Please make sure the backend is running.",
      suggestions: [],
      data: {},
    };
  }

  if (response.status === 401) {
    return {
      success: false,
      command: "auth_required",
      message: payload?.message || "Please log in first.",
      suggestions: [],
      data: {},
    };
  }

  if (!response.ok && typeof payload?.success !== "boolean") {
    return {
      success: false,
      command: "request_failed",
      message: payload?.message || "The command request failed.",
      suggestions: payload?.suggestions || [],
      data: payload?.data || {},
    };
  }

  return {
    success: Boolean(payload?.success),
    command: payload?.command || "unknown",
    message: payload?.message || "",
    data: payload?.data || {},
    suggestions: payload?.suggestions || [],
  };
}

export const DEMO_ACCOUNTS = [
  { username: "alice", password: "alice123", displayName: "Alice Nguyen" },
  { username: "brian", password: "brian123", displayName: "Brian Tran" },
  { username: "clara", password: "clara123", displayName: "Clara Le" },
];
