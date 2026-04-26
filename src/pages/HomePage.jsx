import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Navigation from '@/components/Navigation';
import HeroSection from '@/components/HeroSection';
import ServicesSection from '@/components/ServicesSection';
import { fetchCurrentUser, loadStoredUser } from "@/lib/api";

export default function HomePage() {
  const navigate = useNavigate();

  useEffect(() => {
    const checkSession = async () => {
      const stored = loadStoredUser();
      if (!stored) return;

      const user = await fetchCurrentUser(stored.id);
      if (user) {
        navigate("/grammar", { replace: true });
      }
    };
    checkSession();
  }, [navigate]);

  return (
    <div className="w-full">
      <Navigation />
      <HeroSection />
      <ServicesSection />
    </div>
  );
}
