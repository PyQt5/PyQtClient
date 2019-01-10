hljs.initHighlightingOnLoad();
var md = window.markdownit();
md.renderer.rules.table_open = function () {
    return '<table class="table table-striped">\n';
};
md.options.html = true;
md.options.breaks = true;
md.options.linkify = true;
md.options.typographer = true;
md.options.highlight = function (str, lang) {
    if (lang && hljs.getLanguage(lang)) {
        try {
            return '<pre class="hljs"><code>' +
                hljs.highlight(lang, str, true).value +
                '</code></pre>';
        } catch (__) {}
    }
    return '<pre class="hljs"><code>' + md.utils.escapeHtml(str) + '</code></pre>';
}
function updateText(text) {
    document.getElementById("result").innerHTML = md.render(text);
    document.getElementById("result").style.display = "block";
}