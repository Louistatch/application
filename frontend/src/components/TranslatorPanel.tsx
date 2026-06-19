"use client";
import { useState } from "react";
import { ArrowLeftRight, Loader2 } from "lucide-react";
import { translate } from "@/lib/api";

export default function TranslatorPanel() {
  const [inputText, setInputText] = useState("");
  const [outputText, setOutputText] = useState("");
  const [direction, setDirection] = useState<"fr_to_kab" | "kab_to_fr">("fr_to_kab");
  const [loading, setLoading] = useState(false);

  const handleTranslate = async () => {
    if (!inputText.trim()) return;
    setLoading(true);
    try {
      const result = await translate(inputText, direction);
      setOutputText(result);
    } catch (e) {
      setOutputText("Erreur de traduction. Vérifiez la connexion au serveur.");
    } finally {
      setLoading(false);
    }
  };

  const swapDirection = () => {
    setDirection((d) => (d === "fr_to_kab" ? "kab_to_fr" : "fr_to_kab"));
    setInputText(outputText);
    setOutputText(inputText);
  };

  return (
    <div className="bg-white rounded-2xl border border-kabye-sand shadow-sm p-4">
      <h2 className="text-kabye-blue font-semibold text-sm mb-3 flex items-center gap-2">
        <span>ⴰ</span> Traduction
      </h2>
      <div className="flex items-center gap-2 mb-2">
        <span className="text-xs font-medium text-gray-500 w-20">
          {direction === "fr_to_kab" ? "Français" : "Taɛrabt"}
        </span>
        <button
          onClick={swapDirection}
          className="p-1 rounded-full hover:bg-kabye-sand transition-colors"
          title="Inverser la direction"
        >
          <ArrowLeftRight size={14} className="text-kabye-blue" />
        </button>
        <span className="text-xs font-medium text-gray-500">
          {direction === "fr_to_kab" ? "Kabyè" : "Français"}
        </span>
      </div>
      <textarea
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
        placeholder={direction === "fr_to_kab" ? "Entrez le texte en français..." : "Tee cee Kabyè..."}
        className="w-full border border-gray-200 rounded-lg p-2 text-sm resize-none h-20 focus:outline-none focus:border-kabye-blue"
      />
      <button
        onClick={handleTranslate}
        disabled={loading || !inputText.trim()}
        className="w-full mt-2 bg-kabye-blue text-white text-sm py-2 rounded-lg hover:bg-opacity-90 disabled:opacity-50 flex items-center justify-center gap-2"
      >
        {loading ? <Loader2 size={14} className="animate-spin" /> : null}
        {loading ? "Traduction..." : "Traduire"}
      </button>
      {outputText && (
        <div className="mt-3 p-3 bg-kabye-sand rounded-lg text-sm text-gray-800 leading-relaxed whitespace-pre-wrap">
          {outputText}
        </div>
      )}
    </div>
  );
}
