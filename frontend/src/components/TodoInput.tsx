"use client";

import { useState } from "react";
import { todoApi } from "@/lib/api";

interface TodoInputProps {
  onAdd: () => void;
}

export function TodoInput({ onAdd }: TodoInputProps) {
  const [title, setTitle] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (!title.trim()) {
      setError("Please enter a todo title");
      return;
    }

    setIsLoading(true);
    try {
      await todoApi.create(title);
      setTitle("");
      onAdd();
    } catch (err) {
      setError("Failed to create todo");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ marginBottom: "24px" }}>
      <div style={{ display: "flex", gap: "12px" }}>
        <input
          type="text"
          className={`input ${error ? "input-error" : ""}`}
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="What needs to be done?"
          style={{ flex: 1 }}
          disabled={isLoading}
        />
        <button
          type="submit"
          className="btn btn-primary"
          disabled={isLoading}
          style={{ minWidth: "100px" }}
        >
          {isLoading ? "Adding..." : "Add"}
        </button>
      </div>
      {error && <p className="error-message">{error}</p>}
    </form>
  );
}
