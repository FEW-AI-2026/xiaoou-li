from pathlib import Path
import re

html_files = [
    "index.html",
    "research.html",
    "professional.html",
    "academic.html",
    "publications.html",
]

new_header = '''<header>
  <nav class="site-nav">
    <a href="index.html" class="nav-brand">Xiaoou Li</a>

    <button class="nav-toggle" type="button" aria-label="Open navigation menu" aria-expanded="false">
      <span></span>
      <span></span>
      <span></span>
    </button>

    <div class="nav-links">
      <a href="index.html">Home</a>
      <a href="research.html">Research &amp; Projects</a>
      <a href="professional.html">Professional Experience</a>
      <a href="academic.html">Teaching &amp; Supervision</a>
      <a href="publications.html">Publications</a>
      <button class="theme-toggle" id="themeToggle" type="button" aria-pressed="false">Dark mode</button>
    </div>
  </nav>
</header>'''

new_script = '''<script>
  (function () {
    const root = document.documentElement;
    const themeToggle = document.querySelector('.theme-toggle');
    const navToggle = document.querySelector('.nav-toggle');
    const navLinks = document.querySelector('.nav-links');
    const storageKey = 'site-theme';

    function setTheme(theme) {
      const isDark = theme === 'dark';
      root.classList.toggle('night-mode', isDark);

      if (themeToggle) {
        themeToggle.textContent = isDark ? 'Light mode' : 'Dark mode';
        themeToggle.setAttribute('aria-pressed', String(isDark));
      }
    }

    const savedTheme = localStorage.getItem(storageKey) || 'light';
    setTheme(savedTheme);

    if (themeToggle) {
      themeToggle.addEventListener('click', function () {
        const nextTheme = root.classList.contains('night-mode') ? 'light' : 'dark';
        localStorage.setItem(storageKey, nextTheme);
        setTheme(nextTheme);
      });
    }

    if (navToggle && navLinks) {
      navToggle.addEventListener('click', function () {
        const isOpen = navLinks.classList.toggle('is-open');
        navToggle.setAttribute('aria-expanded', String(isOpen));
      });

      navLinks.querySelectorAll('a').forEach(function (link) {
        link.addEventListener('click', function () {
          navLinks.classList.remove('is-open');
          navToggle.setAttribute('aria-expanded', 'false');
        });
      });
    }
  })();
</script>'''

for file_name in html_files:
    path = Path(file_name)
    text = path.read_text(encoding="utf-8")

    text = re.sub(
        r"<header>.*?</header>",
        new_header,
        text,
        count=1,
        flags=re.DOTALL,
    )

    # Remove previous inline scripts related to theme/menu to avoid duplicated listeners.
    text = re.sub(
        r"\n?<script>[\s\S]*?(site-theme|night-mode|themeToggle|theme-toggle|nav-toggle|navLinks)[\s\S]*?</script>\n?",
        "\n",
        text,
        flags=re.IGNORECASE,
    )

    text = text.replace("</body>", f"{new_script}\n</body>")

    path.write_text(text, encoding="utf-8")

css_path = Path("style.css")
css = css_path.read_text(encoding="utf-8")

mobile_css = '''
/* Responsive navigation with hamburger menu */
.site-nav {
  max-width: 1120px;
  margin: 0 auto;
  padding: 0.9rem 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  flex-wrap: nowrap;
  overflow: visible;
}

.nav-brand {
  color: var(--primary);
  text-decoration: none;
  font-weight: 800;
  padding: 0.55rem 0;
  white-space: nowrap;
}

.nav-links {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.nav-toggle {
  display: none;
  width: 44px;
  height: 44px;
  border: 1px solid var(--border);
  border-radius: 12px;
  background: var(--bg);
  cursor: pointer;
  padding: 0.65rem;
}

.nav-toggle span {
  display: block;
  height: 2px;
  width: 100%;
  background: var(--primary);
  border-radius: 999px;
  margin: 5px 0;
}

.theme-toggle {
  border: 1px solid var(--border);
  background: var(--accent-soft);
  color: var(--primary);
  font-weight: 700;
  padding: 0.55rem 0.8rem;
  border-radius: 999px;
  cursor: pointer;
  transition: background 0.2s ease, color 0.2s ease, transform 0.2s ease;
}

.theme-toggle:hover {
  transform: translateY(-1px);
}

html.night-mode {
  --primary: #9cc7ff;
  --primary-dark: #e5f0ff;
  --accent: #76a9ff;
  --accent-soft: #13243d;
  --text: #e5e7eb;
  --muted: #a8b3c5;
  --bg: #0b1120;
  --bg-light: #111827;
  --border: #263244;
  --shadow: 0 14px 35px rgba(0, 0, 0, 0.35);
}

html.night-mode body {
  background:
    radial-gradient(circle at top left, rgba(47, 128, 237, 0.16), transparent 28rem),
    linear-gradient(180deg, #0b1120 0%, #111827 100%);
}

html.night-mode header,
html.night-mode footer {
  background: rgba(11, 17, 32, 0.88);
}

html.night-mode .hero {
  background: linear-gradient(135deg, rgba(17, 24, 39, 0.96) 0%, rgba(15, 23, 42, 0.96) 100%);
}

html.night-mode .card,
html.night-mode .intro-card,
html.night-mode .nav-links {
  background: rgba(17, 24, 39, 0.94);
}

html.night-mode .profile-img {
  border-color: #1f2937;
}

html.night-mode .btn-primary {
  color: #ffffff;
}

html.night-mode .btn-secondary,
html.night-mode .nav-toggle,
html.night-mode .theme-toggle {
  background: #111827;
  color: var(--primary-dark);
}

@media (max-width: 720px) {
  .site-nav {
    padding: 0.8rem 1rem;
    position: relative;
    justify-content: space-between;
    flex-wrap: nowrap;
    overflow: visible;
  }

  .nav-toggle {
    display: block;
    flex: 0 0 auto;
  }

  .nav-links {
    position: absolute;
    top: calc(100% + 0.5rem);
    left: 1rem;
    right: 1rem;
    display: none;
    flex-direction: column;
    align-items: stretch;
    gap: 0.45rem;
    padding: 0.8rem;
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 18px;
    box-shadow: var(--shadow);
  }

  .nav-links.is-open {
    display: flex;
  }

  .nav-links a,
  .theme-toggle {
    width: 100%;
    text-align: left;
  }
}
'''

if "Responsive navigation with hamburger menu" not in css:
    css = css.rstrip() + "\n\n" + mobile_css + "\n"

css_path.write_text(css, encoding="utf-8")
