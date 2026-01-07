"use client";

import { useState, useEffect } from "react";
import { useAuth } from "@/lib/auth";
import { todoApi, Todo } from "@/lib/api";
import { TodoList } from "@/components/TodoList";
import { TodoInput } from "@/components/TodoInput";

export default function TodosPage() {
  const { user } = useAuth();
  const [todos, setTodos] = useState<Todo[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchTodos = async () => {
    try {
      const response = await todoApi.list();
      setTodos(response.todos);
      setError("");
    } catch (err) {
      setError("Failed to load todos");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchTodos();
  }, []);

  const handleTodoUpdate = () => {
    fetchTodos();
  };

  if (isLoading) {
    return <div className="loading">Loading todos...</div>;
  }

  return (
    <div>
      <p style={{ marginBottom: "16px", color: "var(--text-secondary)" }}>
        Welcome, {user?.email}
      </p>

      <TodoInput onAdd={handleTodoUpdate} />

      {error && <p className="error-message" style={{ marginBottom: "16px" }}>{error}</p>}

      <TodoList todos={todos} onUpdate={handleTodoUpdate} />
    </div>
  );
}
