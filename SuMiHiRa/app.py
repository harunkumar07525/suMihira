from flask import Flask, render_template_string, url_for

app = Flask(__name__)

# Sample data for the page
SERVICES = [
    {"title": "SuMiHiRa Astrology (Prashna)", "desc": "Astrology (Prashna)"},
    {"title": "SuMiHiRa Yoga", "desc": "Coming Soon..."},
    {"title": "SuMiHiRa Music", "desc": "Coming Soon..."},
    {"title": "SuMiHiRa Vastu", "desc": "Coming Soon..."},
]

HTML = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>SuMiHiRa</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
      /* small extra styles for carousel */
      .slide { transition: transform .4s ease, opacity .4s ease; }
      .hidden-slide { opacity: 0; transform: translateX(20px); pointer-events: none; position: absolute; }
      .visible-slide { opacity: 1; transform: translateX(0); position: relative; }
    </style>
  </head>
  <body class="bg-gray-50 text-gray-800">
    <div class="max-w-6xl mx-auto p-6">

      <!-- App Tile -->
      <header class="flex items-center gap-4 mb-6">
        <div class="w-20 h-20 bg-gradient-to-br from-indigo-500 to-purple-500 rounded-2xl flex items-center justify-center text-white text-2xl font-bold shadow-lg">P</div>
        <div>
          <h1 class="text-2xl font-extrabold">SuMiHiRa</h1>
          <p class="text-sm text-gray-600">Astrology (Prashna)</p>
        </div>
      </header>

      <!-- App Intro -->
      <section class="bg-white rounded-2xl p-6 shadow-sm mb-8">
        <div class="md:flex md:items-center md:justify-between">
          <div>
            <h2 class="text-3xl font-bold mb-2">Welcome to SuMiHiRa</h2>
            <p class="text-gray-600 mb-4">Astrology Questions and Answers</p>
            <a href="#services" class="inline-block px-4 py-2 bg-indigo-600 text-white rounded-lg shadow hover:bg-indigo-700">Explore services</a>
          </div>
          <div class="mt-6 md:mt-0 flex items-center gap-4">
            <div class="p-4 bg-gradient-to-br from-yellow-50 to-red-50 rounded-lg">
              <p class="text-sm text-gray-500">About us</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Services with slide tiles (carousel) -->
      <section id="services" class="mb-8">
        <h3 class="text-xl font-bold mb-3">Services — carousel</h3>
        <div class="relative bg-white rounded-2xl p-6 shadow-sm overflow-hidden">
          <div id="carousel" class="min-h-[140px]">
            <!-- slides inserted by template -->
            {% for s in services %}
              <article class="slide p-4 rounded-xl bg-gradient-to-r from-white to-gray-50 border shadow-sm">
                <h4 class="text-lg font-semibold">{{ s.title }}</h4>
                <p class="text-gray-600">{{ s.desc }}</p>
              </article>
            {% endfor %}
          </div>

          <!-- controls -->
          <div class="absolute inset-y-0 left-0 flex items-center">
            <button id="prevBtn" class="p-2 m-3 bg-white rounded-full shadow hover:scale-105">◀</button>
          </div>
          <div class="absolute inset-y-0 right-0 flex items-center">
            <button id="nextBtn" class="p-2 m-3 bg-white rounded-full shadow hover:scale-105">▶</button>
          </div>

          <!-- pager -->
          <div id="pager" class="mt-4 flex gap-2 justify-center"></div>
        </div>
      </section>

      <!-- App services tiles (grid) -->
      <section>
        <h3 class="text-xl font-bold mb-3">Services — tiles</h3>
        <div class="mb-4">
<input id="searchInput" type="text" placeholder="Search services..." class="w-full border rounded-lg px-3 py-2" />
</div>
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
          {% for s in services %}
            <div class="bg-white p-4 rounded-2xl shadow-sm hover:shadow-lg transition">
              <div class="flex items-start gap-3">
                <div class="w-12 h-12 rounded-xl bg-indigo-50 flex items-center justify-center font-bold text-indigo-600">{{ s.title[0] }}</div>
                <div>
                  <h4 class="font-semibold">{{ s.title }}</h4>
                  <p class="text-gray-600 text-sm">{{ s.desc }}</p>
                </div>
              </div>
              <div class="mt-4 flex gap-2">
                <button class="px-3 py-1 bg-indigo-600 text-white rounded-lg">Open</button>
                <button class="px-3 py-1 border rounded-lg">Details</button>
              </div>
            </div>
          {% endfor %}
        </div>
      </section>

      <footer class="mt-8 text-sm text-gray-500">SuMiHiRa Version 1.0.0</footer>
    </div>

    <script>
      // Simple carousel logic (no deps). It keeps track of slides and shows one at a time.
      (function(){
        const carousel = document.getElementById('carousel');
        const slides = Array.from(carousel.querySelectorAll('.slide'));
        const pager = document.getElementById('pager');
        let idx = 0;
        let autoTimer = null;

        function render(){
          slides.forEach((s,i)=>{
            if(i === idx){
              s.classList.remove('hidden-slide'); s.classList.add('visible-slide');
            } else {
              s.classList.add('hidden-slide'); s.classList.remove('visible-slide');
            }
          });
          // pager
          pager.innerHTML = '';
          slides.forEach((_,i)=>{
            const dot = document.createElement('button');
            dot.className = 'w-3 h-3 rounded-full ' + (i===idx ? 'bg-indigo-600' : 'bg-gray-300');
            dot.addEventListener('click', ()=>{ idx = i; resetAuto(); render(); });
            pager.appendChild(dot);
          });
        }

        function next(){ idx = (idx + 1) % slides.length; render(); }
        function prev(){ idx = (idx - 1 + slides.length) % slides.length; render(); }
        function resetAuto(){ if(autoTimer) clearInterval(autoTimer); autoTimer = setInterval(next, 4000); }

        document.getElementById('nextBtn').addEventListener('click', ()=>{ next(); resetAuto(); });
        document.getElementById('prevBtn').addEventListener('click', ()=>{ prev(); resetAuto(); });

        // initialize
        if(slides.length === 0) return;
        // make slides stack nicely
        slides.forEach(s=>{ s.style.position='absolute'; s.style.left='0'; s.style.right='0'; });
        render(); resetAuto();
      })();

      // Search filter for services tiles
(function(){
const searchInput = document.getElementById('searchInput');
const tiles = document.querySelectorAll('.service-tile');
if(!searchInput) return;
searchInput.addEventListener('input', ()=>{
const q = searchInput.value.toLowerCase();
tiles.forEach(tile => {
const title = tile.dataset.title;
const desc = tile.dataset.desc;
if(title.includes(q) || desc.includes(q)){
tile.style.display = '';
} else {
tile.style.display = 'none';
}
});
});
})();
    </script>
  </body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML, services=SERVICES)

if __name__ == '__main__':
    app.run(debug=True)
