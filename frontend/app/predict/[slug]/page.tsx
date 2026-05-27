import { notFound } from "next/navigation";
import { PredictionForm } from "@/components/predict/PredictionForm";
import { getModelBySlug } from "@/lib/models";

type Props = { params: Promise<{ slug: string }> };

export default async function PredictPage({ params }: Props) {
  const { slug } = await params;
  if (!getModelBySlug(slug)) notFound();

  return (
    <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
      <PredictionForm slug={slug} />
    </div>
  );
}
