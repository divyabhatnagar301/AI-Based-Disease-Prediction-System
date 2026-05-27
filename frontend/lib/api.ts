const API_BASE =
  process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, "") || "http://localhost:5000";

export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public body?: unknown
  ) {
    super(message);
    this.name = "ApiError";
  }
}

async function request<T>(
  path: string,
  options: RequestInit = {},
  token?: string | null
): Promise<T> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string>),
  };
  if (token) headers.Authorization = `Bearer ${token}`;

  const res = await fetch(`${API_BASE}${path}`, { ...options, headers });
  const data = await res.json().catch(() => ({}));

  if (!res.ok) {
    const msg =
      (data as { error?: string }).error ||
      `Request failed (${res.status})`;
    throw new ApiError(msg, res.status, data);
  }
  return data as T;
}

export const api = {
  baseUrl: API_BASE,

  health: () => request<HealthResponse>("/api/health"),

  signup: (body: SignupBody) =>
    request<AuthResponse>("/api/auth/signup", {
      method: "POST",
      body: JSON.stringify(body),
    }),

  signin: (body: SigninBody) =>
    request<AuthResponse>("/api/auth/signin", {
      method: "POST",
      body: JSON.stringify(body),
    }),

  profile: (token: string) =>
    request<{ user: User }>("/api/auth/profile", {}, token),

  modelsInfo: () => request<{ models: Record<string, ModelInfo> }>("/api/models/info"),

  modelFeatures: (diseaseType: string) =>
    request<ModelFeaturesResponse>(`/api/models/${diseaseType}/features`),

  predict: (endpoint: string, body: Record<string, unknown>, token: string) =>
    request<PredictionResponse>(endpoint, {
      method: "POST",
      body: JSON.stringify(body),
    }, token),

  predictions: (token: string, params?: { disease_type?: string; limit?: number }) => {
    const q = new URLSearchParams();
    if (params?.disease_type) q.set("disease_type", params.disease_type);
    if (params?.limit) q.set("limit", String(params.limit));
    const qs = q.toString() ? `?${q}` : "";
    return request<{ predictions: PredictionRecord[]; count: number }>(
      `/api/predictions${qs}`,
      {},
      token
    );
  },

  prediction: (id: number, token: string) =>
    request<PredictionRecord>(`/api/predictions/${id}`, {}, token),

  deletePrediction: (id: number, token: string) =>
    request<{ message: string }>(`/api/predictions/${id}`, { method: "DELETE" }, token),
};

export type User = {
  id: number;
  username: string;
  email: string;
  full_name: string;
  created_at?: string;
};

export type AuthResponse = {
  message: string;
  token: string;
  user: User;
};

export type SignupBody = {
  username: string;
  email: string;
  password: string;
  full_name?: string;
};

export type SigninBody = {
  username: string;
  password: string;
};

export type HealthResponse = {
  status: string;
  models_loaded: Record<string, boolean>;
  database?: string;
};

export type ModelInfo = {
  model_name: string;
  accuracy: number;
  feature_names: string[];
  feature_count: number;
  loaded: boolean;
};

export type ModelFeaturesResponse = {
  disease_type: string;
  feature_names?: string[];
  feature_descriptions?: Record<string, string>;
  input_type?: string;
  sequence_length?: number;
  class_names?: string[];
  model_accuracy?: number;
};

export type PredictionResponse = {
  prediction: string;
  probability: number;
  prediction_code?: number;
  model_accuracy?: number;
  input_features?: Record<string, unknown>;
  class_names?: string[];
  probabilities?: number[];
  sequence_length?: number;
};

export type PredictionRecord = {
  id: number;
  disease_type: string;
  input_data: Record<string, unknown>;
  prediction_result: string;
  prediction_probability: number;
  created_at: string;
};
