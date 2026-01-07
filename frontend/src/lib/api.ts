// API Client for frontend

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface RequestOptions {
  method?: string;
  body?: Record<string, unknown>;
  requiresAuth?: boolean;
}

async function request<T>(endpoint: string, options: RequestOptions = {}): Promise<T> {
  const { method = "GET", body, requiresAuth = false } = options;

  const headers: HeadersInit = {
    "Content-Type": "application/json",
  };

  if (requiresAuth) {
    const token = document.cookie
      .split("; ")
      .find((row) => row.startsWith("auth_token="))
      ?.split("=")[1];

    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    method,
    headers,
    credentials: "include",
    body: body ? JSON.stringify(body) : undefined,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    const message = errorData.error?.message || "An error occurred";
    throw new Error(message);
  }

  // Handle 204 No Content
  if (response.status === 204) {
    return {} as T;
  }

  return response.json();
}

// Auth API
export const authApi = {
  signup: (email: string, password: string) =>
    request<{ message: string; user: { id: number; email: string } }>("/auth/signup", {
      method: "POST",
      body: { email, password },
    }),

  signin: (email: string, password: string) =>
    request<{ message: string; token: string; user: { id: number; email: string } }>(
      "/auth/signin",
      {
        method: "POST",
        body: { email, password },
      }
    ),

  signout: () =>
    request<{ message: string }>("/auth/signout", {
      method: "POST",
    }),

  me: () =>
    request<{ user: { id: number; email: string; created_at: string } }>("/auth/me", {
      requiresAuth: true,
    }),
};

// Todo API
export interface Todo {
  id: number;
  user_id: number;
  title: string;
  is_complete: boolean;
  created_at: string;
  updated_at: string;
}

export const todoApi = {
  list: () =>
    request<{ todos: Todo[]; count: number }>("/todos", {
      requiresAuth: true,
    }),

  get: (id: number) =>
    request<Todo>(`/todos/${id}`, {
      requiresAuth: true,
    }),

  create: (title: string) =>
    request<Todo>("/todos", {
      method: "POST",
      body: { title },
      requiresAuth: true,
    }),

  update: (id: number, title: string) =>
    request<Todo>(`/todos/${id}`, {
      method: "PUT",
      body: { title },
      requiresAuth: true,
    }),

  delete: (id: number) =>
    request<Record<string, never>>(`/todos/${id}`, {
      method: "DELETE",
      requiresAuth: true,
    }),

  toggle: (id: number, is_complete: boolean) =>
    request<Todo>(`/todos/${id}/toggle`, {
      method: "PATCH",
      body: { is_complete },
      requiresAuth: true,
    }),
};
