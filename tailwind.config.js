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
        "our-story": 'url("https://res.cloudinary.com/ddyvvm4ql/image/upload/q_auto,f_auto/wedding-site/backgrounds/Background-Fuchsia")',
        faq: 'url("https://res.cloudinary.com/ddyvvm4ql/image/upload/q_auto,f_auto/wedding-site/backgrounds/Background-Pink")',
        itinerary: 'url("https://res.cloudinary.com/ddyvvm4ql/image/upload/q_auto,f_auto/wedding-site/backgrounds/Background-LightPink")',
        gallery: 'url("https://res.cloudinary.com/ddyvvm4ql/image/upload/q_auto,f_auto/wedding-site/backgrounds/Background_Pink_Long")',
      },
      backgroundSize: {
        vine: "contain",
      },
    },
  },
  plugins: [],
};
