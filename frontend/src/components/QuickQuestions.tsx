"use client";

const QUESTIONS = [
  "Amek ara aberreɣ uzemmur?",
  "Iman n tsaliḥt n iɣessiren",
  "Comment traiter les parasites de l'olivier?",
  "Calendrier de semailles kabyle",
];

export default function QuickQuestions() {
  const fill = (q: string) => {
    const el = document.querySelector("textarea");
    if (!el) return;
    const setter = Object.getOwnPropertyDescriptor(
      window.HTMLTextAreaElement.prototype,
      "value"
    )?.set;
    setter?.call(el, q);
    el.dispatchEvent(new Event("input", { bubbles: true }));
    el.focus();
  };

  return (
    <div className="bg-white rounded-2xl border border-kabyle-sand p-4">
      <h3 className="text-kabyle-blue font-semibold text-xs mb-2">Questions rapides</h3>
      <div className="space-y-1.5 text-xs">
        {QUESTIONS.map((q) => (
          <button
            key={q}
            className="w-full text-left px-2 py-1.5 bg-kabyle-sand rounded-lg text-gray-700 hover:bg-kabyle-gold hover:text-white transition-colors"
            onClick={() => fill(q)}
          >
            {q}
          </button>
        ))}
      </div>
    </div>
  );
}
