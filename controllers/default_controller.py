from flask import render_template, send_file

def download_locally(path: str):
    try:
        return send_file(path, as_attachment=True)
    except Exception as e:
        return render_template(
            'error.html',
            label="Internal server error: document doesn't exist",
            status=500
        )