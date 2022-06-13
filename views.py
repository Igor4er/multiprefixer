import os
import random
from flask import render_template, send_from_directory, abort, make_response, request, redirect, url_for, flash
from app import app
from werkzeug.exceptions import HTTPException
import shutil
from config import BASE_DIRECTORY as BASE_DIR


@app.route("/")
def index():
    dir = request.cookies.get("dir", "none")
    position = request.cookies.get("index", "none")
    vindex = request.cookies.get("vindex", "none")
    first_underscored_video_number = get_first_underscored_video_number(dir)
    first_underscored_photo_number = get_first_underscored_photo_number(dir)
    return render_template("index.html", dir=dir, position=position, vindex=vindex, first_underscored_video_number=first_underscored_video_number, first_underscored_photo_number=first_underscored_photo_number)


@app.route("/edit", methods=["post", "get"])
def edit():
    directory = request.cookies.get("dir", "none")
    if directory != "drop":
        dirs = get_all_dirs()
    else:
        dirs = ["drop"]
    value_index = request.cookies.get("index", "0")
    vindex = request.cookies.get("vindex", "0")
    resp = make_response(render_template("edit.html", dirs=dirs, value_index=value_index, vindex=vindex))
    if request.method == "POST":
        dir = request.form.get("dir")
        resp.set_cookie("dir", dir, secure=True, samesite="Lax", httponly=True)

        index = request.form.get("position", "0")
        resp.set_cookie("index", index, secure=True, samesite="Lax")

        vindex = request.form.get("vindex", "0")
        resp.set_cookie("vindex", vindex, secure=True, samesite="Lax")
    return resp


@app.route("/list")
def auto_list():
    directory = request.cookies.get("dir", "none")
    return redirect(url_for("list_photos", directory_name=directory))


@app.route("/list_videos")
def auto_list_videos():
    directory = request.cookies.get("dir", "none")
    return redirect(url_for("list_videos", directory_name=directory))


@app.route("/list_<directory_name>")
def list_photos(directory_name):
    list, _ = get_all_photos(directory_name)
    return render_template("list.html", list=list, len=len(list), dir=directory_name)


@app.route("/list_<directory_name>_videos")
def list_videos(directory_name):
    list, _ = get_all_videos(directory_name)
    return render_template("list_videos.html", list=list, len=len(list), dir=directory_name)


@app.route("/random")
def auto_random():
    directory = request.cookies.get("dir", "none")
    return render_template("auto_random.html", directory=directory)


@app.route("/random_<directory_name>.jpg")
def random_photo(directory_name):
    list, path = get_all_photos(directory_name)
    random_photo = random.choice(list)
    resp = make_response(send_from_directory(path, random_photo, mimetype="image/jpeg"))
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    resp.headers["Expires"] = "0"
    return resp


@app.route("/random_<directory_name>_video.mp4")
def random_video(directory_name):
    list, path = get_all_videos(directory_name)
    random_video = random.choice(list)
    resp = make_response(send_from_directory(path, random_video, mimetype="video/mp4"))
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    resp.headers["Expires"] = "0"
    return resp


@app.route("/<index>_in_<directory_name>.jpg")
def get_photo_by_index(index, directory_name):
    list, path = get_all_photos(directory_name)
    index = int(index)
    if index > len(list) or index < 0:
        abort(418)
    photo = list[index]
    resp = make_response(send_from_directory(path, photo, mimetype="image/jpeg"))
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    resp.headers["Expires"] = "0"
    return resp


@app.route("/<index>_in_<directory_name>.mp4")
def get_video_by_index(index, directory_name):
    list, path = get_all_videos(directory_name)
    index = int(index)
    if index > len(list) or index < 0:
        abort(418)
    video = list[index]
    resp = make_response(send_from_directory(path, video, mimetype="video/mp4"))
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    resp.headers["Expires"] = "0"
    return resp


@app.route("/<name>_of_<directory_name>.jpg")
def get_photo_by_name(name, directory_name):
    path = os.path.join(BASE_DIR, directory_name)
    resp = make_response(send_from_directory(path, name, mimetype="image/jpeg"))
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    resp.headers["Expires"] = "0"
    return resp


