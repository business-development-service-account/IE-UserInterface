/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'sidebar-dark': '#2c3e50',
        'sidebar-hover': '#34495e',
        'accent-blue': '#3498db',
        'accent-blue-hover': '#2980b9',
        'content-bg': '#f5f5f5',
        'card-bg': '#ffffff',
        'border-light': '#e0e0e0',
        'text-muted': '#7f8c8d',
        'text-light': '#95a5a6',
        'input-border': '#ddd',
        'hover-bg': '#e9ecef',
      },
    },
  },
  plugins: [],
}