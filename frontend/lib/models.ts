import {
  Activity,
  Droplets,
  Heart,
  HeartPulse,
  type LucideIcon,
} from "lucide-react";

export type ModelConfig = {
  id: string;
  slug: string;
  apiType: string;
  name: string;
  shortName: string;
  description: string;
  endpoint: string;
  featuresEndpoint: string;
  color: string;
  gradient: string;
  icon: LucideIcon;
  sampleHint: string;
};

export const MODELS: ModelConfig[] = [
  {
    id: "diabetes",
    slug: "diabetes",
    apiType: "diabetes",
    name: "Diabetes Prediction",
    shortName: "Diabetes",
    description:
      "Random Forest model analyzing glucose, HbA1c, BMI, and lifestyle factors.",
    endpoint: "/api/predict/diabetes",
    featuresEndpoint: "/api/models/diabetes/features",
    color: "text-teal-600",
    gradient: "from-teal-500 to-emerald-600",
    icon: Activity,
    sampleHint: "8 clinical & lifestyle features",
  },
  {
    id: "heart",
    slug: "heart",
    apiType: "heart",
    name: "Heart Disease",
    shortName: "Heart",
    description:
      "Cardiovascular risk assessment using 13 standard cardiac indicators.",
    endpoint: "/api/predict/heart",
    featuresEndpoint: "/api/models/heart/features",
    color: "text-rose-600",
    gradient: "from-rose-500 to-pink-600",
    icon: Heart,
    sampleHint: "13 cardiac measurements",
  },
  {
    id: "kidney",
    slug: "kidney",
    apiType: "kidney",
    name: "Kidney Disease",
    shortName: "Kidney",
    description:
      "Logistic regression on urinalysis, renal function, and metabolic markers.",
    endpoint: "/api/predict/kidney",
    featuresEndpoint: "/api/models/kidney/features",
    color: "text-sky-600",
    gradient: "from-sky-500 to-blue-600",
    icon: Droplets,
    sampleHint: "29 renal & metabolic features",
  },
  {
    id: "liver",
    slug: "liver",
    apiType: "liver",
    name: "Liver Disease",
    shortName: "Liver",
    description:
      "XGBoost classifier using bilirubin, enzymes, and protein panel values.",
    endpoint: "/api/predict/liver",
    featuresEndpoint: "/api/models/liver/features",
    color: "text-amber-600",
    gradient: "from-amber-500 to-orange-600",
    icon: Activity,
    sampleHint: "10 liver panel features",
  },
  {
    id: "heart_ecg",
    slug: "heart-ecg",
    apiType: "heart_ecg",
    name: "Heart ECG (LSTM)",
    shortName: "ECG",
    description:
      "Deep learning LSTM classifies 187-sample ECG segments into heartbeat types.",
    endpoint: "/api/predict/heart-ecg",
    featuresEndpoint: "/api/models/heart_ecg/features",
    color: "text-violet-600",
    gradient: "from-violet-500 to-purple-600",
    icon: HeartPulse,
    sampleHint: "187-point ECG waveform",
  },
];

export const API_ENDPOINTS = [
  { method: "POST", path: "/api/auth/signup", auth: false, tag: "Auth" },
  { method: "POST", path: "/api/auth/signin", auth: false, tag: "Auth" },
  { method: "GET", path: "/api/auth/profile", auth: true, tag: "Auth" },
  { method: "POST", path: "/api/predict/diabetes", auth: true, tag: "Predict" },
  { method: "POST", path: "/api/predict/heart", auth: true, tag: "Predict" },
  { method: "POST", path: "/api/predict/kidney", auth: true, tag: "Predict" },
  { method: "POST", path: "/api/predict/liver", auth: true, tag: "Predict" },
  { method: "POST", path: "/api/predict/heart-ecg", auth: true, tag: "Predict" },
  { method: "GET", path: "/api/predictions", auth: true, tag: "History" },
  { method: "GET", path: "/api/predictions/:id", auth: true, tag: "History" },
  { method: "DELETE", path: "/api/predictions/:id", auth: true, tag: "History" },
  { method: "GET", path: "/api/models/info", auth: false, tag: "Models" },
  { method: "GET", path: "/api/models/:type/features", auth: false, tag: "Models" },
  { method: "GET", path: "/api/health", auth: false, tag: "System" },
];

export function getModelBySlug(slug: string): ModelConfig | undefined {
  return MODELS.find((m) => m.slug === slug);
}

export const SAMPLE_VALUES: Record<string, Record<string, number>> = {
  diabetes: {
    gender: 0,
    age: 45,
    hypertension: 0,
    heart_disease: 0,
    smoking_history: 4,
    bmi: 25.5,
    HbA1c_level: 5.5,
    blood_glucose_level: 100,
  },
  heart: {
    age: 63,
    sex: 1,
    cp: 3,
    trestbps: 145,
    chol: 233,
    fbs: 1,
    restecg: 0,
    thalach: 150,
    exang: 0,
    oldpeak: 2.3,
    slope: 0,
    ca: 0,
    thal: 1,
  },
  kidney: {
    "Age of the patient": 48,
    "Blood pressure (mm/Hg)": 80,
    "Specific gravity of urine": 1.02,
    "Albumin in urine": 0,
    "Sugar in urine": 0,
    "Random blood glucose level (mg/dl)": 121,
    "Blood urea (mg/dl)": 36,
    "Serum creatinine (mg/dl)": 1.2,
    "Sodium level (mEq/L)": 142,
    "Potassium level (mEq/L)": 4.5,
    "Hemoglobin level (gms)": 15,
    "Packed cell volume (%)": 44,
    "White blood cell count (cells/cumm)": 7800,
    "Red blood cell count (millions/cumm)": 5.2,
    "Estimated Glomerular Filtration Rate (eGFR)": 90,
    "Urine protein-to-creatinine ratio": 0.15,
    "Urine output (ml/day)": 1500,
    "Serum albumin level": 4.5,
    "Cholesterol level": 200,
    "Parathyroid hormone (PTH) level": 35,
    "Serum calcium level": 9.5,
    "Serum phosphate level": 3.5,
    "Body Mass Index (BMI)": 25,
    "Duration of diabetes mellitus (years)": 0,
    "Duration of hypertension (years)": 0,
    "Cystatin C level": 0.8,
    "C-reactive protein (CRP) level": 2,
    "Interleukin-6 (IL-6) level": 5,
    Appetite: 1,
  },
  liver: {
    "Age of the patient": 65,
    "Gender of the patient": 1,
    "Total Bilirubin": 0.7,
    "Direct Bilirubin": 0.1,
    "\u00a0Alkphos Alkaline Phosphotase": 187,
    "\u00a0Sgpt Alamine Aminotransferase": 16,
    "Sgot Aspartate Aminotransferase": 18,
    "Total Protiens": 6.8,
    "\u00a0ALB Albumin": 3.3,
    "A/G Ratio Albumin and Globulin Ratio": 0.9,
  },
};

export function generateDemoEcg(length = 187): number[] {
  const signal: number[] = [];
  for (let i = 0; i < length; i++) {
    const t = i / length;
    const base = 0.02 * Math.sin(2 * Math.PI * 8 * t);
    const spike =
      i % 23 === 0 ? 0.8 * Math.exp(-((i % 23) ** 2) / 8) : 0;
    const noise = (Math.random() - 0.5) * 0.04;
    signal.push(Number((base + spike + noise).toFixed(4)));
  }
  return signal;
}
