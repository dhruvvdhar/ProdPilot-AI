import axios, { type AxiosError } from "axios";
import { tokenStorage } from "@/lib/tokenStorage";

export const API_BASE_URL: string =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

apiClient.interceptors.request.use((config) => {
  const token = tokenStorage.get();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

/** Normalized shape every API error is coerced into. */
export class ApiError extends Error {
  status: number | undefined;
  errors: string[] | undefined;

  constructor(message: string, status?: number, errors?: string[]) {
    super(message);
    this.status = status;
    this.errors = errors;
  }
}

let onUnauthorized: (() => void) | null = null;

/** Registered once by AuthContext so a 401 anywhere logs the user out. */
export function registerUnauthorizedHandler(handler: () => void) {
  onUnauthorized = handler;
}

apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError<{ message?: string; errors?: string[]; detail?: string }>) => {
    const status = error.response?.status;
    const body = error.response?.data;

    const message =
      body?.message ||
      body?.detail ||
      error.message ||
      "Something went wrong. Please try again.";

    if (status === 401) {
      tokenStorage.clear();
      onUnauthorized?.();
    }

    return Promise.reject(new ApiError(message, status, body?.errors));
  },
);
