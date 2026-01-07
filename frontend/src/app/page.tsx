"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";

export default function Home() {
  const router = useRouter();
  const { isAuthenticated, isLoading } = useAuth();

  useEffect(() => {
    if (!isLoading) {
      if (isAuthenticated) {
        router.push("/todos");
      } else {
        router.push("/signin");
      }
    }
  }, [isAuthenticated, isLoading, router]);

  return (
    <div className="container">
      <div className="loading">Loading...</div>
    </div>
  );
}
