import { Button } from '@/components/ui/button';
import HeroIllustration from './HeroIllustration';

export default function HeroSection() {
  return (
    <section className="flex justify-between items-center px-8 py-20 bg-light-gray min-h-screen">
      {/* Left Content */}
      <div className="flex-1 max-w-lg">
        <h1 className="text-6xl font-bold text-black mb-6 leading-tight">
          Write better<br />English, instantly.
        </h1>
        
        <p className="text-lg text-black mb-8 leading-relaxed">
          Our grammar checker identifies errors and suggests improvements in real-time. Whether it's an essay, an email, or a report, ensureyour writing is always professional and error-free.
        </p>
        
        <Button 
          className="bg-black text-light-gray hover:bg-dark border-2 border-black px-8 py-6 text-lg"
        >
          Check your text now
        </Button>
      </div>

      {/* Right Illustration */}
      <div className="flex-1 flex justify-center">
        <HeroIllustration />
      </div>
    </section>
  );
}
