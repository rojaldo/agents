# Guía de personalización de Reveal.js

## usa estas dependencias:

```html
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/dist/reveal.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/dist/theme/white.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/atom-one-light.min.css">
```

## usa estos estilos:

```css

    <style>
        .reveal { text-align: left; color: #555555; }
        .reveal section { text-align: left; padding: 40px; display: flex; flex-direction: column; justify-content: flex-start; }
        .reveal h1, .reveal h2, .reveal h3 { text-transform: none; text-align: left; color: #555555; }
        
        /* Encabezados */
        .reveal h1 { font-size: 1.05em; margin-bottom: 0.5em; }
        .reveal h2 { font-size: 1em; margin-bottom: 0.5em; }
        .reveal h3 { font-size: 0.75em; margin-bottom: 0.3em; }
        
        /* Párrafos y énfasis */
        .reveal p { font-size: 0.6em; margin: 0.3em 0; color: #555555; }
        .reveal strong { font-size: 1em; font-weight: bold; }
        
        /* Código */
        .reveal pre { background: #f8f8f8; border: 1px solid #ddd; width: 100%; padding: 0.5em; margin: 0.5em 0; }
        .reveal pre code { font-size: 0.7em; color: #555555; }
        
        /* Listas y elementos */
        .reveal ul { font-size: 0.55em; text-align: left; margin-left: 0.5em; color: #555555; }
        .reveal li { margin: 0.3em 0; color: #555555; }
    </style>
```