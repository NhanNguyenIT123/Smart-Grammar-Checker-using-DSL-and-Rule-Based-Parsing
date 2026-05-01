const API_BASE = import.meta.env.VITE_API_BASE_URL || "/api";
const USER_STORAGE_KEY = "grammardsl-demo-user";
const SESSION_TIMEOUT_MS = 15 * 60 * 1000;

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

export function normalizeUser(payload) {
  if (!payload) return null;

  // Handle various nested structures
  const rawUser =
    payload?.user ??
    payload?.data?.user ??
    payload?.data ??
    (payload?.username || payload?.id || payload?.user_id ? payload : null);

  if (!rawUser) {
    return null;
  }

  // Ensure we have at least an ID or username
  const id = String(rawUser.id ?? rawUser.user_id ?? rawUser.userId ?? rawUser.username || "");
  const username = String(rawUser.username ?? rawUser.user_name ?? rawUser.name ?? id || "guest");

  if (!id && !username) return null;

  return {
    id: id || username,
    username: username,
    displayName: String(
      rawUser.display_name ??
        rawUser.displayName ??
        rawUser.full_name ??
        rawUser.fullName ??
        toDisplayName(rawUser)
    ),
    role: String(rawUser.role || "student"),
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
    if (data.lastActivity && Date.now() - data.lastActivity > SESSION_TIMEOUT_MS) {
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
    body: JSON.stringify({
      username: formData.username,
      password: formData.password,
      displayName: formData.fullName,
    }),
  });

  const payload = await parseJsonResponse(response);
  return {
    success: response.ok,
    message: payload?.message || "Could not create the demo student account.",
  };
}

export async function executeDslCommand(input, userId, context = {}) {
  let response;
  let payload;
  try {
    response = await fetch(`${API_BASE}/command`, {
      method: "POST",
      credentials: "include",
      headers: buildHeaders(userId, {
        "Content-Type": "application/json",
      }),
      body: JSON.stringify({ input, context }),
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

  if (!response.ok && payload?.success === undefined) {
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

async function getJson(path, userId) {
  const response = await fetch(`${API_BASE}${path}`, {
    credentials: "include",
    headers: buildHeaders(userId),
  });
  const payload = await parseJsonResponse(response);
  if (!response.ok) {
    throw new Error(payload?.message || "Request failed.");
  }
  return payload;
}

async function postJson(path, body, userId) {
  const response = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    credentials: "include",
    headers: buildHeaders(userId, {
      "Content-Type": "application/json",
    }),
    body: JSON.stringify(body),
  });
  const payload = await parseJsonResponse(response);
  if (!response.ok) {
    throw new Error(payload?.message || "Request failed.");
  }
  return payload;
}

export async function listClasses(userId) {
  const payload = await getJson("/classes", userId);
  return payload.classes || [];
}

export async function createClass(name, userId) {
  const payload = await postJson("/classes", { name }, userId);
  return payload.class;
}

export async function joinClass(joinCode, userId) {
  const payload = await postJson("/classes/join", { joinCode }, userId);
  return payload.class;
}

export async function getClassDetail(classId, userId) {
  return getJson(`/classes/${classId}`, userId);
}

export async function listClassQuizzes(classId, userId) {
  const payload = await getJson(`/classes/${classId}/quizzes`, userId);
  return payload.quizzes || [];
}

export async function getQuizDetail(quizId, userId) {
  return getJson(`/quizzes/${quizId}`, userId);
}

export async function getQuizAttempts(quizId, userId) {
  const payload = await getJson(`/quizzes/${quizId}/attempts`, userId);
  return payload.rows || [];
}

export const DEMO_ACCOUNTS = [
  { username: "alice", password: "alice123", displayName: "Alice Nguyen", role: "student" },
  { username: "brian", password: "brian123", displayName: "Brian Tran", role: "tutor" },
  { username: "clara", password: "clara123", displayName: "Clara Le", role: "student" },
  { username: "david", password: "david123", displayName: "David Vo", role: "student" },
  { username: "emma", password: "emma123", displayName: "Emma Pham", role: "tutor" },
];
