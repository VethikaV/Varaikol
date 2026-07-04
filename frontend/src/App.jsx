import { useState } from "react";
import { Home, Lightbulb, PenTool, Search } from "lucide-react";
import HomePage from "./pages/HomePage";
import IdeasPage from "./pages/IdeasPage";
import SketchPage from "./pages/SketchPage";
import AnalyzePage from "./pages/AnalyzePage";
import Navbar from "./components/Navbar";

const tabs = [
  { label: "Home", icon: Home },
  { label: "Ideas", icon: Lightbulb },
  { label: "Sketch", icon: PenTool },
  { label: "Analyze", icon: Search },
];

export default function App() {
  const [tab, setTab] = useState(0);

  const handleTabChange = (value) => {
    const numericValue = Number(value);
    setTab(isNaN(numericValue) ? 0 : numericValue);
  };

  return (
    <div className="app">
      {tab === 0 ? (
        <HomePage setTab={handleTabChange} />
      ) : (
        <>
          <div className="app-header">
            <span className="app-logo" onClick={() => handleTabChange(0)}>
            வரைகோல்
            </span>
            <Navbar active={tab} setActive={handleTabChange} tabs={tabs} />
          </div>

          {tab === 1 && <IdeasPage />}
          {tab === 2 && <SketchPage />}
          {tab === 3 && <AnalyzePage />}
        </>
      )}
    </div>
  );
}