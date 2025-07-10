---
title: custom.css
date: 2025-07-10
updated: 2025-07-10
---

@import url('<https://fonts.googleapis.com/css2?family=Cinzel>:wght@400..900&family=Newsreader:ital,opsz,wght@0,6..72,200..800;1,6..72,200..800&display=swap');

/* Apply the sans-serif font to the headings */

article:is(h1, h2, h3, h4, h5, h6) {  
   font-family: 'Cinzel', serif!important;  
}

/* Apply the sans-serif font to the rest of your markdown content */

article:not(h1, h2, h3, h4, h5, h6) {  
   font-family: 'Newsreader', serif!important;  
}