@app.route("/<name>_of_<directory_name>.mp4")
def get_video_by_name(name, directory_name):
    path = os.path.join(BASE_DIR, directory_name)
    path = os.path.join(path, "vid")
    resp = make_response(send_from_directory(path, name, mimetype="video/mp4"))
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    resp.headers["Expires"] = "0"
    return resp


@app.route("/prefixer")
def prefixer():
    dir = request.cookies.get("dir", "none")
    index = request.cookies.get("index", "0")
    photo = url_for('get_photo_by_index', index=index, directory_name=dir)
    resp = make_response(render_template("show.html", photo=photo))
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    resp.headers["Expires"] = "0"
    return resp


@app.route("/prefixer/video")
def prefixer_video():
    dir = request.cookies.get("dir", "none")
    index = request.cookies.get("vindex", "0")
    video = url_for('get_video_by_index', index=index, directory_name=dir)
    resp = make_response(render_template("show_videos.html", video=video))
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    resp.headers["Expires"] = "0"
    return resp


@app.route("/api/photo")
def photo_now():
    dir = request.cookies.get("dir", "none")
    index = request.cookies.get("index", "0")
    photo = url_for('get_photo_by_index', index=index, directory_name=dir)
    return photo


@app.route("/api/video")
def video_now():
    dir = request.cookies.get("dir", "none")
    index = request.cookies.get("vindex", "0")
    video = url_for('get_video_by_index', index=index, directory_name=dir)
    return video


@app.route("/prefixer/previous")
def previous():
    index = request.cookies.get("index", "0")
    resp = make_response(redirect(url_for('prefixer')))
    new_index = str(int(index)-1)
    resp.set_cookie("index", new_index, secure=True, samesite="Lax")
    return resp


@app.route("/prefixer/previous/video")
def previous_video():
    index = request.cookies.get("vindex", "0")
    resp = make_response(redirect(url_for('prefixer_video')))
    new_index = str(int(index)-1)
    resp.set_cookie("vindex", new_index, secure=True, samesite="Lax")
    return resp


@app.route("/prefixer/delete_unconfirmed")
def delete_unconfirmed():
    url = url_for("delete")
    return render_template("delete_unconfirmed.html", confirm_url=url)


@app.route("/prefixer/delete")
def delete():
    directory_name = request.cookies.get("dir")
    index = int(request.cookies.get("index"))
    list, path = get_all_photos(directory_name)
    os.remove(os.path.join(path, list[index]))
    return redirect(url_for("prefixer"))


@app.route("/prefixer/delete/video")
def delete_video():
    directory_name = request.cookies.get("dir")
    index = int(request.cookies.get("vindex"))
    list, path = get_all_videos(directory_name)
    os.remove(os.path.join(path, list[index]))
    url = url_for("prefixer")
    return redirect(url)


@app.route('/prefixer/underscore')
def underscore():
    directory_name = request.cookies.get("dir")
    index = int(request.cookies.get("index"))
    list, path = get_all_photos(directory_name)
    before = os.path.join(path, list[index])
    after = os.path.join(path, "_" + list[index])
    try:
        os.rename(before, after)
    except:
        return redirect(url_for("next"))
    url = url_for("prefixer")
    return redirect(url)


@app.route('/prefixer/underscore/video')
def underscore_video():
    directory_name = request.cookies.get("dir")
    index = int(request.cookies.get("vindex"))
    list, path = get_all_videos(directory_name)
    before = os.path.join(path, list[index])
    after = os.path.join(path, "_" + list[index])
    try:
        os.rename(before, after)
    except:
        return redirect(url_for("next"))
    url = url_for("prefixer_video")
    return redirect(url)


@app.route("/prefixer/next")
def next():
    index = request.cookies.get("index", "0")
    resp = make_response(redirect(url_for('prefixer')))
    new_index = str(int(index)+1)
    resp.set_cookie("index", new_index, secure=True, samesite="Lax")
    return resp


