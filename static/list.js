let prev = document.getElementById("prev");
function showPreviewImage(span) {
    if (prev.checked) {
        let div = span.getElementsByTagName("div")[0];
        div.setAttribute("class", "img_container");
        let img = span.getElementsByTagName("img")[0];
        let a = span.getElementsByTagName("a")[0];
        img.src = a.href;
    }
}

function hidePreviewImage(span) {
    let div = span.getElementsByTagName("div")[0];
    div.setAttribute("class", "hid");
}