# blog/utils.py
import json
import html

def render_editorjs_to_html(json_str):
    try:
        data = json.loads(json_str)
        blocks = data.get("blocks", [])
        html_output = ""

        for block in blocks:
            t = block.get("type")
            d = block.get("data")

            if t == "header":
                level = d.get("level", 2)
                html_output += f"<h{level}>{d.get('text')}</h{level}>"

            elif t == "paragraph":
                html_output += f"<p>{d.get('text')}</p>"

            elif t == "code":
                escaped = html.escape(d.get("code", ""))
                html_output += f"<pre><code>{escaped}</code></pre>"

            elif t == "quote":
                caption = f"<small>{d.get('caption')}</small>" if d.get('caption') else ''
                html_output += f"<blockquote>{d.get('text')}<br>{caption}</blockquote>"

            elif t == "image":
                url = d.get("file", {}).get("url", "")
                caption = d.get("caption", "")
                if url:
                    html_output += f"<figure><img src='{url}' class='img-fluid'/><figcaption>{caption}</figcaption></figure>"

            elif t == "list":
                style = d.get("style", "unordered")
                tag = "ul" if style == "unordered" else "ol"
                items = "".join(f"<li>{item}</li>" for item in d.get("items", []))
                html_output += f"<{tag}>{items}</{tag}>"

            elif t == "table":
                rows = d.get("content", [])
                html_output += "<table class='table table-bordered'>"
                for row in rows:
                    html_output += "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>"
                html_output += "</table>"

            elif t == "embed":  # YouTube
                embed = d.get("embed")
                if embed:
                    html_output += (
                        f"<div class='ratio ratio-16x9 mb-2'>"
                        f"<iframe src='{embed}' frameborder='0' allowfullscreen></iframe>"
                        f"</div>"
                    )

            else:
                html_output += f"<div class='text-muted'>[Unsupported block: {t}]</div>"

        return html_output

    except Exception as e:
        return f"<div class='text-danger'>Ошибка парсинга: {str(e)}</div>"
