let base_url = "http://127.0.0.1:5000"
let next_url = base_url + "/prefixer/next/video"
let previous_url = base_url + "/prefixer/previous/video"
let delete_url = base_url + "/prefixer/delete/video"
let underscore_url = base_url + "/prefixer/underscore/video"


function setCookie(cName, cValue, expDays) {
        let date = new Date();
        date.setTime(date.getTime() + (expDays * 24 * 60 * 60 * 1000));
        const expires = "expires=" + date.toUTCString();
        document.cookie = cName + "=" + cValue + "; " + expires + "; SameSite=Lax " + "; secure" + "; path=/";
}


function getCookie(cName) {
      const name = cName + "=";
      const cDecoded = decodeURIComponent(document.cookie); //to be careful
      const cArr = cDecoded .split('; ');
      let res;
      cArr.forEach(val => {
          if (val.indexOf(name) === 0) res = val.substring(name.length);
      })
      return res;
}


function getPhoto() {
    let cookies = document.cookie;
    let photo_url = "http://127.0.0.1:5000/api/video";
    let xhr = new XMLHttpRequest();
    xhr.open("GET", photo_url);
    // xhr.setRequestHeader("Cookie", cookies);
    xhr.onreadystatechange = function () {
       if (xhr.readyState === 4) {
          let resp = xhr.responseText;
          updatePhoto(resp);
          return xhr.status;
       }};
    xhr.send();
}

function updatePhoto(photo_url) {
let el = document.getElementById("ima");
let queryString = "?t=" + new Date().getTime();
el.src = photo_url + queryString;
}

function cookieXHR(url) {
    let cookies = document.cookie;
    let xhr = new XMLHttpRequest();
    xhr.open("GET", url);
    xhr.onreadystatechange = function () {
       if (xhr.readyState === 4) {
          return xhr.status;
       }};
    xhr.send();
}

function next() {
    let index_now = parseInt(getCookie("vindex"));
    let index_after = index_now + 1;
    index_after = '' + index_after;
    setCookie("vindex", index_after, "session")
    getPhoto();
}

function previous() {
    let index_now = parseInt(getCookie("vindex"));
    let index_after = index_now - 1;
    index_after = '' + index_after;
    setCookie("vindex", index_after, "session")
    getPhoto();
}

function delete_photo() {
    updateCycle(delete_url);
}

function underscore() {
    updateCycle(underscore_url);
}

function updateCycle(url) {
    cookieXHR(url);
    getPhoto();
}

function fastHide() {
    let el = document.getElementById("ima");
    el.setAttribute("class", "pdn");
}

function flashHide() {
    let el = document.getElementById("ima");
    let attr = el.getAttribute("class");
    if (attr != "pdn") {
    el.setAttribute("class", "dn");
    }
}

function flashShow() {
    let el = document.getElementById("ima");
    let attr = el.getAttribute("class");
    if (attr != "pdn") {
    el.setAttribute("class", "class");
    }
}
