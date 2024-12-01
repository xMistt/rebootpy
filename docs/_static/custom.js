
function setTheme(themeToSet) {
  localStorage.setItem('theme', themeToSet);
  document.documentElement.setAttribute('data-theme', themeToSet);
}

function getCurrentTheme() {
  return document.documentElement.getAttribute('data-theme');
}

$(document).ready(function () {
  const sections = $('div.section');
  let activeLink = null;
  const bottomHeightThreshold = $(document).height() - 30;

  $(window).on('scroll', function () {
    const distanceFromTop = $(this).scrollTop();
    let currentSection = null;

    if (distanceFromTop + window.innerHeight > bottomHeightThreshold) {
      currentSection = $(sections[sections.length - 1]);
    } else {
      sections.each(function () {
        const section = $(this);
        if (section.offset().top - 1 < distanceFromTop) {
          currentSection = section;
        }
      });
    }

    if (activeLink) {
      activeLink.parent().removeClass('active');
    }

    if (currentSection) {
      activeLink = $(`.sphinxsidebar a[href="#${currentSection.attr('id')}"]`);
      activeLink.parent().addClass('active');
    }
  });

  // Store the fullname of the element clicked for possibly later use.
  $('.source-link').parent().on('click', function () {
    const rawFullname = $(this).children(":first").attr('class').split(/\s+/).find(c => c.startsWith('fullname'));
    if (!rawFullname) return;

    const split = rawFullname.split('-');
    let fullname = split.slice(1).join('.');

    if (fullname === 'none') fullname = null;
    sessionStorage.setItem('referrer', fullname);
  });

  // Check if a referrer is stored and if so use that value.
  $('.docs-link').on('click', function () {
    const fullname = sessionStorage.getItem('referrer');
    if (!fullname || fullname === 'null') return;

    const elem = $(this);
    const newHref = elem.attr('href').split('#')[0] + '#' + fullname;
    elem.attr('href', newHref);
  });
});

$(document).on('DOMContentLoaded', () => {
  const tables = document.querySelectorAll('.py-attribute-table[data-move-to-id]');
  tables.forEach(table => {
    const element = document.getElementById(table.getAttribute('data-move-to-id'));
    const parent = element.parentNode;
    // Insert table after the element
    parent.insertBefore(table, element.nextSibling);
  });
});
