function renderReadme(name) {
    if (typeof _mainWindow != "undefined") {
        _mainWindow.renderReadme(name);
    }
};

hljs.initHighlightingOnLoad();
var md = window.markdownit();

md.renderer.rules.table_open = function() {
    return '<table class="table table-striped">\n';
};

md.options.html = true;
md.options.breaks = true;
md.options.linkify = true;
md.options.typographer = true;
md.options.highlight = function(str, lang) {
    if (lang && hljs.getLanguage(lang)) {
        try {
            return '<pre class="hljs"><code>' +
                hljs.highlight(lang, str, true).value +
                '</code></pre>';
        } catch (__) {}
    }
    return '<pre class="hljs"><code>' + md.utils.escapeHtml(str) + '</code></pre>';
};

// 更新文字
function updateText(text) {
    layer.closeAll();
    $("#result").html(md.render(text)); 
    document.getElementById("loading").style.display = "none";
    document.getElementById("result").style.display = text.length > 0 ? "block" : "none";
    backToUp();
    //     hljs.initHighlighting.called = false;
    //     hljs.initHighlighting();
}

// 更新代码
function updateCode(text) {
    $("#code").html(hljs.highlightAuto(text).value);
    //捕获页
    layer.open({
        type: 1,
        shade: false,
        title: false, //不显示标题
        area: ["80%", "80%"],
        content: $('#codediv'), //捕获的元素，注意：最好该指定的元素要存放在body最外层，否则可能被其它的相对元素所影响
    });
}

// 返回顶部
function backToUp() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}

function getQueryString(name) {
    // 获取url中的参数
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
    var r = window.location.search.substr(1).match(reg);
    if (r !== null) return unescape(r[2]);
    return null;
}

window.onload = function() {
    var name = getQueryString("name");
    name = (name === "null" ? "" : name);
    setTimeout(function() {
        renderReadme(name);
    }, 500);
};