#!/usr/bin/env python
# A simple script to suck up HTML, convert any images to inline Base64
# encoded format and write out the converted file.
#
# Usage: python standalone_html.py <input_file.html> <output_file.html>
#
# TODO: Consider MHTML format: https://en.wikipedia.org/wiki/MHTML

import os
import re
from bs4 import BeautifulSoup, Tag, NavigableString


def guess_type(filepath):
    """
    Return the mimetype of a file, given it's path.
    This is a wrapper around two alternative methods - Unix 'file'-style
    magic which guesses the type based on file content (if available),
    and simple guessing based on the file extension (eg .jpg).
    :param filepath: Path to the file.
    :type filepath: str
    :return: Mimetype string.
    :rtype: str
    """
    try:
        import magic  # python-magic

        type = magic.from_file(filepath, mime=True)
        if type == "application/octet-stream":
            import mimetypes

            return mimetypes.guess_type(filepath)[0]
        else:
            return type
    except ImportError:
        import mimetypes

        return mimetypes.guess_type(filepath)[0]


def file_to_base64(filepath):
    """
    Returns the content of a file as a Base64 encoded string.
    :param filepath: Path to the file.
    :type filepath: str
    :return: The file content, Base64 encoded.
    :rtype: str
    """
    import base64

    with open(filepath, "rb") as f:
        encoded_str = base64.b64encode(f.read())
    return encoded_str.decode("utf-8")


def read_file(filepath):
    with open(filepath, "r") as f:
        return f.read()


def read_and_embed_css(filepath):
    with open(filepath, "r") as f:
        blob = f.read()
        while True:
            m = re.search(r"src:url\((.\/.*?)\)", blob)
            if not m:
                break
            path = m.group(1)
            span = m.span()

            mimetype = guess_type(path)
            replace = "src:url(data:%s;base64,%s)" % (mimetype, file_to_base64(path))
            blob = blob.replace(blob[span[0] : span[1]], replace, 1)
        return blob


def make_html_images_inline(in_filepath, out_filepath):
    """
    Takes an HTML file and writes a new version with inline Base64 encoded
    images.
    :param in_filepath: Input file path (HTML)
    :type in_filepath: str
    :param out_filepath: Output file path (HTML)
    :type out_filepath: str
    """
    basepath = os.path.split(in_filepath.rstrip(os.path.sep))[0]
    soup = BeautifulSoup(open(in_filepath, "r"), "html.parser")
    for img in soup.find_all("img"):
        img_path = os.path.join(basepath, img.attrs["src"])
        mimetype = guess_type(img_path)
        img.attrs["src"] = "data:%s;base64,%s" % (mimetype, file_to_base64(img_path))

    for link in soup.find_all("link"):
        if link.attrs["href"][0] != ".":
            continue
        link_path = os.path.join(basepath, link.attrs["href"])
        # link.attrs['href'] = \
        #    "data:text/css;base64,%s" % (file_to_base64(link_path))
        # tag = Tag(soup, "newTag")
        link.name = "style"
        del link.attrs["href"]
        del link.attrs["rel"]
        link.insert(0, read_and_embed_css(link_path))
        # link.replaceWith(tag)

    for script in soup.find_all("script"):
        if not script.attrs:
            continue
        if script.attrs["src"][0] != ".":
            continue
        script_path = os.path.join(basepath, script.attrs["src"])
        script.attrs["src"] = "data:text/javascript;base64,%s" % (file_to_base64(script_path))

    with open(out_filepath, "w") as of:
        of.write(str(soup))


if __name__ == "__main__":
    import sys

    make_html_images_inline(sys.argv[1], sys.argv[2])
