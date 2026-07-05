import { useEffect, useRef } from "react";
import "./style.css";
import homepageGif from "../assets/homepage.gif";

import { Lightbulb, Image, ScanSearch } from "lucide-react";

const features = [
  {
    id: 1,
    icon: <Lightbulb size={32} />,
    tag: "Inspire",
    title: "What Can I Draw?",
    desc: "Describe anything and receive AI-generated drawing ideas with reference images, difficulty levels, and creative tips.",
    cta: "Get Ideas",
    tab: 1,
  },
  {
    id: 2,
    icon: <Image size={32} />,
    tag: "Transform",
    title: "Photo to Sketch",
    desc: "Convert any photo into a clean pencil sketch.",
    cta: "Convert Photo",
    tab: 2,
  },
  {
    id: 3,
    icon: <ScanSearch size={32} />,
    tag: "Improve",
    title: "Analyze My Drawing",
    desc: "Upload artwork and get AI feedback.",
    cta: "Analyze Drawing",
    tab: 3,
  },
];

export default function HomePage({ setTab }) {
  const cardsRef = useRef([]);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => e.isIntersecting && e.target.classList.add("visible"));
      },
      { threshold: 0.1 }
    );
    cardsRef.current.forEach((el) => el && observer.observe(el));
    return () => observer.disconnect();
  }, []);

  return (
    <div className="home">

      {/* ── Nav ── */}
      <nav className="home-nav">
        <span className="home-nav-logo">வரைகோல்</span>
        <button className="home-nav-btn" onClick={() => setTab(0)}>
          Start Drawing
        </button>
      </nav>

      {/* ── Hero ── */}
      <section className="hero">
        <div className="hero-left">
          <p className="hero-tamil">Every Masterpiece</p>
          <h1 className="hero-title">
           வரைகோல் <br />
            <em>Begins with a Line</em>
          </h1>
          <p className="hero-sub">
            Your AI-powered drawing companion — get ideas, convert photos to
            sketches, and receive expert feedback on your artwork.
          </p>
          <button className="hero-cta" onClick={() => setTab(0)}>
            Start Creating →
          </button>
        </div>
       <div className="hero-right">
           <img
          src={homepageGif}
          alt="AI Drawing Assistant"
         className="hero-image"
         />
</div>
      </section>

      {/* ── Cards ── */}
      <div className="features-grid">
  {features.map((feature) => (
    <div className="feature-card" key={feature.id}>
      
      <div className="feature-icon">{feature.icon}</div>

      <span className="feature-tag">{feature.tag}</span>

      <h3>{feature.title}</h3>

      <p>{feature.desc}</p>

      <button
        className="feature-btn"
        onClick={() => setTab(feature.tab)}
      >
        {feature.cta}
      </button>

    </div>
  ))}
</div>
      
    </div>
  );
}