/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./**/*.html",
    "./fiches/templates/**/*.html",
    "./modules/templates/**/*.html",
    "./home/templates/**/*.html",
    // Ajoute d'autres chemins si besoin selon ta structure
  ],
  theme: {
    extend: {
      colors: {
        rouge: '#b22222',
        dore: '#daa520',
        gris: '#333333',
        'gris-clair': '#f8f8f8',
        'rouge-cramoisi': '#DC143C',
        'rouge-charte': '#b22222',
        'rouge-fraise': '#FB2943',
        'rouge-nacarat': '#FF6863 ',
      },
      fontFamily: {
        sans: ['Inter', 'Noto Sans', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
