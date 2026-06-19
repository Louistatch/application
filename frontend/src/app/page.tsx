import ChatInterface from "@/components/ChatInterface";
import TranslatorPanel from "@/components/TranslatorPanel";

export default function Home() {
  return (
    <main className="min-h-screen bg-[#f7f3ec] p-4 md:p-8">
      <div className="max-w-6xl mx-auto">
        {/* Hero */}
        <div className="text-center mb-6">
          <h1 className="text-3xl font-bold text-kabyle-blue mb-1">
            ⴰⵎⵣⴰⵔⵓⴳ ⴰⵇⴱⴰⵢⵍⵉ
          </h1>
          <p className="text-kabyle-gold font-medium text-lg">Amẓarug Aqbayli n Tẓuṛt n Wakal</p>
          <p className="text-gray-500 text-sm mt-1">Agronome IA · Parle et comprend le kabyle</p>
        </div>

        {/* Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          {/* Chat - 2/3 */}
          <div className="lg:col-span-2 bg-white rounded-2xl shadow-sm border border-kabyle-sand h-[650px] flex flex-col overflow-hidden">
            <ChatInterface />
          </div>

          {/* Sidebar - 1/3 */}
          <div className="space-y-4">
            <TranslatorPanel />

            {/* Info card */}
            <div className="bg-kabyle-blue text-white rounded-2xl p-4 text-sm">
              <h3 className="font-semibold text-kabyle-gold mb-2">Capacités / Tazmert</h3>
              <ul className="space-y-1.5 text-blue-100 text-xs">
                <li>🌿 Conseil agricole en kabyle</li>
                <li>🫒 Oliviers, figuiers, vigne kabyle</li>
                <li>💧 Irrigation & gestion de l'eau</li>
                <li>🌱 Semences & calendrier cultural</li>
                <li>🦟 Maladies & ravageurs des cultures</li>
                <li>🔄 Traduction FR ↔ Taqbaylit</li>
                <li>📖 Corpus kabyle (dictionnaire + Bible)</li>
              </ul>
            </div>

            {/* Quick questions */}
            <div className="bg-white rounded-2xl border border-kabyle-sand p-4">
              <h3 className="text-kabyle-blue font-semibold text-xs mb-2">Questions rapides</h3>
              <div className="space-y-1.5 text-xs">
                {[
                  "Amek ara aberreɣ uzemmur?",
                  "Iman n tsaliḥt n iɣessiren",
                  "Comment traiter les parasites de l'olivier?",
                  "Calendrier de semailles kabyle",
                ].map((q) => (
                  <button
                    key={q}
                    className="w-full text-left px-2 py-1.5 bg-kabyle-sand rounded-lg text-gray-700 hover:bg-kabyle-gold hover:text-white transition-colors"
                    onClick={() => {
                      const el = document.querySelector("textarea");
                      if (el) {
                        const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
                          window.HTMLTextAreaElement.prototype, "value"
                        )?.set;
                        nativeInputValueSetter?.call(el, q);
                        el.dispatchEvent(new Event("input", { bubbles: true }));
                        el.focus();
                      }
                    }}
                  >
                    {q}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
