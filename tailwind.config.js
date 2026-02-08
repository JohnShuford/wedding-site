/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./wedding/templates/**/*.html", "./wedding/static/js/**/*.js"],
  theme: {
    extend: {
      colors: {
        wedding: {
          peach: "#efcebd",
          "dark-red": "#7b2c44",
          coral: "#c64e45",
          "light-coral": "#f7918e",
          blush: "#fce1d6",
          dark: "#2e2e2e",
        },
      },
      fontFamily: {
        lora: ["Lora", "serif"],
        luxurious: ["Luxurious Script", "cursive"],
      },
      fontSize: {
        "12xl": "12rem",
        "10xl": "10rem",
      },
      backgroundImage: {
        "our-story": 'url("/static/images/backgrounds/Background-Fuchsia.png")',
        faq: 'url("/static/images/backgrounds/Background-Pink.png")',
        itinerary: 'url("/static/images/backgrounds/Background-LightPink.png")',
        gallery: 'url("/static/images/backgrounds/Background_Pink_Long.png")',
        "vine-repeat": 'url("/static/images/itinerary/vine.png")',
      },
      backgroundSize: {
        vine: "contain",
      },
    },
  },
  plugins: [],
};
