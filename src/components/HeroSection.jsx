import { Button } from '@/components/ui/button';
import HeroIllustration from './HeroIllustration';
import heroStar from '@/assets/hero_star.svg';

export default function HeroSection() {
  return (
    <section style={{
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      padding: '70px 100px 80px 100px',
      backgroundColor: '#FFFFFF',
    }}>
      {/* Left Content */}
      <div style={{
        flex: 1,
        display: 'flex',
        flexDirection: 'column'
      }}>
        <h1 style={{
          fontSize: '4rem',
          fontWeight: '500',
          color: '#000000',
          top: '0',
          lineHeight: '1.2'
        }}>
          Write better<br />English, instantly.
        </h1>
        
        <p style={{
          fontSize: '1.125rem',
          color: '#000000',
          marginBottom: '32px',
          lineHeight: '1.6',
          fontWeight: '400'
        }}>
          Our grammar checker identifies errors and suggests improvements in real-time. Whether it's an essay, an email, or a report, ensure your writing is always professional and error-free.
        </p>
        
        <Button 
          style={{
            backgroundColor: '#000000',
            color: '#FFFFFF',
            border: '2px solid #000000',
            padding: '12px 32px',
            fontSize: '1rem',
            borderRadius: '14px',
            fontWeight: '500',
            width: 'fit-content',
            cursor: 'pointer'
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.backgroundColor = '#191A23';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.backgroundColor = '#000000';
          }}
        >
          Check your text now
        </Button>
      </div>

      {/* Right Illustration */}
      <div style={{
        flex: 1,
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        position: 'relative'
      }}>
        <div style={{
          width: '100%',
          position: 'relative'
        }}>
          <div style={{
            position: 'absolute',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            zIndex: 10,
            userSelect: 'none',
            pointerEvents: 'none'
          }}>
            <img
              src={heroStar}
              alt="Floating star"
              className="hero-star"
              style={{
                width: '100%',
                display: 'block',
              }}
            />
          </div>
          <div style={{
            width: '100%',
            userSelect: 'none',
            pointerEvents: 'none'
          }}>
            <HeroIllustration />
          </div>
        </div>
      </div>
    </section>
  );
}
