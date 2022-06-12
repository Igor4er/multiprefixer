let prev = document.getElementById("prev");
function showPreviewImage(span) {
    if (prev.checked) {
        let div = span.getElementsByTagName("div")[0];
        div.setAttribute("class", "img_container");
        let vid = span.getElementsByTagName("video")[0];
        let a = span.getElementsByTagName("a")[0];
        vid.src = a.href;
    }
}

function hidePreviewImage(span) {
    let div = span.getElementsByTagName("div")[0];
    div.setAttribute("class", "hid");
}