@app.route("/prefixer/next/video")
def next_video():
    index = request.cookies.get("vindex", "0")
    resp = make_response(redirect(url_for('prefixer_video')))
    new_index = str(int(index)+1)
    resp.set_cookie("vindex", new_index, secure=True, samesite="Lax")
    return resp


@app.route("/prefixer/move", methods=["post", "get"])
def move():
    if request.method == "POST":
        dest_dir = os.path.join(BASE_DIR, request.form.get("dir"))
        dir = request.cookies.get("dir")
        index = int(request.cookies.get("index"))
        list, path = get_all_photos(dir)
        source = os.path.join(path, list[index])
        if request.form.get("underscore"):
            dest = os.path.join(dest_dir, "_" + list[index])
        else:
            dest = os.path.join(dest_dir, list[index])
        shutil.move(source, dest)
        return redirect(url_for("prefixer"))
    options = get_all_dirs()
    return render_template("move.html", options=options)


@app.route("/prefixer/move/video", methods=["post", "get"])
def move_video():
    if request.method == "POST":
        dest_dir = os.path.join(BASE_DIR, request.form.get("dir"))
        dest_dir = os.path.join(dest_dir, 'vid')
        dir = request.cookies.get("dir")
        index = int(request.cookies.get("vindex"))
        list, path = get_all_videos(dir)
        source = os.path.join(path, list[index])
        if request.form.get("underscore"):
            dest = os.path.join(dest_dir, "_" + list[index])
        else:
            dest = os.path.join(dest_dir, list[index])
        shutil.move(source, dest)
        return redirect(url_for("prefixer_video"))
    options = get_all_dirs()
    return render_template("move.html", options=options)


@app.route("/instant_drop")
def drop_dir():
    resp = make_response(redirect(url_for("blank_page")))
    resp.set_cookie("dir", "drop", secure=True, samesite="Lax", httponly=True)
    return resp


@app.route("/blank")
def blank_page():
    return render_template("blank.html")


@app.route("/script.js")
def js():
    return send_from_directory(os.path.join(app.root_path, "static"), "script.js")


@app.route("/script_video.js")
def js_vid():
    return send_from_directory(os.path.join(app.root_path, "static"), "videos.js")


@app.route("/list.js")
def list_js():
    return send_from_directory(os.path.join(app.root_path, "static"), "list.js")


@app.route("/list_vid.js")
def list_js_vid():
    return send_from_directory(os.path.join(app.root_path, "static"), "list_vid.js")


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, "static"), "favicon.ico")


def underscored_photos():
    path = os.path.join(BASE_DIR, directory_name)
    list = os.listdir(path)
    for item in list:
        if not item.startswith("_"):
            list.remove(item)
    return list, path


@app.errorhandler(HTTPException)
def redirect_index(e):
    flash(str(e.code) + " " + e.name + ": (" + request.url + ") [" + request.method + "]")
    return redirect(url_for('index'))


def get_all_photos(directory_name):
    path = os.path.join(BASE_DIR, directory_name)
    try:
        list = os.listdir(path)
    except FileNotFoundError:
        list = ["FileNotFoundError.jpg"]
    for item in list:
        if not item.endswith("jpg"):
            list.remove(item)
    return list, path


def get_all_videos(directory_name):
    path = os.path.join(BASE_DIR, directory_name)
    path = os.path.join(path, "vid")
    try:
        list = os.listdir(path)
    except FileNotFoundError as e:
        list = ["FileNotFoundError.mp4"]
    for item in list:
        if not item.endswith("mp4"):
            list.remove(item)
    return list, path


def get_first_underscored_video_number(dir):
    try:
        list_vids, path = get_all_videos(dir)
    except:
        return 0
    number = 0
    for item in list_vids:
        if not item.startswith("_"):
            number += 1
        else:
            return number


def get_first_underscored_photo_number(dir):
    try:
        list_photos, path = get_all_photos(dir)
    except:
        return 0
    number = 0
    for item in list_photos:
        if not item.startswith("_"):
            number += 1
        else:
            return number


def get_all_dirs():
    return os.listdir(BASE_DIR)
