export default function HeroIllustration() {
  return (
    <svg viewBox="0 0 500 500" className="w-full max-w-md" xmlns="http://www.w3.org/2000/svg">
      {/* Hand outline paths */}
      <path d="M 150 200 Q 180 150, 220 140 Q 240 135, 260 145" stroke="#000000" strokeWidth="3" fill="none" />
      <path d="M 180 220 Q 210 160, 250 150 Q 270 145, 285 160" stroke="#000000" strokeWidth="3" fill="none" />
      <path d="M 200 240 Q 230 180, 270 175 Q 290 172, 300 190" stroke="#000000" strokeWidth="3" fill="none" />
      <path d="M 215 265 Q 240 210, 280 210 Q 300 210, 310 225" stroke="#000000" strokeWidth="3" fill="none" />
      
      {/* Palm shape */}
      <path d="M 120 280 Q 150 250, 200 260 Q 250 270, 280 300 Q 270 350, 200 360 Q 130 365, 110 320 Z" fill="none" stroke="#000000" strokeWidth="2" />
      
      {/* Green geometric shape - main accent */}
      <polygon points="200,200 280,260 240,350 160,300" fill="#B9FF66" opacity="0.9" />
      
      {/* Decorative circles and dots */}
      <circle cx="220" cy="180" r="15" fill="#000000" />
      <circle cx="320" cy="240" r="12" fill="#000000" />
      <circle cx="380" cy="290" r="10" fill="#B9FF66" />
      <circle cx="150" cy="100" r="8" fill="#B9FF66" />
      <circle cx="420" cy="360" r="6" fill="#000000" />
      
      {/* Star/diamond shapes */}
      <polygon points="250,450 255,465 270,465 260,475 265,490 250,480 235,490 240,475 230,465 245,465" fill="#000000" />
      
      {/* Accent lines */}
      <line x1="300" y1="150" x2="350" y2="200" stroke="#B9FF66" strokeWidth="3" />
      <line x1="100" y1="350" x2="80" y2="400" stroke="#B9FF66" strokeWidth="2" />
    </svg>
  );
}
