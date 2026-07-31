(() => {
  const root = document.documentElement;
  const button = document.querySelector('#theme-toggle');
  const saved = localStorage.getItem('dashforge-docs-theme');
  const preferredDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const setTheme = (theme) => {
    root.dataset.theme = theme;
    button.setAttribute('aria-label', `Switch to ${theme === 'dark' ? 'light' : 'dark'} theme`);
    localStorage.setItem('dashforge-docs-theme', theme);
  };

  setTheme(saved || (preferredDark ? 'dark' : 'light'));
  button.addEventListener('click', () => setTheme(root.dataset.theme === 'dark' ? 'light' : 'dark'));

  const currentPage = document.body.dataset.page;
  const sectionNavigation = {
    charts: [
      ['workflow', 'Recommended order'], ['add-chart', 'add_chart'], ['title', 'set_title'],
      ['preset', 'preset'], ['rows', 'set_chart_per_row'], ['size', 'set_custom_size'],
      ['labels', 'Card titles & subtitles'], ['maximize', 'set_max_buttons'],
    ],
    appearance: [
      ['theme', 'set_theme'], ['colors', 'set_colors'], ['font', 'set_font_family'],
      ['header', 'Header, logo & footer'],
    ],
    data: [
      ['kpi', 'add_kpi'], ['dataset', 'add_dataset'], ['dataset-name', 'set_dataset_name'],
      ['server', 'Local server settings'], ['build-run', 'build_dashboard & run'],
      ['complete-example', 'Complete example'],
    ],
  };

  const sections = sectionNavigation[currentPage];
  if (sections) {
    document.querySelector('.sidebar-label').textContent = 'On this page';
    document.querySelector('.nav-list').innerHTML = sections
      .map(([id, label]) => `<a href="#${id}">${label}</a>`)
      .join('');
    document.querySelector('.sidebar-bottom').innerHTML = '<a href="index.html">← All documentation</a><a href="https://pypi.org/project/dashforge/" target="_blank" rel="noreferrer">View on PyPI ↗</a><a href="https://github.com/Omar-astro/DashForge-library" target="_blank" rel="noreferrer">View on GitHub ↗</a>';
  } else {
    document.querySelectorAll('[data-page-link]').forEach((link) => {
      link.classList.toggle('active', link.dataset.pageLink === currentPage);
    });
  }

  const imageStyles = document.createElement('style');
  imageStyles.textContent = `
    .github-button{display:inline-flex;align-items:center;border:1px solid var(--ink);color:var(--ink);background:var(--surface)}
    .github-button:hover{border-color:var(--blue);color:var(--blue)}
    .doc-figure{margin:28px 0;overflow:hidden;border:1px solid var(--line);border-radius:10px;background:var(--surface);box-shadow:var(--shadow)}
    .doc-figure img{display:block;width:100%;height:auto}.doc-figure figcaption{padding:10px 14px;color:var(--muted);font-size:13px;border-top:1px solid var(--line)}
    .doc-figure-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}.doc-figure-grid .doc-figure{margin:28px 0}
    @media(max-width:850px){.doc-figure-grid{grid-template-columns:1fr}}
  `;
  document.head.append(imageStyles);

  if (currentPage === 'start') {
    const actions = document.querySelector('.hero-actions');
    // Replace this URL if the GitHub repository location changes.
    actions.insertAdjacentHTML('beforeend', '<a class="button github-button" href="https://github.com/Omar-astro/DashForge-library" target="_blank" rel="noreferrer">View on GitHub ↗</a>');
  }

  const imageReferences = {
    'assets\\Documentation\\First_layout.png': {
      src: '../assets/Documentation/First_layout.png',
      alt: 'A DashForge dashboard with a navigation header and chart cards',
      caption: 'A first DashForge dashboard after running the quick-start example.',
    },
    'assets\\Documentation\\3-1Layout.png': {
      src: '../assets/Documentation/3-1Layout.png',
      alt: 'A DashForge dashboard arranged in a row of three charts followed by one chart',
      caption: 'The automatic three-plus-one chart layout.',
    },
    'assets\\Documentation\\SizingChart.png': {
      src: '../assets/Documentation/SizingChart.png',
      alt: 'A DashForge dashboard with chart cards of different widths and heights',
      caption: 'Custom chart sizing can emphasize the most important content.',
    },
    'assets\\gallery\\Layout5.5.png': {
      src: '../assets/gallery/Layout5.5.png',
      alt: 'A DashForge dataset page showing a filterable data table',
      caption: 'The optional dataset page gives viewers a filterable table of source data.',
    },
  };
  const imageGroups = {
    'assets\\Documentation\\MaxView.png | assets\\Documentation\\MinView.png': [
      ['../assets/Documentation/MaxView.png', 'A DashForge chart card maximized to fill the dashboard', 'Expanded chart view.'],
      ['../assets/Documentation/MinView.png', 'A DashForge dashboard in its regular chart-grid view', 'Regular chart-grid view.'],
    ],
    'assets\\Documentation\\Final_output1.png | assets\\Documentation\\Final_output1.5.png': [
      ['../assets/Documentation/Final_output1.png', 'The completed DashForge monthly sales dashboard', 'Completed dashboard overview.'],
      ['../assets/Documentation/Final_output1.5.png', 'A detailed view of the completed DashForge dashboard', 'Completed dashboard detail.'],
    ],
  };
  const figure = (src, alt, caption) => {
    const element = document.createElement('figure');
    element.className = 'doc-figure';
    element.innerHTML = `<img src="${src}" alt="${alt}"><figcaption>${caption}</figcaption>`;
    return element;
  };
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_COMMENT);
  const comments = [];
  while (walker.nextNode()) comments.push(walker.currentNode);
  comments.forEach((comment) => {
    const reference = comment.data.trim();
    if (imageReferences[reference]) {
      const { src, alt, caption } = imageReferences[reference];
      comment.replaceWith(figure(src, alt, caption));
    } else if (imageGroups[reference]) {
      const group = document.createElement('div');
      group.className = 'doc-figure-grid';
      imageGroups[reference].forEach(([src, alt, caption]) => group.append(figure(src, alt, caption)));
      comment.replaceWith(group);
    } else if (reference.startsWith('Picture needed: assets\\')) {
      comment.remove();
    }
  });
})();
