hljs.initHighlightingOnLoad();
var md = window.markdownit();

md.renderer.rules.table_open = function () {
    return '<table class="table table-striped">\n';
}

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

// 更新文字
function updateText(text) {
    document.getElementById("result").innerHTML = md.render(text);
    document.getElementById("result").style.display = "block";
}

// 返回顶部
function backToUp() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}