import { Hero } from "@/components/landing/Hero";
import { StatsBar } from "@/components/landing/StatsBar";
import { ModelGrid } from "@/components/landing/ModelGrid";
import { Features } from "@/components/landing/Features";
import { HowItWorks } from "@/components/landing/HowItWorks";
import { ApiReference } from "@/components/landing/ApiReference";
import { CTA } from "@/components/landing/CTA";

export default function HomePage() {
  return (
    <>
      <Hero />
      <StatsBar />
      <ModelGrid />
      <Features />
      <HowItWorks />
      <ApiReference />
      <CTA />
    </>
  );
}
