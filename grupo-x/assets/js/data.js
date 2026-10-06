/* Base de datos compartida del ecosistema Grupo X Team X (demo estática).
   En producción esta estructura vive en una única base de datos; ambas marcas leen y escriben aquí. */
window.GX_DATA = {
  projects: [
    { id: "CX-001", brand: "construx", type: "house", es: "Casa Mirador", en: "Mirador House", city: "Panamá", year: 2025, status: "done", m2: 210 },
    { id: "CX-002", brand: "construx", type: "remodel", es: "Remodelación Apto. Costa", en: "Costa Apartment Remodel", city: "Panamá", year: 2025, status: "done", m2: 96 },
    { id: "CX-003", brand: "construx", type: "commercial", es: "Local Café Esquina", en: "Corner Café Space", city: "Panamá", year: 2026, status: "active", m2: 64 },
    { id: "CX-004", brand: "construx", type: "land", es: "Urbanización de terreno Vista", en: "Vista Land Development", city: "Chiriquí", year: 2026, status: "planning", m2: 1200 },
    { id: "AV-001", brand: "produavx", type: "film", es: "Corto «Última Escena»", en: "Short «Last Scene»", city: "Panamá", year: 2025, status: "done", m2: 0 },
    { id: "AV-002", brand: "produavx", type: "commercial", es: "Spot Marca Local", en: "Local Brand Spot", city: "Panamá", year: 2026, status: "active", m2: 0 },
    { id: "AV-003", brand: "produavx", type: "audio", es: "Podcast + Mezcla Master", en: "Podcast + Master Mix", city: "Remoto", year: 2026, status: "active", m2: 0 },
    { id: "AV-004", brand: "produavx", type: "tour", es: "Recorrido de obra (ConstruX)", en: "Site Walkthrough (ConstruX)", city: "Panamá", year: 2026, status: "done", m2: 0, shared: true }
  ],
  partners: [
    { name: "Partner Social A", reach: 48, channel: "Instagram" },
    { name: "Partner Social B", reach: 31, channel: "TikTok" },
    { name: "Partner Social C", reach: 22, channel: "YouTube" },
    { name: "Partner Social D", reach: 14, channel: "LinkedIn" }
  ],
  documents: [
    { name: "Contrato-marco-servicios.pdf", brand: "gx", es: "Contrato marco", en: "Master agreement" },
    { name: "Guion-UltimaEscena-v4.pdf", brand: "produavx", es: "Guion", en: "Script" },
    { name: "Planos-CasaMirador-rev2.dwg", brand: "construx", es: "Planos", en: "Blueprints" },
    { name: "Plan-Contenidos-Q4.xlsx", brand: "gx", es: "Plan de contenidos compartido", en: "Shared content plan" }
  ]
};
