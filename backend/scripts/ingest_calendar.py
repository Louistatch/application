"""
Ingestion du calendrier Kabyè 2023 (Académie Kabiyè, Togo).
"""
import sys, os, uuid
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from rag.retriever import KabyeRetriever

CALENDAR_DATA = [
    # Jours de la semaine
    ("Ñɔɔtʋ wiye (jours de la semaine) en Kabyè: KujukŸ=Dimanche, Hodo=Lundi, PiyŸ=Mardi, CùlŸ=Mercredi, SŸrŸkŸwŸŋ=Jeudi, KemeŋŸ=Vendredi, MŸzŸŋ=Samedi", {"source": "calendrier_kabye_2023", "type": "vocabulaire"}),

    # Mois
    ("Mois en Kabyè (WŸŸŋ naza 2023): KüLAŋ=Janvier, LèLAŋ=Février, LAKòò=Mars, ɔOMAŋ=Avril, AGOZA=Mai, MòSòGúM=Juin, HASòYAɔè=Juillet, KòYèNA=Août, SALAò=Septembre, ALOMA=Octobre, KAMèò=Novembre, SAòAYòò=Décembre", {"source": "calendrier_kabye_2023", "type": "vocabulaire"}),

    # Événements culturels et agricoles extraits du calendrier
    ("Janvier (KüLAŋ): PùnŸŋ kùfŸlŸŋ wiye — début de l'année. Kpou — fête locale. Lùmaŋza nÿ adùma kùyakû wiye. Sarakawa — fête importante des Kabyè.", {"source": "calendrier_kabye_2023", "type": "evenements_janvier"}),
    ("Février (LèLAŋ): Kùmùyÿ tÿɔna pasûû — commémoration. GNASSINGBE Eyadèma sùm yýý týzûû — anniversaire décès.", {"source": "calendrier_kabye_2023", "type": "evenements_fevrier"}),
    ("Mars (LAKòò): Tata Tambéerima — fête culturelle. Taƒÿ-tû eewoki you. Agûzû — début de saison agricole. Laba — réunions/assemblées. Ajÿyÿÿ kpeekpe hŸlŸŸ kùyŸkû.", {"source": "calendrier_kabye_2023", "type": "evenements_mars"}),
    ("Avril (ɔOMAŋ): Haƒû paya caa — rites du sol. Togo tùyýýwÿû kazandû — fête nationale du Togo. PŸskŸŸ wiye (Pâques). EYADEMA lakû. Saison de préparation des champs.", {"source": "calendrier_kabye_2023", "type": "evenements_avril"}),
    ("Mai (AGOZA): Moba payÿ nËùmŸ — début grande saison des pluies. Sûnzûmùyÿ týkù týna — semailles en cours. Yeesu ÿsýdaakpaû wiye (Ascension). Fezuukiƒeƒeu tibu (Pentecôte). Saison de semailles principale.", {"source": "calendrier_kabye_2023", "type": "evenements_mai"}),
    ("Juin (MòSòGúM): Naÿ haƒaû — activités des champs. ÿjam pûyû ÿÿtûû — récoltes intermédiaires. Tùÿ sýû kùyŸkû. Cýjý nËŸzùŋ — marchés. Tabaski. Plein saison des pluies, entretien des cultures.", {"source": "calendrier_kabye_2023", "type": "evenements_juin"}),
    ("Juillet (HASòYAɔè): Akpema — site culturel. ÿyaa naalÿ kaŋ pùyÿ nÿ pokuli-ƒÿ. Pocoki Hodo. Lubùyÿ pŸzùŋ PiyŸ LŸû. KelizŸŋ wiye — célébrations. AfrikŸ hŸlŸŸ kùyŸkû. Entretien des cultures, désherbage.", {"source": "calendrier_kabye_2023", "type": "evenements_juillet"}),
    ("Août (KòYèNA): Cùmûû payaa — activités communautaires. KûnËýÿ ÿÿkûû kû-tû. MŸrùyŸ ÿsýdŸŸkpŸzûû wiye — Assomption. Mois chargé pour l'entretien des cultures.", {"source": "calendrier_kabye_2023", "type": "evenements_aout"}),
    ("Septembre (SALAò): Tipontre — Lùm eekpeÿ tulùÿa. ÿzûtûyŸŸ tŸkŸyŸŋsùm kùyŸkû — rentrée scolaire. Ajÿyÿÿ kpeekpe lŸÿhÿzùyÿ kùyŸkû. Togo tÿtûyýkûûnËŸƒûû yýý týzûû. Début des récoltes de mil et sorgho.", {"source": "calendrier_kabye_2023", "type": "evenements_septembre"}),
    ("Octobre (ALOMA): Sýnzi yýý kandiyaa. Pýý wayù manÿ eekoyuu — fêtes des récoltes. Ajÿyÿÿ kùkpÿndûû ÿgbÿyÿ ƒûû wiye. Grande saison des récoltes: ignames, maïs, sorgho.", {"source": "calendrier_kabye_2023", "type": "evenements_octobre"}),
    ("Novembre (KAMèò): Kamûû maƒaa. Sona ÿÿlûlûû a-týýyaa tÿ — fêtes de fin de récoltes. KiƒeƒemŸ kùyŸkû. SùƒŸŸ yýý týzûû wiye. Piya nÿ Caƒÿ pa-habùyÿ — fêtes des initiations. Kùjaÿ kÿwÿyÿ habùyÿ. Somdina habùyÿ. Stockage des récoltes.", {"source": "calendrier_kabye_2023", "type": "evenements_novembre"}),
    ("Décembre (SAòAYòò): Binah Sinkaring — fête du Binah. Haƒû se weewee pinde. KisimŸsù wiye — Noël. Kùjaÿ Mandela laû. Préparation champs pour nouvelle saison.", {"source": "calendrier_kabye_2023", "type": "evenements_decembre"}),

    # Jours de marché par zone
    ("Jours de marché Kabyè - 1er jour (KujukŸ/Dimanche): KOZAH: Yàndÿ, Somdinà, Làzà-Lâu, Nùÿgbàÿdà, Kpÿnzùÿdÿ, Fÿyûûdà, Lándà. TCHAOUDJO: Sokodé. SOTOUBOUA: Ajégelee. BINAH: Hiluu, Kùdàƒûû, Somdÿ. TONE: Nanergou. TANDJOARE: Bogou, Nano. CINKASSE: Cinkasse. DOUFELGOU: Nùamtougou.", {"source": "calendrier_kabye_2023", "type": "marches_kujuka"}),
    ("Jours de marché Kabyè - 2e jour (Hodo/Lundi): KOZAH: Piyà, Càƒÿ, Acàÿgbàdÿ, Lándà, Fÿyûûdà. SOTOUBOUA: Koloÿpýý/Awudà. DOUFELGOU: Ɖefàlù-fÿyûû. BINAH: Màcàÿtým. OTI: Barkoissi. CINKASSE: Nadjoundi. TANDJOARE: Warkambou. KERAN: Kanté.", {"source": "calendrier_kabye_2023", "type": "marches_hodo"}),
    ("Jours de marché Kabyè - 4e jour (CùlŸ/Mercredi): KOZAH: Kàyàŋ, Cùcàû, Fÿyûûdà, Sàyùdÿÿ, Sàràkàwàŋ. BINAH: Kpàkûdÿÿÿÿlàŋ. OTI: Mango. DOUFELGOU: KàjàlàÿÿSiu. SOTOUBOUA: marchés.", {"source": "calendrier_kabye_2023", "type": "marches_cula"}),
    ("Jours de marché Kabyè - 5e jour (SàràkàwàŋJeudi): KOZAH: Fÿyûûdà, FÿÿÿSOS, Lándà, Piyà, Kàsù, Làmà Sàûƒÿ-Ayolomà, KpàtàyûûdÿÿÿÿKPENDJAL: Mandouri. TONE: Nanergou. CINKASSE: Cinkassé. TANDJOARE: Warkambou. DOUFELGOU: Défalé. OTI: Nagbéni.", {"source": "calendrier_kabye_2023", "type": "marches_sarakawa"}),
    ("Jours de marché Kabyè - 7e jour (MàzàŋSamedi): KOZAH: Làzà (Comdÿ nÿ Ahodo), LàmàŸ (Kpedàŋ nÿ AgbàŸloosi), Piyà-Làw nÿ Piyà TýûdàŸ. BINAH: Fàrùndÿ. BASSAR: Sandaafou. SOTOUBOUA: Kpendjeéria. ASSOLI: Bafilo. OTI: Gàndo, Mango. TCHAOUDJO: Alehe.", {"source": "calendrier_kabye_2023", "type": "marches_mazan"}),

    # Agriculture kabyè saisonnière
    ("Calendrier agricole Kabyè: Saison sèche (novembre-mars) = KAMèò à LAKòò: préparation des champs, labours, stockage récoltes. Saison des pluies (avril-octobre) = ɔOMAŋ à ALOMA: semailles (mai), entretien (juin-août), récoltes (septembre-octobre).", {"source": "calendrier_kabye_2023", "type": "calendrier_agricole"}),
    ("Cultures principales région Kabyè (Kozah, Binah, Togo Nord): Ignames (ñûmŸ) — culture principale, récolte octobre-novembre. Sorgho et mil — semailles mai-juin, récolte septembre. Maïs — deux saisons. Haricots, arachides, soja — cultures associées. Coton — culture de rente.", {"source": "calendrier_kabye_2023", "type": "cultures_kabye"}),
    ("Académie Kabiyè (Kabiyè Akademii): Institution officielle de standardisation de la langue kabyè. Siège: Lomé (BP 398) et Kara (BP 43), Togo. Contact: kabiyetomakademii@yahoo.fr. Publie le calendrier kabyè annuel et les ressources pédagogiques.", {"source": "calendrier_kabye_2023", "type": "institution"}),
]


def ingest_calendar():
    retriever = KabyeRetriever()
    texts = [d[0] for d in CALENDAR_DATA]
    metadatas = [d[1] for d in CALENDAR_DATA]
    ids = [str(uuid.uuid4()) for _ in CALENDAR_DATA]
    count = retriever.add_documents("kabye_dictionary", texts, metadatas, ids)
    print(f"Calendrier Kabyè 2023 indexé: {count} entrées.")


if __name__ == "__main__":
    ingest_calendar()
