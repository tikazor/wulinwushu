/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./**/*.html",
    "./fiches/templates/**/*.html",
    "./modules/templates/**/*.html",
    "./home/templates/**/*.html",
    "./**/*.djhtml", 
    // Ajoute d'autres chemins si besoin selon ta structure
  ],
  
  theme: {
    extend: {
      colors: {
  'btn-modifier': '#2563eb',
  'btn-modifier-hover': '#1d4ed8',

  'btn-supprimer': '#dc2626',
  'btn-supprimer-hover': '#b91c1c',

  'btn-valider': '#16a34a',
  'btn-valider-hover': '#15803d',

  'btn-retour': '#6b7280',
  'btn-retour-hover': '#4b5563',

  'carte-bordure': '#e5e7eb',
  'carte-fond': '#ffffff',

  'alert-success': '#22c55e',
  'alert-error': '#ef4444',
  'alert-info': '#3b82f6',

  rouge: '#b22222',
  dore: '#daa520',
  gris: '#333333',

  'gris-clair': '#f8f8f8',
  'rouge-cramoisi': '#DC143C',
  'rouge-charte': '#b22222',
  'rouge-fraise': '#FB2943',
  'rouge-nacarat': '#FF6863',
  }
    },
  },
  plugins: [],

}
