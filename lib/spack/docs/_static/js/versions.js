// taken from https://github.com/readthedocs/sphinx_rtd_theme/blob/3.0.2/sphinx_rtd_theme/static/js/versions.js_t

function onSelectorSwitch(event) {
  const option = event.target.selectedIndex;
  const item = event.target.options[option];
  window.location.href = item.dataset.url;
}

document.addEventListener("readthedocs-addons-data-ready", function (event) {
  const config = event.detail.data();

  const versionSwitch = document.querySelector(
    "div.version-switch",
  );
  let versions = config.versions.active;
  if (config.versions.current.hidden || config.versions.current.type === "external") {
    versions.unshift(config.versions.current);
  }
  const versionSelect = `
  <select>
    ${versions
      .map(
        (version) => `
      <option
value="${version.slug}"
${config.versions.current.slug === version.slug ? 'selected="selected"' : ""}
            data-url="${version.urls.documentation}">
            ${version.slug}
        </option>`,
      )
      .join("\n")}
  </select>
`;

  versionSwitch.innerHTML = versionSelect;
  versionSwitch.firstElementChild.addEventListener("change", onSelectorSwitch);
})
