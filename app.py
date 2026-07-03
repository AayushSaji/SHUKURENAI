import base64
import io
from urllib.parse import urlparse

import segno
import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

st.set_page_config(page_title="Workspace Studio", layout="wide", initial_sidebar_state="expanded")


def init_state():
    defaults = {
        "mode": "🎨 Advanced Image Studio",
        "qr_fg": "#111111",
        "qr_bg": "#f4f4f4",
        "filter_name": "Original",
        "quality": 85,
        "crop_top": 0,
        "crop_bottom": 0,
        "crop_left": 0,
        "crop_right": 0,
        "resize_width": 0,
        "resize_height": 0,
        "resize_keep_aspect": True,
        "last_warning": "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def file_bytes(uploader):
    if uploader is None:
        return None
    return uploader.getvalue()


def open_image(uploader):
    try:
        return Image.open(io.BytesIO(file_bytes(uploader))).convert("RGBA")
    except Exception as e:
        st.warning(f"Could not open image: {e}")
        return None


def sepia(img):
    gray = ImageOps.grayscale(img).convert("RGB")
    out = Image.new("RGB", gray.size)
    pixels = out.load()
    src = gray.load()
    for y in range(gray.size[1]):
        for x in range(gray.size[0]):
            p = src[x, y]
            r = min(255, int(p * 1.07))
            g = min(255, int(p * 0.74))
            b = min(255, int(p * 0.43))
            pixels[x, y] = (r, g, b)
    return out.convert("RGBA")


def apply_filter(img, name):
    try:
        base = img.convert("RGBA")
        if name == "Original":
            return base
        if name == "Black & White":
            return ImageOps.grayscale(base).convert("RGBA")
        if name == "Sepia Tone":
            return sepia(base)
        if name == "Gaussian Blur":
            return base.filter(ImageFilter.GaussianBlur(radius=3))
        if name == "Contour Sketch":
            return base.filter(ImageFilter.CONTOUR)
        if name == "Vibrant Saturation":
            return ImageEnhance.Color(base).enhance(1.8)
        if name == "Retro Negative":
            rgb = ImageOps.invert(base.convert("RGB"))
            return rgb.convert("RGBA")
        if name == "Emboss Art":
            return base.filter(ImageFilter.EMBOSS)
        return base
    except Exception as e:
        st.warning(f"Filter warning: {e}")
        return img


def crop_image(img, top, bottom, left, right):
    try:
        w, h = img.size
        left = max(0, min(left, w - 1))
        right = max(0, min(right, w - 1))
        top = max(0, min(top, h - 1))
        bottom = max(0, min(bottom, h - 1))
        box = (left, top, max(left + 1, w - right), max(top + 1, h - bottom))
        return img.crop(box)
    except Exception as e:
        st.warning(f"Crop warning: {e}")
        return img


def resize_image(img, width, height, keep_aspect):
    try:
        if keep_aspect:
            if width and not height:
                ratio = width / img.size[0]
                height = max(1, int(img.size[1] * ratio))
            elif height and not width:
                ratio = height / img.size[1]
                width = max(1, int(img.size[0] * ratio))
            elif not width and not height:
                return img
            else:
                ratio = min(width / img.size[0], height / img.size[1])
                width = max(1, int(img.size[0] * ratio))
                height = max(1, int(img.size[1] * ratio))
        if width and height:
            return img.resize((int(width), int(height)), Image.LANCZOS)
        return img
    except Exception as e:
        st.warning(f"Resize warning: {e}")
        return img


def image_to_download_bytes(img, quality):
    try:
        buf = io.BytesIO()
        save_img = img.convert("RGB")
        save_img.save(buf, format="JPEG", quality=int(quality), optimize=True)
        return buf.getvalue()
    except Exception as e:
        st.warning(f"Compression warning: {e}")
        return None


def qr_from_text(content, fg, bg):
    try:
        qr = segno.make(content, error="m")
        out = io.BytesIO()
        qr.save(out, kind="png", scale=8, dark=fg, light=bg)
        return out.getvalue()
    except Exception as e:
        st.warning(f"QR generation warning: {e}")
        return None


def image_payload_text(uploaded):
    try:
        raw = file_bytes(uploaded)
        b64 = base64.b64encode(raw).decode("utf-8")
        mime = uploaded.type or "application/octet-stream"
        return f"data:{mime};base64,{b64}"
    except Exception as e:
        st.warning(f"Base64 warning: {e}")
        return None


init_state()

with st.sidebar:
    st.title("Workspace")
    st.session_state.mode = st.radio(
        "Navigation",
        ["🎨 Advanced Image Studio", "🔮 Universal QR Engine"],
        index=0 if st.session_state.mode == "🎨 Advanced Image Studio" else 1,
    )
    st.color_picker("QR dark color", value=st.session_state.qr_fg, key="qr_fg")
    st.color_picker("QR light color", value=st.session_state.qr_bg, key="qr_bg")

st.markdown("# Production Workspace")
st.markdown("A single-file app for image editing and QR generation.")

if st.session_state.mode == "🎨 Advanced Image Studio":
    st.markdown("## Advanced Image Studio")
    up = st.file_uploader("Upload PNG, JPG, or JPEG", type=["png", "jpg", "jpeg"])
    if up:
        src = open_image(up)
        if src:
            c1, c2 = st.columns(2)
            with c1:
                st.image(src, caption="Original", use_container_width=True)
            with c2:
                st.session_state.filter_name = st.selectbox(
                    "Filter",
                    [
                        "Original",
                        "Black & White",
                        "Sepia Tone",
                        "Gaussian Blur",
                        "Contour Sketch",
                        "Vibrant Saturation",
                        "Retro Negative",
                        "Emboss Art",
                    ],
                    index=[
                        "Original",
                        "Black & White",
                        "Sepia Tone",
                        "Gaussian Blur",
                        "Contour Sketch",
                        "Vibrant Saturation",
                        "Retro Negative",
                        "Emboss Art",
                    ].index(st.session_state.filter_name)
                    if st.session_state.filter_name in [
                        "Original",
                        "Black & White",
                        "Sepia Tone",
                        "Gaussian Blur",
                        "Contour Sketch",
                        "Vibrant Saturation",
                        "Retro Negative",
                        "Emboss Art",
                    ]
                    else 0,
                )
                filtered = apply_filter(src, st.session_state.filter_name)
                st.image(filtered, caption="Filtered", use_container_width=True)

            st.markdown("### Direct Manipulation")
            a, b, c, d = st.columns(4)
            with a:
                st.session_state.crop_top = st.number_input("Crop top", 0, src.size[1] - 1, st.session_state.crop_top, 1)
                st.session_state.crop_bottom = st.number_input("Crop bottom", 0, src.size[1] - 1, st.session_state.crop_bottom, 1)
            with b:
                st.session_state.crop_left = st.number_input("Crop left", 0, src.size[0] - 1, st.session_state.crop_left, 1)
                st.session_state.crop_right = st.number_input("Crop right", 0, src.size[0] - 1, st.session_state.crop_right, 1)
            with c:
                st.session_state.resize_keep_aspect = st.checkbox("Keep aspect ratio", value=st.session_state.resize_keep_aspect)
                st.session_state.resize_width = st.number_input("Width", 0, 10000, st.session_state.resize_width, 1)
            with d:
                st.session_state.resize_height = st.number_input("Height", 0, 10000, st.session_state.resize_height, 1)
                st.session_state.quality = st.slider("Compression quality", 1, 100, int(st.session_state.quality))

            processed = filtered.copy()
            processed = crop_image(processed, st.session_state.crop_top, st.session_state.crop_bottom, st.session_state.crop_left, st.session_state.crop_right)
            processed = resize_image(processed, st.session_state.resize_width, st.session_state.resize_height, st.session_state.resize_keep_aspect)

            out_bytes = image_to_download_bytes(processed, st.session_state.quality)
            if out_bytes:
                st.markdown("### Optimized Output")
                p1, p2 = st.columns(2)
                with p1:
                    st.image(processed, caption="Processed", use_container_width=True)
                with p2:
                    st.metric("Original file size", f"{len(file_bytes(up)) / 1024:.1f} KB")
                    st.metric("Exported file size", f"{len(out_bytes) / 1024:.1f} KB")
                    st.metric("Estimated savings", f"{max(0, 100 - (len(out_bytes) / len(file_bytes(up)) * 100)):.1f}%")
                    st.download_button(
                        "Download processed image",
                        data=out_bytes,
                        file_name="processed_image.jpg",
                        mime="image/jpeg",
                    )
elif st.session_state.mode == "🔮 Universal QR Engine":
    st.markdown("## Universal QR Engine")
    pipeline = st.radio("Pipeline", ["Text to QR", "Link to QR", "Image to QR Pipeline"], horizontal=True)

    if pipeline == "Text to QR":
        text = st.text_area("Enter raw text", height=220, placeholder="Type paragraphs here...")
        if text.strip():
            qr_bytes = qr_from_text(text, st.session_state.qr_fg, st.session_state.qr_bg)
            if qr_bytes:
                c1, c2 = st.columns(2)
                with c1:
                    st.image(qr_bytes, caption="QR Code", use_container_width=True)
                with c2:
                    st.code(text, language="text")
                    st.download_button("Download QR PNG", data=qr_bytes, file_name="text_qr.png", mime="image/png")

    elif pipeline == "Link to QR":
        link = st.text_input("Enter absolute URL", placeholder="https://example.com")
        if link.strip():
            parsed = urlparse(link.strip())
            if parsed.scheme in ("http", "https") and parsed.netloc:
                qr_bytes = qr_from_text(link.strip(), st.session_state.qr_fg, st.session_state.qr_bg)
                if qr_bytes:
                    c1, c2 = st.columns(2)
                    with c1:
                        st.image(qr_bytes, caption="QR Code", use_container_width=True)
                    with c2:
                        st.write(link.strip())
                        st.download_button("Download QR PNG", data=qr_bytes, file_name="link_qr.png", mime="image/png")
            else:
                st.warning("Please enter a valid absolute URL starting with http:// or https://")

    else:
        up = st.file_uploader("Upload an image for payload conversion", type=["png", "jpg", "jpeg"])
        if up:
            payload = image_payload_text(up)
            if payload:
                st.info("Image payload converted to a Base64 data URI string. Large images may exceed practical QR limits.")
                payload_preview = payload[:2000] + ("..." if len(payload) > 2000 else "")
                qr_bytes = qr_from_text(payload_preview, st.session_state.qr_fg, st.session_state.qr_bg)
                c1, c2 = st.columns(2)
                with c1:
                    st.image(qr_bytes, caption="Payload QR Preview", use_container_width=True)
                with c2:
                    st.code(payload_preview, language="text")
                    st.download_button("Download QR PNG", data=qr_bytes, file_name="image_payload_qr.png", mime="image/png")
