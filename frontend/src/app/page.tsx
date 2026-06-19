import ChatInterface from "@/components/ChatInterface";
import TranslatorPanel from "@/components/TranslatorPanel";
import QuickQuestions from "@/components/QuickQuestions";

export default function Home() {
  return (
    <main className="min-h-screen bg-[#f7f3ec] p-4 md:p-8">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-6">
          <h1 className="text-3xl font-bold text-kabye-blue mb-1">
            Agronome Kabyè
          </h1>
          <p className="text-kabye-gold font-medium text-lg">Tee cee kɛɛ Kabyè — Togo Nord</p>
          <p className="text-gray-500 text-sm mt-1">Agronome IA · Parle et comprend le kabyè</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          <div className="lg:col-span-2 bg-white rounded-2xl shadow-sm border border-kabye-sand h-[650px] flex flex-col overflow-hidden">
            <ChatInterface />
          </div>

          <div className="space-y-4">
            <TranslatorPanel />

            <div className="bg-kabye-blue text-white rounded-2xl p-4 text-sm">
              <h3 className="font-semibold text-kabye-gold mb-2">Capacités / Tazmert</h3>
              <ul className="space-y-1.5 text-blue-100 text-xs">
                <li>🌿 Conseil agricole en kabyè</li>
                <li>🫒 Ignames, sorgho, coton (Togo Nord)</li>
                <li>💧 Irrigation &amp; gestion de l&apos;eau</li>
                <li>🌱 Semences &amp; calendrier cultural</li>
                <li>🦟 Maladies &amp; ravageurs des cultures</li>
                <li>🔄 Traduction FR ↔ Kabyè</li>
                <li>📖 Corpus kabyè (calendrier + données agro)</li>
              </ul>
            </div>

            <QuickQuestions />
          </div>
        </div>
      </div>
    </main>
  );
}
