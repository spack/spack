// based on https://github.com/readthedocs/sphinx_rtd_theme/blob/3.0.2/sphinx_rtd_theme/static/js/versions.js_t

function onSelectorSwitch(event) {
  const option = event.target.selectedIndex;
  const item = event.target.options[option];
  window.location.href = item.dataset.url;
}

function initVersionSelector(config) {
  const versionSwitch = document.querySelector(".version-switch");
  if (!versionSwitch) { return; }
  let versions = config.versions.active;
  if (config.versions.current.hidden || config.versions.current.type === "external") {
    versions.unshift(config.versions.current);
  }
  const versionSelect = `
  <select>
    ${versions
      .map(
        (version) => `
<option value="${version.slug}" ${config.versions.current.slug === version.slug ? 'selected="selected"' : ""} data-url="${version.urls.documentation}">
  ${version.slug}
</option>`,
      )
      .join("\n")}
  </select>
`;

  versionSwitch.innerHTML = versionSelect;
  versionSwitch.firstElementChild.addEventListener("change", onSelectorSwitch);
}

function initSearch(currentVersion) {
  let searchTimeout;
  let originalContent;
  const searchInput = document.querySelector(".sidebar-search");
  const mainContent = document.getElementById("furo-main-content");
  const searchForm = document.querySelector(".sidebar-search-container");

  if (!searchInput || !mainContent || !searchForm) { return; }

  // Store original content
  originalContent = mainContent.innerHTML;

  searchInput.addEventListener("input", handleSearchInput);
  searchInput.addEventListener("keydown", handleTabNavigation);
  searchForm.addEventListener("submit", handleFormSubmit);

  function handleSearchInput(e) {
    const query = e.target.value.trim();
    clearTimeout(searchTimeout);
    if (query.length === 0) {
      mainContent.innerHTML = originalContent;
      return;
    }
    searchTimeout = setTimeout(function () {
      performSearch(query);
    }, 300);
  }

  function handleFormSubmit(e) {
    e.preventDefault();
    const query = searchInput.value.trim();
    if (query) {
      performSearch(query);
    }
  }

  function handleTabNavigation(e) {
    // Check if we're tabbing throught search results
    if (e.key !== 'Tab' || e.shiftKey) { return; }
    const searchResults = document.querySelector(".search-results");
    if (!searchResults) { return; }

    // Focus on the first link in search results instead of default behavior
    e.preventDefault();
    const firstLink = searchResults.querySelector("a");
    if (firstLink) {
      firstLink.focus();
    }
  }

  function performSearch(query) {
    const fullQuery = `project:spack/${currentVersion} ${query}`;
    const searchUrl = `/_/api/v3/search/?q=${encodeURIComponent(fullQuery)}`;

    fetch(searchUrl)
      .then(function (response) {
        if (!response.ok) { throw new Error("HTTP error! status: " + response.status); }
        return response.json();
      })
      .then(function (data) {
        displaySearchResults(data, query);
      })
      .catch(function (error) {
        mainContent.innerHTML = "<p>Error performing search.</p>";
      });
  }

  function displaySearchResults(data, query) {
    if (!data.results?.length) {
      mainContent.innerHTML = `<h2>No Results Found</h2><p>No results found for "${query}".</p>`;
      return;
    }

    let html = '<div class="search-results"><h1>Search Results</h1>';

    data.results.forEach((result, index) => {
      const title = result.highlights?.title?.[0] ?? result.title;
      html += `<h2><a href="${result.domain}${result.path}">${title}</a></h2>`;

      result.blocks?.forEach(block => {
        const blockTitle = block.highlights?.title?.[0];
        if (blockTitle) {
          html += `<h3><a href="${result.domain}${result.path}#${block.id}">${blockTitle}</a></h3>`;
        }
        html += block.highlights?.content?.map(content => `<p>${content}</p>`).join('') ?? '';
      });

      if (index < data.results.length - 1) {
        html += `<hr class="docutils" />`;
      }
    });

    html += "</div>";
    mainContent.innerHTML = html;
  }
}

document.addEventListener("readthedocs-addons-data-ready", function (event) {
  const config = event.detail.data();
  initVersionSelector(config);
  initSearch(config.versions.current.slug);
});
