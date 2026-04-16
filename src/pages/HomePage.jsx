import Navigation from '@/components/Navigation';
import HeroSection from '@/components/HeroSection';
import ServicesSection from '@/components/ServicesSection';

export default function HomePage() {
  return (
    <div className="w-full">
      <Navigation />
      <HeroSection />
      <ServicesSection />
    </div>
  );
}
