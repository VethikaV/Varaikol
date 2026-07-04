import { useEffect, useRef } from "react";
import "./style.css";
import homepageGif from "../assets/homepage.gif";

const features = [
  {
    id: 1,
    tag: "Inspire",
    title: "What Can I Draw?",
    desc: "Describe anything — get three AI-generated drawing ideas with reference images, difficulty levels, and tips.",
    cta: "Get Ideas",
    preview: (
      <div className="card-preview ideas-preview">
        <div className="preview-input-mock">
          <span>a butterfly...</span>
          <div className="preview-btn-mock">Get Ideas</div>
        </div>
        <div className="preview-images-mock">
          <div className="prev-img easy">Easy</div>
          <div className="prev-img medium">Medium</div>
          <div className="prev-img hard">Hard</div>
        </div>
      </div>
    ),
  },
  {
    id: 2,
    tag: "Transform",
    title: "Photo to Sketch",
    desc: "Upload any photo and get a clean pencil outline in seconds. Perfect as a tracing base or reference.",
    cta: "Convert Photo",
    preview: (
      <div className="card-preview sketch-preview">
        <div className="sketch-mock-wrap">
          <div className="sketch-mock original">
            <div className="mock-label">Photo</div>
            <div className="mock-img-block photo-block" />
          </div>
          <div className="arrow-mock">→</div>
          <div className="sketch-mock result">
            <div className="mock-label">Sketch</div>
            <div className="mock-img-block sketch-block" />
          </div>
        </div>
      </div>
    ),
  },
  {
    id: 3,
    tag: "Improve",
    title: "Analyze My Drawing",
    desc: "Upload your artwork and receive AI feedback on medium, style, and specific tips to improve.",
    cta: "Analyze Drawing",
    preview: (
      <div className="card-preview analyze-preview">
        <div className="analyze-mock-img" />
        <div className="analyze-mock-result">
          <div className="mock-result-row">
            <span className="mock-dot" />
            <span>Medium: Pencil Shading</span>
          </div>
          <div className="mock-result-row">
            <span className="mock-dot" />
            <span>Style: Realistic Sketch</span>
          </div>
          <div className="mock-result-row muted">
            <span className="mock-dot" />
            <span>Improve shading on cheeks</span>
          </div>
          <div className="mock-result-row muted">
            <span className="mock-dot" />
            <span>Work on eye proportions</span>
          </div>
        </div>
      </div>
    ),
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
      <section className="features-section">
        <p className="features-eyebrow">Three ways to help you draw</p>
        <div className="features-grid">
          {features.map((f, i) => (
            <div
              key={f.id}
              className="feat-card"
              ref={(el) => (cardsRef.current[i] = el)}
              onClick={() => setTab(f.id)}
            >
              {/* Preview area at top */}
              <div className="feat-card-preview">{f.preview}</div>

              {/* Text at bottom */}
              <div className="feat-card-body">
                <span className="feat-tag">{f.tag}</span>
                <h3 className="feat-title">{f.title}</h3>
                <p className="feat-desc">{f.desc}</p>
                <span className="feat-cta">
                  {f.cta} <span className="feat-arrow">↗</span>
                </span>
              </div>
            </div>
          ))}
        </div>
      </section>

      
    </div>
  );
}