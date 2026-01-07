"use client";

import { useState } from "react";
import { Todo } from "@/lib/api";
import { todoApi } from "@/lib/api";

interface TodoItemProps {
  todo: Todo;
  onUpdate: () => void;
}

export function TodoItem({ todo, onUpdate }: TodoItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(todo.title);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const handleToggle = async () => {
    try {
      await todoApi.toggle(todo.id, !todo.is_complete);
      onUpdate();
    } catch (err) {
      setError("Failed to update todo");
    }
  };

  const handleSave = async () => {
    if (!editTitle.trim()) {
      setError("Title cannot be empty");
      return;
    }

    setIsLoading(true);
    try {
      await todoApi.update(todo.id, editTitle);
      setIsEditing(false);
      onUpdate();
    } catch (err) {
      setError("Failed to update todo");
    } finally {
      setIsLoading(false);
    }
  };

  const handleCancel = () => {
    setEditTitle(todo.title);
    setIsEditing(false);
    setError("");
  };

  const handleDelete = async () => {
    if (!confirm("Are you sure you want to delete this todo?")) return;

    setIsLoading(true);
    try {
      await todoApi.delete(todo.id);
      onUpdate();
    } catch (err) {
      setError("Failed to delete todo");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <li className={`todo-item ${todo.is_complete ? "completed" : ""}`}>
      <input
        type="checkbox"
        className="todo-checkbox"
        checked={todo.is_complete}
        onChange={handleToggle}
        disabled={isLoading}
      />

      {isEditing ? (
        <div style={{ flex: 1, display: "flex", flexDirection: "column", gap: "8px" }}>
          <input
            type="text"
            className="input"
            value={editTitle}
            onChange={(e) => setEditTitle(e.target.value)}
            autoFocus
          />
          {error && <p className="error-message">{error}</p>}
          <div style={{ display: "flex", gap: "8px" }}>
            <button className="btn btn-primary" onClick={handleSave} disabled={isLoading}>
              Save
            </button>
            <button className="btn btn-secondary" onClick={handleCancel} disabled={isLoading}>
              Cancel
            </button>
          </div>
        </div>
      ) : (
        <>
          <span className="todo-title">{todo.title}</span>
          <div className="todo-actions">
            <button
              className="btn btn-ghost"
              onClick={() => setIsEditing(true)}
              disabled={isLoading}
              title="Edit"
            >
              Edit
            </button>
            <button
              className="btn btn-ghost"
              onClick={handleDelete}
              disabled={isLoading}
              title="Delete"
            >
              Delete
            </button>
          </div>
        </>
      )}
    </li>
  );
}
